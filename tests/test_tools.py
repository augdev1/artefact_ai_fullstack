import pytest
from app.db.database import DatabaseManager
from app.tools.catalog_tools import search_products, get_product_details, list_promotions
from app.tools.order_tools import get_order_status
from app.tools.policy_tools import get_store_policies
from app.tools.dispatcher import ToolDispatcher

def test_search_violões_under_1000(memory_db: DatabaseManager):
    """Test scenario from challenge PDF: 'Quais opções de violões disponíveis custando até R$1000?'"""
    results = search_products(
        query="violão",
        max_price=1000.0,
        in_stock_only=True,
        db=memory_db
    )
    assert len(results) > 0
    for p in results:
        assert p["current_price_brl"] <= 1000.0
        assert p["stock_quantity"] > 0
        assert p["pix_price_brl"] <= p["current_price_brl"]

def test_get_takamine_gd20_price(memory_db: DatabaseManager):
    """Test scenario from challenge PDF: 'Quanto custa o Takamine GD20?'"""
    product = get_product_details("Takamine GD20", db=memory_db)
    assert product is not None
    assert "Takamine GD20" in product["name"]
    assert product["original_price_brl"] > 0
    assert product["pix_price_brl"] > 0
    assert product["stock_quantity"] >= 0
    assert "installment_options" in product
    assert product["installment_options"]["max_installments"] == 12

def test_order_status_by_id(memory_db: DatabaseManager):
    """Test querying real order from dataset."""
    order = get_order_status(order_id=1, db=memory_db)
    assert order["found"] is True
    assert order["order_id"] == 1
    assert order["status"] == "delivered"
    assert len(order["items"]) > 0
    assert order["tracking_code"] != ""

def test_order_status_not_found(memory_db: DatabaseManager):
    """Test order status lookup with non-existent ID."""
    order = get_order_status(order_id=99999, db=memory_db)
    assert order["found"] is False

def test_list_active_promotions_only(memory_db: DatabaseManager):
    """Verify that only promotions with is_active = 1 are returned when requested."""
    promos = list_promotions(active_only=True, db=memory_db)
    assert len(promos) > 0
    for p in promos:
        assert p["is_active"] is True
        assert p["discount_percent"] > 0

def test_store_policies_remorse_and_hours():
    """Test scenario from challenge PDF: 'Me arrependi da minha compra, posso devolver meu pedido?' and hours."""
    # Remorse / return policy
    res_return = get_store_policies("arrependi da compra posso devolver")
    matched_text = " ".join([p["content"] for p in res_return["matched_policies"]])
    assert "7 (sete) dias" in matched_text or "7 dias" in matched_text
    assert "Código de Defesa do Consumidor" in matched_text or "CDC" in matched_text

    # Hours policy
    res_hours = get_store_policies("horário de funcionamento e endereço")
    hours_text = " ".join([p["content"] for p in res_hours["matched_policies"]])
    assert "09:00" in hours_text
    assert "Campo Grande" in hours_text

def test_tool_dispatcher_execution(memory_db: DatabaseManager):
    """Verify ToolDispatcher wraps and executes tools properly."""
    dispatcher = ToolDispatcher(db=memory_db)
    
    # Search tool
    res = dispatcher.execute_tool("search_products", {"query": "Yamaha", "limit": 2})
    assert "results" in res
    assert len(res["results"]) <= 2

    # Policies tool
    res_pol = dispatcher.execute_tool("get_store_policies", {"topic_or_query": "pix"})
    assert "matched_policies" in res_pol

