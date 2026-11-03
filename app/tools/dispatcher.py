"""Tool Dispatcher for executing agent function calls."""

import json
import logging
from typing import Dict, Any, Optional
from app.db.database import DatabaseManager
from app.tools.catalog_tools import search_products, get_product_details, list_promotions
from app.tools.order_tools import get_order_status
from app.tools.policy_tools import get_store_policies

logger = logging.getLogger(__name__)

class ToolDispatcher:
    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any] | str) -> Dict[str, Any]:
        """Execute a tool with given parameters and return structured result."""
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments) if arguments.strip() else {}
            except Exception as e:
                logger.error("Failed to parse tool arguments: %s", e)
                return {"error": f"Invalid JSON arguments: {str(e)}"}

        logger.info("Executing tool '%s' with args %s", tool_name, arguments)

        try:
            if tool_name == "search_products":
                return {
                    "results": search_products(
                        query=arguments.get("query"),
                        category_name=arguments.get("category_name"),
                        max_price=arguments.get("max_price"),
                        min_price=arguments.get("min_price"),
                        in_stock_only=arguments.get("in_stock_only", True),
                        limit=arguments.get("limit", 5),
                        db=self.db
                    )
                }

            elif tool_name == "get_product_details":
                name_or_id = arguments.get("name_or_id") or arguments.get("product_id") or arguments.get("name")
                if not name_or_id:
                    return {"error": "name_or_id is required"}
                result = get_product_details(str(name_or_id), db=self.db)
                if not result:
                    return {"found": False, "message": f"Instrumento '{name_or_id}' não encontrado no catálogo."}
                return {"found": True, "product": result}

            elif tool_name == "check_order_status":
                return get_order_status(
                    order_id=arguments.get("order_id"),
                    tracking_code=arguments.get("tracking_code"),
                    customer_phone_or_email=arguments.get("customer_phone_or_email"),
                    db=self.db
                )

            elif tool_name == "list_promotions":
                return {
                    "promotions": list_promotions(
                        active_only=arguments.get("active_only", True),
                        db=self.db
                    )
                }

            elif tool_name == "get_store_policies":
                topic = arguments.get("topic_or_query") or arguments.get("topic") or arguments.get("query", "")
                return get_store_policies(topic)

            else:
                return {"error": f"Tool '{tool_name}' is not recognized."}

        except Exception as e:
            logger.exception("Error executing tool %s: %s", tool_name, e)
            return {"error": f"Erro ao executar ferramenta {tool_name}: {str(e)}"}

tool_dispatcher = ToolDispatcher()

