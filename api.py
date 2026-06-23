from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from db import init_db, get_last_price, get_history
from tracker import load_products, save_products, check_all_products

app = Flask(__name__)
CORS(app)

init_db()


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/products", methods=["GET"])
def get_products():
    products = load_products()

    for product in products:
        last = get_last_price(product["url"])
        if last:
            product["last_price"] = last[0]
            product["last_checked"] = last[1]
        else:
            product["last_price"] = None
            product["last_checked"] = None

    return jsonify(products)


@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    url = data.get("url")
    target_price = data.get("target_price")
    name = data.get("name", "")

    if not url or target_price is None:
        return jsonify({"error": "url and target_price required"}), 400

    products = load_products()

    for product in products:
        if product["url"] == url:
            return jsonify({"error": "Product already tracked"}), 409

    new_product = {
        "name": name or "Unknown Product",
        "url": url,
        "target_price": float(target_price)
    }

    products.append(new_product)
    save_products(products)

    return jsonify(new_product), 201


@app.route("/api/products/<int:index>", methods=["DELETE"])
def remove_product(index):
    products = load_products()

    if index < 0 or index >= len(products):
        return jsonify({"error": "Product not found"}), 404

    removed = products.pop(index)
    save_products(products)

    return jsonify({"removed": removed})


@app.route("/api/history", methods=["GET"])
def product_history():
    url = request.args.get("url")

    if not url:
        return jsonify({"error": "url is required"}), 400

    return jsonify(get_history(url))


@app.route("/api/check", methods=["POST"])
def check_now():
    results = check_all_products()
    return jsonify(results)


if __name__ == "__main__":
    app.run(port=5000, debug=True)