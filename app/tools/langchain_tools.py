"""LangChain Tools for Empório da Música Agent."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from app.tools.catalog_tools import search_products, get_product_details, list_promotions
from app.tools.order_tools import get_order_status
from app.tools.policy_tools import get_store_policies
from app.db.database import db_manager

# Input Schemas
class SearchProductsInput(BaseModel):
    query: Optional[str] = Field(None, description="Termo de busca como marca ou tipo de instrumento (ex: 'violão', 'Takamine', 'Yamaha', 'piano', 'bateria')")
    category_name: Optional[str] = Field(None, description="Categoria do instrumento: 'Violões', 'Guitarras', 'Baixos', 'Baterias e Percussão', 'Teclados e Pianos', 'Instrumentos de Sopro (Madeiras)', 'Instrumentos de Sopro (Metais)', 'Cordas Orquestrais', 'Ukuleles'")
    max_price: Optional[float] = Field(None, description="Preço máximo em Reais (ex: 1000.00)")
    min_price: Optional[float] = Field(None, description="Preço mínimo em Reais")
    in_stock_only: bool = Field(True, description="Filtrar apenas itens com estoque > 0")

class ProductDetailsInput(BaseModel):
    name_or_id: str = Field(..., description="Nome do modelo (ex: 'Takamine GD20', 'Yamaha C40') ou ID numérico do produto")

class OrderStatusInput(BaseModel):
    order_id: Optional[int] = Field(None, description="Número de identificação do pedido (ex: 1, 2, 3)")
    tracking_code: Optional[str] = Field(None, description="Código de rastreamento do pedido (ex: 'BRAB1234567BR')")
    customer_phone_or_email: Optional[str] = Field(None, description="E-mail ou telefone do cliente cadastrado")

class PromotionsInput(BaseModel):
    active_only: bool = Field(True, description="Se verdadeiro, lista apenas promoções ativas e válidas atualmente")

class PoliciesInput(BaseModel):
    topic_or_query: str = Field(..., description="Assunto ou dúvida sobre o manual de atendimento: 'horário de funcionamento', 'endereço', 'política de troca e devolução', 'frete e entregas', 'pagamento pix e parcelamento', 'garantia'")

# LangChain Tool Decorators
@tool("search_products", args_schema=SearchProductsInput)
def search_products_tool(
    query: Optional[str] = None,
    category_name: Optional[str] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    in_stock_only: bool = True
) -> str:
    """Busca instrumentos musicais no catálogo da loja por palavras-chave, categoria ou faixa de preço."""
    results = search_products(
        query=query,
        category_name=category_name,
        max_price=max_price,
        min_price=min_price,
        in_stock_only=in_stock_only,
        limit=5,
        db=db_manager
    )
    if not results:
        return "Nenhum instrumento encontrado com esses critérios de busca."
    
    formatted = []
    for p in results:
        promo_info = f" (EM PROMOÇÃO: {p['promotion_discount_percent']}% OFF)" if p['in_promotion'] else ""
        formatted.append(
            f"- **{p['name']}** ({p['category']}): R$ {p['current_price_brl']:.2f}{promo_info} | "
            f"PIX à vista: R$ {p['pix_price_brl']:.2f} | Estoque: {p['stock_quantity']} un | "
            f"Descrição: {p['description']}"
        )
    return "\n".join(formatted)

@tool("get_product_details", args_schema=ProductDetailsInput)
def get_product_details_tool(name_or_id: str) -> str:
    """Consulta detalhes completos de preço, estoque, desconto PIX, parcelamento e especificações de um instrumento musical específico."""
    prod = get_product_details(name_or_id, db=db_manager)
    if not prod:
        return f"Instrumento '{name_or_id}' não encontrado no catálogo da Empório da Música."
    
    promo_str = f"Sim ({prod['promotion_discount_percent']}% OFF - {prod['promotion_campaign']})" if prod['in_promotion'] else "Não"
    inst_val = prod['installment_options']['installment_value']
    
    return (
        f"Detalhes do Instrumento:\n"
        f"- Nome: {prod['name']}\n"
        f"- Categoria: {prod['category']}\n"
        f"- Preço Original: R$ {prod['original_price_brl']:.2f}\n"
        f"- Preço Atual: R$ {prod['current_price_brl']:.2f}\n"
        f"- Preço com Desconto PIX (5% à vista): R$ {prod['pix_price_brl']:.2f}\n"
        f"- Parcelamento: Até 12x de R$ {inst_val:.2f} sem juros no cartão de crédito\n"
        f"- Em Promoção: {promo_str}\n"
        f"- Quantidade em Estoque: {prod['stock_quantity']} unidades\n"
        f"- Especificações: {prod['specs']}\n"
        f"- Descrição: {prod['description']}"
    )

@tool("check_order_status", args_schema=OrderStatusInput)
def check_order_status_tool(
    order_id: Optional[int] = None,
    tracking_code: Optional[str] = None,
    customer_phone_or_email: Optional[str] = None
) -> str:
    """Consulta o status atual, itens e código de rastreamento de um pedido de cliente."""
    order = get_order_status(
        order_id=order_id,
        tracking_code=tracking_code,
        customer_phone_or_email=customer_phone_or_email,
        db=db_manager
    )
    if not order or not order.get("found"):
        return "Nenhum pedido localizado com os dados informados. Por favor, verifique o número do pedido ou código de rastreamento."
    
    items_str = ", ".join([f"{it['quantity']}x {it['product_name']}" for it in order["items"]])
    return (
        f"Dados do Pedido #{order['order_id']}:\n"
        f"- Cliente: {order['customer_name']}\n"
        f"- Data do Pedido: {order['order_date']}\n"
        f"- Status: {order['status_description']}\n"
        f"- Total: R$ {order['total_brl']:.2f}\n"
        f"- Forma de Pagamento: {order['payment_method']}\n"
        f"- Código de Rastreamento: {order['tracking_code']}\n"
        f"- Previsão de Entrega: {order['estimated_delivery']}\n"
        f"- Itens: {items_str}"
    )

@tool("list_promotions", args_schema=PromotionsInput)
def list_promotions_tool(active_only: bool = True) -> str:
    """Lista as promoções ativas cadastradas no sistema da loja."""
    promos = list_promotions(active_only=active_only, db=db_manager)
    if not promos:
        return "No momento não temos produtos com promoções ativas cadastradas."
    
    lines = []
    for p in promos:
        lines.append(
            f"- **{p['product_name']}** ({p['category']}): De R$ {p['original_price_brl']:.2f} por R$ {p['promotional_price_brl']:.2f} "
            f"({p['discount_percent']:.0f}% OFF - {p['campaign_description']}) | Estoque: {p['stock_quantity']} un"
        )
    return "Promoções Ativas:\n" + "\n".join(lines)

@tool("get_store_policies", args_schema=PoliciesInput)
def get_store_policies_tool(topic_or_query: str) -> str:
    """Consulta o manual de políticas internas da loja: horários de funcionamento, endereço, fretes e prazos, formas de pagamento (PIX 5%, parcelamento), regras de trocas e devoluções (7 dias arrependimento CDC), garantia e escopo exclusivo de instrumentos."""
    res = get_store_policies(topic_or_query)
    policies = res.get("matched_policies", [])
    if not policies:
        return "Não encontrei diretrizes específicas para este tema no manual de políticas da loja."
    
    parts = []
    for p in policies:
        parts.append(f"### {p['title']}\n{p['content']}")
    return "\n\n".join(parts)

LANGCHAIN_TOOLS = [
    search_products_tool,
    get_product_details_tool,
    check_order_status_tool,
    list_promotions_tool,
    get_store_policies_tool,
]

