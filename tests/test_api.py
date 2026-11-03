import pytest
from fastapi.testclient import TestClient
from app.api.server import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check_endpoint(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database_ok"] is True

def test_chat_endpoint_with_mock(client: TestClient):
    payload = {
        "message": "Quanto custa o Takamine GD20?",
        "session_id": "api_test_session",
        "force_mock": True
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Takamine GD20" in data["response"]
    assert "get_product_details" in data["tools_used"]
    assert data["guardrail_triggered"] is False

def test_chat_endpoint_guardrail_accessory(client: TestClient):
    payload = {
        "message": "Vocês vendem encordoamento e palhetas?",
        "session_id": "api_test_session_2",
        "force_mock": True
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["guardrail_triggered"] is True
    assert data["guardrail_reason"] == "accessory_request"

def test_chat_history_and_clear(client: TestClient):
    sid = "history_test_session"
    client.post("/api/chat", json={"message": "Qual o endereço da loja?", "session_id": sid, "force_mock": True})
    
    # Check history
    res_hist = client.get(f"/api/chat/history/{sid}")
    assert res_hist.status_code == 200
    messages = res_hist.json()["messages"]
    assert len(messages) == 2

    # Clear history
    res_clear = client.delete(f"/api/chat/history/{sid}")
    assert res_clear.status_code == 200
    assert res_clear.json()["cleared"] is True

    # Verify cleared
    res_hist_after = client.get(f"/api/chat/history/{sid}")
    assert len(res_hist_after.json()["messages"]) == 0

def test_catalog_and_policies_endpoints(client: TestClient):
    res_cat = client.get("/api/catalog?query=violão&max_price=1500")
    assert res_cat.status_code == 200
    assert "products" in res_cat.json()

    res_pol = client.get("/api/policies")
    assert res_pol.status_code == 200
    assert "payment_methods" in res_pol.json()

