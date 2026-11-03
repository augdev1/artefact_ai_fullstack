"""Store Policies Retrieval Tool."""

from typing import Dict, Any, List
from app.knowledge.policies import query_policies, STORE_POLICIES

def get_store_policies(topic_or_query: str) -> Dict[str, Any]:
    """
    Consult internal store policies and procedures manual.
    Use this for questions about:
    - Store address, location, telephone, email
    - Opening and closing hours, weekend operations
    - Return and exchange rules, 7-day remorse window (CDC), 30-day defects
    - Shipping fees, delivery timeframes (Campo Grande motoboy vs Correios/Jadlog)
    - Payment options, PIX 5% discount, credit card installments (up to 12x)
    - Warranty (90-day legal CDC vs manufacturer)
    - Store scope (explaining that the store sells only instruments, not accessories)
    """
    matches = query_policies(topic_or_query, max_results=2)
    return {
        "query": topic_or_query,
        "matched_policies": matches
    }

