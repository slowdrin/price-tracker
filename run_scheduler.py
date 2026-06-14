import json
import re
import time
from apscheduler.schedulers.blocking import BlockingScheduler

from scraper import get_product_info
from db import init_db, save_price, get_last_price
from notifier import send_alert


def parse_price(price_str: str) -> float:
    match = re.search(r"[\d.]+", price_str.replace(",", ""))
    return float(match.group()) if match else None


def check_prices():
    print(f"\n--- Checking prices at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")

    with open("products.json", "r") as f:
        products = json.load(f)

    for product in products:
        url = product["url"]
        target_price = product["target_price"]

        try:
            info = get_product_info(url)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            continue

        print("Scraped:", info)
        current_price = parse_price(info["price"])

        last = get_last_price(url)
        if last:
            print("Previous price:", last[0], "at", last[1])

        save_price(info["title"], url, info["price"])

        if current_price is not None and current_price <= target_price:
            subject = f"Price Alert: {info['title'][:50]}"
            body = (
                f"Price dropped to {info['price']} (target was {target_price})\n\n"
                f"{url}"
            )
            send_alert(subject, body)
        else:
            print(f"No alert: {current_price} > target {target_price}")


if __name__ == "__main__":
    init_db()

    # Run once immediately on startup
    check_prices()

    scheduler = BlockingScheduler()
    # Run every 6 hours - change as needed
    scheduler.add_job(check_prices, "interval", hours=6)

    print("\nScheduler started. Checking every 6 hours. Press Ctrl+C to stop.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")