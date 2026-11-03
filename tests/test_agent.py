import pytest
from app.agent.engine import AgentEngine
from app.agent.memory import MessageStore
from app.tools.dispatcher import ToolDispatcher
from app.db.database import DatabaseManager

@pytest.fixture
def test_engine(memory_db: DatabaseManager):
    store = MessageStore()
    dispatcher = ToolDispatcher(db=memory_db)
    return AgentEngine(provider="mock", dispatcher=dispatcher, store=store)

def test_agent_catalog_query(test_engine: AgentEngine):
    res = test_engine.process_message("Quais opções de violões disponíveis custando até R$1000?", session_id="test_1")
    assert "search_products" in res["tools_used"]
    assert res["guardrail_triggered"] is False
    assert "violões" in res["response"].lower() or "yamaha" in res["response"].lower()
    assert len(test_engine.memory.get_history("test_1")) == 2

def test_agent_product_price_query(test_engine: AgentEngine):
    res = test_engine.process_message("Quanto custa o Takamine GD20?", session_id="test_2")
    assert "get_product_details" in res["tools_used"]
    assert "Takamine GD20" in res["response"]
    assert "PIX" in res["response"]

def test_agent_order_status_query(test_engine: AgentEngine):
    res = test_engine.process_message("Qual o status do meu pedido 1?", session_id="test_3")
    assert "check_order_status" in res["tools_used"]
    assert "pedido #1" in res["response"].lower()

def test_agent_policy_query(test_engine: AgentEngine):
    res = test_engine.process_message("Me arrependi da minha compra, posso devolver meu pedido?", session_id="test_4")
    assert "get_store_policies" in res["tools_used"]
    assert "7" in res["response"] or "devolução" in res["response"].lower()

def test_agent_accessory_guardrail_trigger(test_engine: AgentEngine):
    res = test_engine.process_message("Vocês vendem encordoamento para violão?", session_id="test_5")
    assert res["guardrail_triggered"] is True
    assert res["guardrail_reason"] == "accessory_request"
    assert len(res["tools_used"]) == 0
    assert "exclusivamente com a venda de instrumentos" in res["response"]

def test_agent_multiturn_memory(test_engine: AgentEngine):
    sid = "multi_turn"
    test_engine.process_message("Olá! Qual o horário de funcionamento?", session_id=sid)
    test_engine.process_message("E qual o endereço da loja?", session_id=sid)
    history = test_engine.memory.get_history(sid)
    assert len(history) == 4  # 2 user msgs + 2 assistant msgs

