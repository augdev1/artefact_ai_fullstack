"""Product Catalog Tools for Empório da Música Agent."""

import json
from typing import List, Dict, Any, Optional
from app.db.database import db_manager, DatabaseManager

def search_products(
    query: Optional[str] = None,
    category_name: Optional[str] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    in_stock_only: bool = True,
    limit: int = 5,
    db: Optional[DatabaseManager] = None
) -> List[Dict[str, Any]]:
    """
    Search for musical instruments in the store catalog.
    
    Args:
        query: Keywords to search in product name or description (e.g. 'violão', 'Takamine', 'Yamaha', 'bateria').
        category_name: Filter by category (e.g. 'Violões', 'Guitarras', 'Baixos', 'Baterias e Percussão', 'Teclados e Pianos').
        max_price: Maximum price filter in BRL (e.g. 1000.0).
        min_price: Minimum price filter in BRL.
        in_stock_only: If True, returns only products with stock_quantity > 0.
        limit: Maximum number of products to return (default 5).
        db: Optional DatabaseManager instance (uses default if None).
    """
    manager = db or db_manager
    sql = """
        SELECT 
            p.product_id,
            p.name,
            c.name AS category,
            p.price_brl,
            p.stock_quantity,
            p.description,
            p.specs,
            pr.discount_percent,
            pr.is_active AS promo_is_active,
            pr.description AS promo_description
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN promotions pr ON p.product_id = pr.product_id AND pr.is_active = 1
        WHERE p.status = 'active'
    """
    params: List[Any] = []

    if in_stock_only:
        sql += " AND p.stock_quantity > 0"

    if max_price is not None:
        sql += " AND p.price_brl <= ?"
        params.append(float(max_price))

    if min_price is not None:
        sql += " AND p.price_brl >= ?"
        params.append(float(min_price))

    if category_name:
        sql += " AND c.name LIKE ?"
        params.append(f"%{category_name.strip()}%")

    if query:
        terms = [t.strip() for t in query.split() if len(t.strip()) > 1]
        for term in terms:
            sql += " AND (p.name LIKE ? OR p.description LIKE ? OR c.name LIKE ?)"
            params.extend([f"%{term}%", f"%{term}%", f"%{term}%"])

    sql += " ORDER BY p.price_brl ASC LIMIT ?"
    params.append(limit)

    results = []
    with manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        for r in rows:
            original_price = float(r["price_brl"])
            promo_discount = float(r["discount_percent"]) if r["promo_is_active"] else 0.0
            
            if promo_discount > 0:
                final_price = round(original_price * (1 - promo_discount / 100.0), 2)
                pix_price = final_price  # Store policy: PIX 5% discount does NOT stack with promotion
                has_promo = True
            else:
                final_price = original_price
                pix_price = round(original_price * 0.95, 2)  # 5% PIX discount on regular price
                has_promo = False

            try:
                specs_dict = json.loads(r["specs"]) if r["specs"] else {}
            except Exception:
                specs_dict = {}

            results.append({
                "product_id": r["product_id"],
                "name": r["name"],
                "category": r["category"],
                "original_price_brl": original_price,
                "current_price_brl": final_price,
                "pix_price_brl": pix_price,
                "in_promotion": has_promo,
                "promotion_discount_percent": promo_discount if has_promo else None,
                "promotion_campaign": r["promo_description"] if has_promo else None,
                "stock_quantity": r["stock_quantity"],
                "in_stock": r["stock_quantity"] > 0,
                "description": r["description"],
                "specs": specs_dict
            })

    return results


def get_product_details(name_or_id: str, db: Optional[DatabaseManager] = None) -> Optional[Dict[str, Any]]:
    """
    Get detailed information for a specific product by name or ID.
    
    Args:
        name_or_id: Product name (e.g. 'Takamine GD20', 'Yamaha C40') or integer product_id.
        db: Optional DatabaseManager instance.
    """
    manager = db or db_manager
    query_str = str(name_or_id).strip()

    sql = """
        SELECT 
            p.product_id,
            p.name,
            c.name AS category,
            p.price_brl,
            p.stock_quantity,
            p.description,
            p.specs,
            pr.discount_percent,
            pr.is_active AS promo_is_active,
            pr.description AS promo_description
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN promotions pr ON p.product_id = pr.product_id AND pr.is_active = 1
        WHERE p.status = 'active'
    """
    params: List[Any] = []

    if query_str.isdigit():
        sql += " AND p.product_id = ?"
        params.append(int(query_str))
    else:
        sql += " AND (p.name LIKE ? OR p.name LIKE ?)"
        params.extend([f"{query_str}%", f"%{query_str}%"])

    sql += " LIMIT 1"

    with manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        r = cursor.fetchone()
        if not r:
            return None

        original_price = float(r["price_brl"])
        promo_discount = float(r["discount_percent"]) if r["promo_is_active"] else 0.0

        if promo_discount > 0:
            final_price = round(original_price * (1 - promo_discount / 100.0), 2)
            pix_price = final_price
            has_promo = True
        else:
            final_price = original_price
            pix_price = round(original_price * 0.95, 2)
            has_promo = False

        try:
            specs_dict = json.loads(r["specs"]) if r["specs"] else {}
        except Exception:
            specs_dict = {}

        return {
            "product_id": r["product_id"],
            "name": r["name"],
            "category": r["category"],
            "original_price_brl": original_price,
            "current_price_brl": final_price,
            "pix_price_brl": pix_price,
            "in_promotion": has_promo,
            "promotion_discount_percent": promo_discount if has_promo else None,
            "promotion_campaign": r["promo_description"] if has_promo else None,
            "stock_quantity": r["stock_quantity"],
            "in_stock": r["stock_quantity"] > 0,
            "description": r["description"],
            "specs": specs_dict,
            "installment_options": {
                "max_installments": 12,
                "installment_value": round(final_price / 12, 2),
                "interest_free": True,
                "min_installment_brl": 100.0
            }
        }


def list_promotions(active_only: bool = True, db: Optional[DatabaseManager] = None) -> List[Dict[str, Any]]:
    """
    List all promotions currently registered in the store system.
    
    Args:
        active_only: If True, returns only active promotions (is_active = 1).
        db: Optional DatabaseManager instance.
    """
    manager = db or db_manager
    sql = """
        SELECT 
            pr.promotion_id,
            pr.product_id,
            p.name AS product_name,
            c.name AS category,
            p.price_brl AS original_price,
            pr.discount_percent,
            pr.description,
            pr.is_active,
            p.stock_quantity
        FROM promotions pr
        JOIN products p ON pr.product_id = p.product_id
        LEFT JOIN categories c ON p.category_id = c.category_id
    """
    params: List[Any] = []
    if active_only:
        sql += " WHERE pr.is_active = 1"

    sql += " ORDER BY pr.discount_percent DESC"

    with manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        results = []
        for r in rows:
            orig = float(r["original_price"])
            disc = float(r["discount_percent"])
            promo_price = round(orig * (1 - disc / 100.0), 2)
            results.append({
                "promotion_id": r["promotion_id"],
                "product_id": r["product_id"],
                "product_name": r["product_name"],
                "category": r["category"],
                "original_price_brl": orig,
                "discount_percent": disc,
                "promotional_price_brl": promo_price,
                "campaign_description": r["description"],
                "is_active": bool(r["is_active"]),
                "in_stock": r["stock_quantity"] > 0,
                "stock_quantity": r["stock_quantity"]
            })
        return results

