import pytest
from fastapi.testclient import TestClient
from app.api.server import app

@pytest.fixture
def client():
    return TestClient(app)

def test_frontend_index_served_successfully(client: TestClient):
    """Verify that the React SPA is served at root / with status 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    html = response.text

    # 1. Branding check: ARTEFACT stylized typography and exact letter shapes
    assert "ARTEFACT" in html or "RTEF" in html
    assert "polyline points=\"4 21 12 3 20 21\"" in html  # Artefact upward lambda/chevron

    # 2. Colors check: Artefact signature magenta and brand dark
    assert "#E60067" in html or "E60067" in html

    # 3. Sidebar and responsive history check
    assert "Histórico de Conversas" in html
    assert "Nova Conversa" in html

    # 4. Persistence check: LocalStorage keys
    assert "artefact_chat_sessions" in html
    assert "artefact_current_session" in html

    # 5. Store identity: Empório da Música and Campo Grande
    assert "Empório da Música" in html
    assert "Campo Grande" in html
