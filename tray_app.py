import threading
import webbrowser

import pystray
from PIL import Image, ImageDraw
from apscheduler.schedulers.background import BackgroundScheduler

from api import app
from db import init_db
from tracker import check_all_products

DASHBOARD_URL = "http://127.0.0.1:5000"
CHECK_INTERVAL_HOURS = 6

scheduler = BackgroundScheduler()


def create_icon_image():
    image = Image.new("RGB", (64, 64), "#111111")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((10, 10, 54, 54), radius=10, fill="#4caf50")
    draw.line((22, 42, 30, 34, 38, 38, 46, 24), fill="white", width=5)
    return image


def run_dashboard():
    app.run(port=5000, debug=False, use_reloader=False)


def open_dashboard(icon=None, item=None):
    webbrowser.open(DASHBOARD_URL)


def check_prices_now(icon=None, item=None):
    def worker():
        print("Checking prices from tray...")
        results = check_all_products()
        print(f"Checked {len(results)} product(s).")

    threading.Thread(target=worker, daemon=True).start()


def start_scheduler():
    scheduler.add_job(
        check_all_products,
        "interval",
        hours=CHECK_INTERVAL_HOURS,
        id="price_check",
        replace_existing=True,
    )
    scheduler.start()


def quit_app(icon, item):
    scheduler.shutdown(wait=False)
    icon.stop()


def main():
    init_db()

    threading.Thread(target=run_dashboard, daemon=True).start()
    start_scheduler()

    icon = pystray.Icon(
        "Price Tracker",
        create_icon_image(),
        "Price Tracker",
        menu=pystray.Menu(
            pystray.MenuItem("Open Dashboard", open_dashboard),
            pystray.MenuItem("Check Prices Now", check_prices_now),
            pystray.MenuItem("Quit", quit_app),
        ),
    )
    icon.run()


if __name__ == "__main__":
    main()
