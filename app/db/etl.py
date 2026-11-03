"""ETL and Data Treatment Module for Empório da Música.

Performs robust cleaning, normalization, type casting, and validation
across the 6 operational CSVs and the policies manual.
"""

import os
import csv
import glob
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import unicodedata

logger = logging.getLogger(__name__)

def normalize_text(text: Optional[str]) -> str:
    """Strip whitespace and normalize Unicode characters."""
    if not text:
        return ""
    text = text.strip()
    return unicodedata.normalize("NFKC", text)

def clean_price(val: Any) -> float:
    """Safely convert price strings/floats to standard float."""
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return round(float(val), 2)
    s = str(val).strip().replace("R$", "").replace(" ", "").replace(",", ".")
    try:
        return round(float(s), 2)
    except (ValueError, TypeError):
        return 0.0

def clean_int(val: Any, default: int = 0) -> int:
    """Safely convert strings/floats to integer."""
    if val is None:
        return default
    try:
        return int(float(str(val).strip()))
    except (ValueError, TypeError):
        return default

def clean_json_specs(specs_str: Optional[str]) -> str:
    """Normalize and validate product specifications JSON string."""
    if not specs_str or not specs_str.strip():
        return "{}"
    try:
        parsed = json.loads(specs_str)
        if isinstance(parsed, dict):
            # Clean keys and values
            cleaned = {normalize_text(k): normalize_text(str(v)) for k, v in parsed.items()}
            return json.dumps(cleaned, ensure_ascii=False)
        return "{}"
    except Exception:
        return "{}"

class DataPipeline:
    """Processes, cleans, and validates all CSV operational data."""

    @staticmethod
    def process_categories(file_path: str) -> List[Dict[str, Any]]:
        cleaned = []
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for r in reader:
                cleaned.append({
                    "category_id": clean_int(r.get("category_id")),
                    "name": normalize_text(r.get("name")),
                    "description": normalize_text(r.get("description"))
                })
        return cleaned

    @staticmethod
    def process_customers(file_path: str) -> List[Dict[str, Any]]:
        cleaned = []
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for r in reader:
                phone = normalize_text(r.get("phone"))
                email = normalize_text(r.get("email")).lower()
                cleaned.append({
                    "customer_id": clean_int(r.get("customer_id")),
                    "name": normalize_text(r.get("name")),
                    "phone": phone,
                    "email": email,
                    "city": normalize_text(r.get("city"))
                })
        return cleaned

    @staticmethod
    def process_products(file_path: str) -> List[Dict[str, Any]]:
        cleaned = []
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for r in reader:
                cleaned.append({
                    "product_id": clean_int(r.get("product_id")),
                    "price_brl": clean_price(r.get("price_brl")),
                    "name": normalize_text(r.get("name")),
                    "category_id": clean_int(r.get("category_id")) if r.get("category_id") else None,
                    "description": normalize_text(r.get("description")),
                    "stock_quantity": max(0, clean_int(r.get("stock_quantity"))),
                    "status": normalize_text(r.get("status")).lower() or "active",
                    "specs": clean_json_specs(r.get("specs")),
                    "created_at": normalize_text(r.get("created_at"))
                })
        return cleaned

    @staticmethod
    def process_orders(file_path: str) -> List[Dict[str, Any]]:
        cleaned = []
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for r in reader:
                cleaned.append({
                    "order_id": clean_int(r.get("order_id")),
                    "customer_id": clean_int(r.get("customer_id")),
                    "order_date": normalize_text(r.get("order_date")),
                    "status": normalize_text(r.get("status")).lower(),
                    "total_brl": clean_price(r.get("total_brl")),
                    "payment_method": normalize_text(r.get("payment_method")).lower(),
                    "tracking_code": normalize_text(r.get("tracking_code")).upper(),
                    "estimated_delivery": normalize_text(r.get("estimated_delivery")),
                    "notes": normalize_text(r.get("notes"))
                })
        return cleaned

    @staticmethod
    def process_order_items(file_path: str) -> List[Dict[str, Any]]:
        cleaned = []
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for r in reader:
                cleaned.append({
                    "order_id": clean_int(r.get("order_id")),
                    "quantity": max(1, clean_int(r.get("quantity"), default=1)),
                    "product_id": clean_int(r.get("product_id"))
                })
        return cleaned

    @staticmethod
    def process_promotions(file_path: str) -> List[Dict[str, Any]]:
        cleaned = []
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for r in reader:
                # Store policy explicitly mandates validating if promotion is active (1) or expired (0)
                is_active = clean_int(r.get("is_active"), default=0)
                cleaned.append({
                    "promotion_id": clean_int(r.get("promotion_id")),
                    "product_id": clean_int(r.get("product_id")),
                    "discount_percent": clean_price(r.get("discount_percent")),
                    "description": normalize_text(r.get("description")),
                    "is_active": 1 if is_active == 1 else 0
                })
        return cleaned
