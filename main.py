import json
import re
from scraper import get_product_info
from db import init_db, save_price, get_last_price
from notifier import send_alert


def parse_price(price_str: str) -> float:
    """Extract numeric value from a price string like 'MAD199.90'."""
    match = re.search(r"[\d.]+", price_str.replace(",", ""))
    return float(match.group()) if match else None


if __name__ == "__main__":
    init_db()

    with open("products.json", "r") as f:
        products = json.load(f)

    for product in products:
        url = product["url"]
        target_price = product["target_price"]

        info = get_product_info(url)
        print("Scraped:", info)

        current_price = parse_price(info["price"])

        last = get_last_price(url)
        if last:
            print("Previous price:", last[0], "at", last[1])
        else:
            print("No previous price recorded.")

        save_price(info["title"], url, info["price"])
        print("Saved current price to database.")

        if current_price is not None and current_price <= target_price:
            subject = f"Price Alert: {info['title'][:50]}"
            body = (
                f"Price dropped to {info['price']} (target was {target_price})\n\n"
                f"{url}"
            )
            send_alert(subject, body)
        else:
            print(f"No alert: {current_price} > target {target_price}")