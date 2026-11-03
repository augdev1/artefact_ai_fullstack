"""LangChain / LangGraph ReAct Agent for Empório da Música."""

import logging
from typing import Dict, Any, List, Optional

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from app.config import settings
from app.agent.persona import SYSTEM_PROMPT
from app.agent.guardrails import ScopeGuardrail
from app.agent.memory import message_store, PersistentMessageStore
from app.tools.langchain_tools import LANGCHAIN_TOOLS

logger = logging.getLogger(__name__)

class LangChainAgent:
    def __init__(
        self,
        provider: Optional[str] = None,
        memory: Optional[PersistentMessageStore] = None
    ):
        self.provider = provider or settings.LLM_PROVIDER
        self.memory = memory or message_store
        self._agent_graph = None

    def _get_agent_graph(self):
        """Lazily initialize the modern LangGraph ReAct agent."""
        if self._agent_graph is not None:
            return self._agent_graph

        if self.provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.2
            )
        elif self.provider == "openai":
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL,
                temperature=0.2
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

        self._agent_graph = create_react_agent(
            model=llm,
            tools=LANGCHAIN_TOOLS,
            prompt=SYSTEM_PROMPT
        )
        return self._agent_graph

    def process_message(
        self,
        message: str,
        session_id: str = "default",
        force_mock: bool = False
    ) -> Dict[str, Any]:
        """
        Process user message through Guardrails, LangChain ReAct loop, and Persistence.
        """
        # 1. Deterministic Guardrail Check
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

        raw_history = self.memory.get_history(session_id)

        # 2. Check for mock mode or run LangChain Agent
        if force_mock or self.provider == "mock":
            from app.agent.engine import agent_engine
            res, tools = agent_engine._run_mock_agent(message, raw_history)
            self.memory.add_message(session_id, {"role": "user", "content": message})
            self.memory.add_message(session_id, {"role": "assistant", "content": res}, tools_called=tools)
            return {
                "response": res,
                "session_id": session_id,
                "tools_used": tools,
                "guardrail_triggered": False,
                "guardrail_reason": None
            }

        # 3. Add user message
        self.memory.add_message(session_id, {"role": "user", "content": message})

        # 4. Prepare message list for LangGraph ReAct agent
        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        for h in raw_history:
            if h["role"] == "user":
                messages.append(HumanMessage(content=h["content"]))
            elif h["role"] == "assistant":
                messages.append(AIMessage(content=h["content"]))
        messages.append(HumanMessage(content=message))

        try:
            graph = self._get_agent_graph()
            result = graph.invoke({"messages": messages})
            
            output_messages = result.get("messages", [])
            final_message = output_messages[-1] if output_messages else AIMessage(content="")
            response_text = final_message.content

            # Extract any tools called during the agent execution
            tools_used = []
            for m in output_messages:
                if isinstance(m, ToolMessage) and m.name:
                    tools_used.append(m.name)
                elif hasattr(m, "tool_calls") and m.tool_calls:
                    for tc in m.tool_calls:
                        if isinstance(tc, dict) and "name" in tc:
                            tools_used.append(tc["name"])

            self.memory.add_message(session_id, {"role": "assistant", "content": response_text}, tools_called=tools_used)

            return {
                "response": response_text,
                "session_id": session_id,
                "tools_used": list(set(tools_used)),
                "guardrail_triggered": False,
                "guardrail_reason": None
            }

        except Exception as e:
            logger.error("LangChain agent execution error: %s. Falling back to deterministic engine.", e)
            from app.agent.engine import agent_engine
            res, tools = agent_engine._run_mock_agent(message, raw_history)
            self.memory.add_message(session_id, {"role": "assistant", "content": res}, tools_called=tools)
            return {
                "response": res,
                "session_id": session_id,
                "tools_used": tools,
                "guardrail_triggered": False,
                "guardrail_reason": None
            }

langchain_agent = LangChainAgent()
