from playwright.sync_api import sync_playwright


def get_product_info(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector(".price-default--current--F8OlYIo", timeout=30000)

        title = page.title()
        price_el = page.query_selector(".price-default--current--F8OlYIo")
        price = price_el.inner_text() if price_el else None

        browser.close()

    return {"title": title, "price": price}


if __name__ == "__main__":
    test_url = "https://www.aliexpress.com/item/1005008473303705.html"
    info = get_product_info(test_url)
    print(info)