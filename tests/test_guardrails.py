import pytest
from app.agent.guardrails import ScopeGuardrail

@pytest.mark.parametrize("query", [
    "Vocês vendem palheta de guitarra?",
    "Tem encordoamento para violão?",
    "Quero comprar um amplificador Fender",
    "Vocês vendem cabo P10 de 5 metros?",
    "Qual o preço do pedal de distorção?",
    "Vocês têm afinador digital avulso?",
    "Vocês vendem case rígido para guitarra?",
])
def test_accessories_guardrail_blocks(query: str):
    """Ensure that inquiries for accessories are strictly caught and blocked."""
    is_blocked, reason, response = ScopeGuardrail.check_scope(query)
    assert is_blocked is True
    assert reason == "accessory_request"
    assert "exclusivamente com a venda de instrumentos" in response or "não comercializamos acessórios" in response

@pytest.mark.parametrize("query", [
    "Quais opções de violões de nylon vocês têm?",
    "Quanto custa o Takamine GD20?",
    "Vocês têm contrabaixo de 5 cordas?",
    "Qual o endereço da loja?",
    "Posso devolver meu pedido em 7 dias?",
])
def test_legitimate_musical_queries_pass(query: str):
    """Ensure legitimate musical instrument or store policy queries pass through."""
    is_blocked, reason, response = ScopeGuardrail.check_scope(query)
    assert is_blocked is False
    assert reason is None
    assert response is None

@pytest.mark.parametrize("query", [
    "Como fazer uma receita de bolo de fubá?",
    "Escreva um código em Python para mim",
    "Quem venceu a eleição presidencial?",
    "Qual a previsão do tempo para amanhã?",
])
def test_off_topic_queries_block(query: str):
    """Ensure unrelated off-topic queries are politely declined."""
    is_blocked, reason, response = ScopeGuardrail.check_scope(query)
    assert is_blocked is True
    assert reason == "off_topic"
    assert "instrumentos musicais" in response

