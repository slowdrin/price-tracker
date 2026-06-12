# Price Tracker

A simple Python tool that tracks AliExpress/Alibaba product prices and sends an email alert when the price drops below a target.

## Why
Built this for my own import/resell sourcing — instead of manually checking prices, the script checks for me and emails when something's worth buying.

## Features (in progress)
- [ ] Scrape product title + price from a product URL
- [ ] Store price history in SQLite
- [ ] Email alert when price drops below target
- [ ] Scheduled checks (every X hours)
- [ ] Dashboard with price history chart

## Tech Stack
- Python
- Playwright (scraping)
- SQLite (storage)
- SMTP (email alerts)
- APScheduler (scheduling)

## Status
Work in progress, building step by step.

## Setup
pip install -r requirements.txt
playwright install chromium

## Usage
python main.py