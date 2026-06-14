from scraper import get_product_info
from db import init_db, save_price, get_last_price

PRODUCT_URL = "https://www.aliexpress.com/item/1005008473303705.html"

if __name__ == "__main__":
    init_db()

    info = get_product_info(PRODUCT_URL)
    print("Scraped:", info)

    last = get_last_price(PRODUCT_URL)
    if last:
        print("Previous price:", last[0], "at", last[1])
    else:
        print("No previous price recorded.")

    save_price(info["title"], PRODUCT_URL, info["price"])
    print("Saved current price to database.")