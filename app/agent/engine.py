"""Agent Engine: ReAct / Tool-calling cognitive architecture with multi-provider support."""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple

from app.config import settings
from app.agent.persona import SYSTEM_PROMPT
from app.agent.guardrails import ScopeGuardrail
from app.agent.memory import message_store, MessageStore
from app.tools.dispatcher import tool_dispatcher, ToolDispatcher
from app.tools.definitions import TOOL_DEFINITIONS

logger = logging.getLogger(__name__)

# Fallback models for Gemini if a specific model has temporary spikes/503
GEMINI_MODELS = ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.8-flash"]

class AgentEngine:
    def __init__(
        self,
        provider: Optional[str] = None,
        dispatcher: Optional[ToolDispatcher] = None,
        store: Optional[MessageStore] = None
    ):
        self.provider = provider or settings.LLM_PROVIDER
        self.dispatcher = dispatcher or tool_dispatcher
        self.memory = store or message_store

    def process_message(
        self,
        message: str,
        session_id: str = "default",
        force_mock: bool = False
    ) -> Dict[str, Any]:
        """
        Process a user message through guardrails, tool calling, and response synthesis.
        """
        # 1. Guardrail Check (Deterministic Scope Verification)
        is_blocked, reason, guardrail_response = ScopeGuardrail.check_scope(message)
        if is_blocked and guardrail_response:
            self.memory.add_message(session_id, {"role": "user", "content": message})
            self.memory.add_message(session_id, {"role": "assistant", "content": guardrail_response})
            return {
                "response": guardrail_response,
                "session_id": session_id,
                "tools_used": [],
                "guardrail_triggered": True,
                "guardrail_reason": reason
            }

        # 2. Add user message to history
        self.memory.add_message(session_id, {"role": "user", "content": message})
        history = self.memory.get_history(session_id)

        # 3. Route to provider
        active_provider = "mock" if force_mock else self.provider

        if active_provider == "mock":
            response, tools_used = self._run_mock_agent(message, history)
        elif active_provider == "gemini":
            response, tools_used = self._run_gemini_agent(message, history)
        elif active_provider == "openai":
            response, tools_used = self._run_openai_agent(message, history)
        else:
            raise ValueError(f"Unknown LLM provider: {active_provider}")

        # 4. Save assistant response
        self.memory.add_message(session_id, {"role": "assistant", "content": response})

        return {
            "response": response,
            "session_id": session_id,
            "tools_used": tools_used,
            "guardrail_triggered": False,
            "guardrail_reason": None
        }

    def _run_gemini_agent(self, user_msg: str, history: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
        """Run agent via Google GenAI SDK with native function calling."""
        from google.genai import Client, types

        client = Client(api_key=settings.GEMINI_API_KEY)
        tools_used = []

        # Convert tool definitions to Gemini FunctionDeclarations
        func_declarations = []
        for t in TOOL_DEFINITIONS:
            func_declarations.append(
                types.FunctionDeclaration(
                    name=t["name"],
                    description=t["description"],
                    parameters=t["parameters"]
                )
            )

        gemini_tools = [types.Tool(function_declarations=func_declarations)]

        # Prepare messages
        contents = []
        for msg in history[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_msg)]))

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=gemini_tools,
            temperature=0.3
        )

        last_error = None
        models_to_try = [settings.GEMINI_MODEL] + [m for m in GEMINI_MODELS if m != settings.GEMINI_MODEL]

        for model_name in models_to_try:
            try:
                # Turn 1: model decides whether to call tools
                res = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config
                )

                # Loop for handling tool calls (ReAct execution loop)
                max_iterations = 4
                iterations = 0
                while iterations < max_iterations:
                    iterations += 1
                    function_calls = res.function_calls

                    if not function_calls:
                        return (res.text or "Olá! Como posso ajudar você hoje na Empório da Música?", tools_used)

                    # Execute all requested function calls
                    tool_parts = []
                    for call in function_calls:
                        tool_name = call.name
                        tool_args = call.args or {}
                        tools_used.append(tool_name)

                        tool_result = self.dispatcher.execute_tool(tool_name, tool_args)
                        tool_parts.append(
                            types.Part.from_function_response(
                                name=tool_name,
                                response={"result": tool_result}
                            )
                        )

                    # Append model turn and tool response turn
                    contents.append(res.candidates[0].content)
                    contents.append(types.Content(role="user", parts=tool_parts))

                    # Send tool outputs back to model
                    res = client.models.generate_content(
                        model=model_name,
                        contents=contents,
                        config=config
                    )

                return (res.text or "Posso te ajudar com algo mais sobre nossos instrumentos?", tools_used)

            except Exception as e:
                logger.warning("Gemini model %s failed: %s. Trying fallback...", model_name, e)
                last_error = e
                continue

        logger.error("All Gemini models failed, falling back to deterministic mock agent: %s", last_error)
        return self._run_mock_agent(user_msg, history)

    def _run_openai_agent(self, user_msg: str, history: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
        """Run agent via OpenAI-compatible SDK."""
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)
        tools_used = []

        openai_tools = [{"type": "function", "function": t} for t in TOOL_DEFINITIONS]

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        max_iterations = 4
        iterations = 0
        while iterations < max_iterations:
            iterations += 1
            res = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                tools=openai_tools,
                temperature=0.3
            )
            msg = res.choices[0].message
            if not msg.tool_calls:
                return (msg.content or "", tools_used)

            messages.append(msg)
            for tc in msg.tool_calls:
                tool_name = tc.function.name
                tool_args = tc.function.arguments
                tools_used.append(tool_name)
                tool_result = self.dispatcher.execute_tool(tool_name, tool_args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tool_name,
                    "content": json.dumps(tool_result, ensure_ascii=False)
                })

        return ("Como posso te ajudar mais com os instrumentos da Empório da Música?", tools_used)

    def _run_mock_agent(self, user_msg: str, history: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
        """
        Deterministic Mock Agent Engine for 100% offline testing and test harness verification.
        Resolves intents and tools without external API dependency.
        """
        msg_lower = user_msg.lower()
        tools_used = []

        # 1. Store policies (returns, regret, exchanges, hours, address, payment, pix + promo rules)
        # Evaluated before products so policy questions about orders or promotions route to policies
        if any(w in msg_lower for w in [
            "arrependi", "devolver", "devolução", "devolucao", "troca", "trocar",
            "endereço", "endereco", "onde fica", "horário", "horario", "frete",
            "cumulativo", "não cumulativo"
        ]) or ("pix" in msg_lower and ("promo" in msg_lower or "desconto" in msg_lower or "acumula" in msg_lower)):
            tools_used.append("get_store_policies")
            res = self.dispatcher.execute_tool("get_store_policies", {"topic_or_query": user_msg})
            pol = res.get("matched_policies", [{}])[0]
            return (
                f"Sobre isso, nossa política é bem clara:\n\n{pol.get('content', '')}\n\nSe precisar de mais alguma informação, estou aqui para ajudar!",
                tools_used
            )

        # 2. Product price / details (e.g. Takamine GD20)
        if "takamine" in msg_lower or ("preço" in msg_lower and any(inst in msg_lower for inst in ["gd20", "c40", "yamaha", "fender", "tagima"])):
            tools_used.append("get_product_details")
            name = "Takamine GD20" if "takamine" in msg_lower else "Yamaha C40"
            res = self.dispatcher.execute_tool("get_product_details", {"name_or_id": name})
            if res.get("found"):
                p = res["product"]
                return (
                    f"O {p['name']} está saindo por R$ {p['current_price_brl']:,.2f}. "
                    f"No PIX à vista você garante 5% de desconto e ele sai por R$ {p['pix_price_brl']:,.2f}, "
                    f"ou você pode parcelar em até 12x de R$ {p['installment_options']['installment_value']:,.2f} sem juros. "
                    f"Temos {p['stock_quantity']} unidades disponíveis em estoque!",
                    tools_used
                )

        # 3. Catalog search with price (e.g. violões até 1000)
        if any(w in msg_lower for w in ["viol", "guitarra", "bateria", "teclado", "baixo", "sopro"]) and any(w in msg_lower for w in ["1000", "500", "2000", "opç", "opc", "até", "ate", "custando", "quanto custa"]):
            tools_used.append("search_products")
            max_p = 1000.0 if "1000" in msg_lower else (500.0 if "500" in msg_lower else 2000.0)
            cat = "Violões" if "viol" in msg_lower else None
            res = self.dispatcher.execute_tool("search_products", {"query": "violão", "category_name": cat, "max_price": max_p})
            items = res.get("results", [])
            if items:
                lines = [f"- **{it['name']}**: R$ {it['current_price_brl']:.2f} (ou R$ {it['pix_price_brl']:.2f} no PIX, estoque: {it['stock_quantity']} un)" for it in items]
                return (
                    f"Com certeza! Temos ótimas opções de violões disponíveis custando até R$ {max_p:.0f}:\n\n"
                    + "\n".join(lines)
                    + "\n\nQual desses modelos combina mais com seu estilo musical?",
                    tools_used
                )

        # 4. Order status check (status, rastreio, onde está o pedido)
        if any(w in msg_lower for w in ["status", "rastreio", "rastreamento", "onde está", "onde esta", "meu pedido"]):
            tools_used.append("check_order_status")
            import re
            m = re.search(r"\b(\d+)\b", msg_lower)
            order_id = int(m.group(1)) if m else 1
            res = self.dispatcher.execute_tool("check_order_status", {"order_id": order_id})
            if res.get("found"):
                return (
                    f"Consultei aqui! O seu pedido #{res['order_id']} está com o status: **{res['status_description']}**.\n"
                    f"Código de rastreamento: `{res['tracking_code']}`. Previsão de entrega: {res['estimated_delivery']}.",
                    tools_used
                )
            else:
                return ("Não localizei nenhum pedido com esse número. Poderia me confirmar o número correto ou seu e-mail?", tools_used)

        # 4. Promotions check
        if any(w in msg_lower for w in ["promoção", "promocao", "promoções", "promocoes", "desconto", "black friday"]):
            tools_used.append("list_promotions")
            res = self.dispatcher.execute_tool("list_promotions", {"active_only": True})
            promos = res.get("promotions", [])
            if promos:
                p_lines = [f"- **{p['product_name']}**: De R$ {p['original_price_brl']:.2f} por R$ {p['promotional_price_brl']:.2f} ({p['discount_percent']:.0f}% OFF - {p['campaign_description']})" for p in promos[:3]]
                return (
                    "Temos promoções ativas imperdíveis no nosso catálogo:\n\n"
                    + "\n".join(p_lines)
                    + "\n\nLembrando que os descontos promocionais não são cumulativos com o desconto de PIX!",
                    tools_used
                )

        # 5. Store policies (address, hours, return, payment)
        if any(w in msg_lower for w in ["endereço", "endereco", "onde fica", "horário", "horario", "troca", "devolver", "arrependi", "frete", "pix"]):
            tools_used.append("get_store_policies")
            res = self.dispatcher.execute_tool("get_store_policies", {"topic_or_query": user_msg})
            pol = res.get("matched_policies", [{}])[0]
            return (
                f"Sobre isso, nossa política é bem clara:\n\n{pol.get('content', '')}\n\nSe precisar de mais alguma informação, estou aqui para ajudar!",
                tools_used
            )

        # Default fallback
        return (
            "Olá! Seja bem-vindo à Empório da Música em Campo Grande/MS. "
            "Sou o assistente virtual da loja e posso te ajudar a pesquisar instrumentos, conferir preços, "
            "acompanhar seus pedidos ou tirar dúvidas sobre nossas formas de pagamento e entrega. Como posso ajudar seu som hoje?",
            tools_used
        )

agent_engine = AgentEngine()
