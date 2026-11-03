"""FastAPI API Routes."""

import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Query, Depends

from app.config import settings
from app.agent.langchain_agent import langchain_agent, LangChainAgent
from app.agent.memory import message_store
from app.knowledge.policies import get_all_policies
from app.tools.catalog_tools import search_products, get_product_details
from app.db.database import db_manager

router = APIRouter(prefix="/api")

# Schemas
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Mensagem do cliente")
    session_id: Optional[str] = Field(None, description="ID de sessão do cliente")
    force_mock: bool = Field(False, description="Forçar motor determinístico mock para testes")

class ChatResponse(BaseModel):
    response: str
    session_id: str
    tools_used: List[str]
    guardrail_triggered: bool
    guardrail_reason: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    provider: str
    model: str
    database_ok: bool

# Routes
@router.get("/health", response_model=HealthResponse)
def health_check():
    """Healthcheck endpoint verifying DB and agent availability."""
    db_ok = False
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            db_ok = (cursor.fetchone()[0] == 1)
    except Exception:
        db_ok = False

    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        provider=settings.LLM_PROVIDER,
        model=settings.GEMINI_MODEL if settings.LLM_PROVIDER == "gemini" else settings.OPENAI_MODEL,
        database_ok=db_ok
    )

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Principal chat endpoint for customer messages.
    Invokes guardrails, tool calling, and generative response synthesis.
    """
    sid = request.session_id or str(uuid.uuid4())
    try:
        result = langchain_agent.process_message(
            message=request.message,
            session_id=sid,
            force_mock=request.force_mock
        )
        return ChatResponse(
            response=result["response"],
            session_id=result["session_id"],
            tools_used=result["tools_used"],
            guardrail_triggered=result["guardrail_triggered"],
            guardrail_reason=result.get("guardrail_reason")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar mensagem: {str(e)}")

@router.get("/chat/history/{session_id}")
def get_chat_history(session_id: str):
    """Retrieve full conversation history for a given session."""
    history = message_store.get_history(session_id)
    return {"session_id": session_id, "messages": history}

@router.delete("/chat/history/{session_id}")
def clear_chat_history(session_id: str):
    """Reset / clear memory for a session."""
    message_store.clear_session(session_id)
    return {"session_id": session_id, "cleared": True}

@router.get("/catalog")
def get_catalog(
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    query: Optional[str] = None,
    limit: int = 20
):
    """Search and browse instruments in the store catalog."""
    products = search_products(
        query=query,
        category_name=category,
        max_price=max_price,
        limit=limit
    )
    return {"total": len(products), "products": products}

@router.get("/catalog/{name_or_id}")
def get_catalog_item(name_or_id: str):
    """Get single product details."""
    prod = get_product_details(name_or_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return prod

@router.get("/policies")
def get_policies_endpoint():
    """Retrieve all store policies."""
    return get_all_policies()

