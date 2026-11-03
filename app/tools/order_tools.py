"""Order Tracking and Status Tools for Empório da Música Agent."""

from typing import Dict, Any, Optional, List
from app.db.database import db_manager, DatabaseManager

STATUS_TRANSLATIONS = {
    "delivered": "Entregue ao destinatário",
    "shipped": "Em transporte / Despachado",
    "processing": "Em separação / Processando no centro de distribuição",
    "payment_pending": "Aguardando confirmação de pagamento",
    "canceled": "Pedido cancelado",
    "refunded": "Reembolsado"
}

def get_order_status(
    order_id: Optional[int] = None,
    tracking_code: Optional[str] = None,
    customer_phone_or_email: Optional[str] = None,
    db: Optional[DatabaseManager] = None
) -> Optional[Dict[str, Any]]:
    """
    Check the status and tracking details of a customer order.
    
    Args:
        order_id: The numeric order ID (e.g. 1, 3, 10).
        tracking_code: The tracking code (e.g. 'BRAB1234567BR').
        customer_phone_or_email: Customer's registered email or phone number.
        db: Optional DatabaseManager instance.
    """
    manager = db or db_manager

    if not order_id and not tracking_code and not customer_phone_or_email:
        return {"error": "Por favor, forneça o número do pedido ou o código de rastreamento."}

    sql = """
        SELECT 
            o.order_id,
            o.customer_id,
            c.name AS customer_name,
            c.email AS customer_email,
            c.phone AS customer_phone,
            c.city AS customer_city,
            o.order_date,
            o.status,
            o.total_brl,
            o.payment_method,
            o.tracking_code,
            o.estimated_delivery,
            o.notes
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE 1=1
    """
    params: List[Any] = []

    if order_id is not None:
        sql += " AND o.order_id = ?"
        params.append(int(order_id))
    elif tracking_code:
        sql += " AND o.tracking_code = ?"
        params.append(tracking_code.strip().upper())
    elif customer_phone_or_email:
        clean_input = customer_phone_or_email.strip()
        sql += " AND (c.email = ? OR c.phone = ? OR c.name LIKE ?)"
        params.extend([clean_input, clean_input, f"%{clean_input}%"])

    sql += " ORDER BY o.order_date DESC LIMIT 1"

    with manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        if not row:
            return {"found": False, "message": "Nenhum pedido localizado com os dados informados."}

        order_id_found = row["order_id"]

        # Fetch items
        cursor.execute("""
            SELECT 
                oi.quantity,
                p.product_id,
                p.name AS product_name,
                p.price_brl
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id = ?
        """, [order_id_found])
        items = [
            {
                "product_id": item["product_id"],
                "product_name": item["product_name"],
                "quantity": item["quantity"],
                "unit_price_brl": float(item["price_brl"])
            }
            for item in cursor.fetchall()
        ]

        raw_status = row["status"]
        status_desc = STATUS_TRANSLATIONS.get(raw_status.lower(), raw_status)

        return {
            "found": True,
            "order_id": row["order_id"],
            "customer_name": row["customer_name"],
            "order_date": row["order_date"],
            "status": raw_status,
            "status_description": status_desc,
            "total_brl": float(row["total_brl"]),
            "payment_method": row["payment_method"],
            "tracking_code": row["tracking_code"],
            "estimated_delivery": row["estimated_delivery"],
            "notes": row["notes"],
            "items": items
        }

