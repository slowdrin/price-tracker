import json
import re
import time

from scraper import get_product_info
from db import init_db, save_price, get_last_price
from notifier import send_alert

PRODUCTS_FILE = "products.json"


def parse_price(price_str: str) -> float:
    match = re.search(r"[\d.]+", price_str.replace(",", ""))
    return float(match.group()) if match else None


def load_products():
    with open(PRODUCTS_FILE, "r") as f:
        return json.load(f)


def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=2)


def check_product(product):
    url = product["url"]
    target_price = product["target_price"]

    info = get_product_info(url)
    current_price = parse_price(info["price"])

    last = get_last_price(url)
    save_price(info["title"], url, info["price"])

    alert_sent = False
    if current_price is not None and current_price <= target_price:
        subject = f"Price Alert: {info['title'][:50]}"
        body = (
            f"Price dropped to {info['price']} (target was {target_price})\n\n"
            f"{url}"
        )
        send_alert(subject, body)
        alert_sent = True

    return {
        "name": product.get("name", info["title"]),
        "url": url,
        "title": info["title"],
        "price": info["price"],
        "current_price": current_price,
        "target_price": target_price,
        "previous_price": last[0] if last else None,
        "previous_checked_at": last[1] if last else None,
        "alert_sent": alert_sent,
        "checked_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


def check_all_products():
    products = load_products()
    results = []
    for product in products:
        try:
            result = check_product(product)
        except Exception as e:
            result = {"url": product["url"], "error": str(e)}
        results.append(result)
    return results