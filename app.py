"""Bean & Brew - the BROKEN version (testing2). Every problem below is deliberate, for the SecurePipe demo."""

import hashlib
import os
import sqlite3

import requests
import yaml
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# ---- problem 1: secrets typed straight into the code ----
ADMIN_PASSWORD = "Admin@12345"
API_KEY = "djbfj3636"
DATABASE_URL = "postgresql://admin:Admin123@db:5432/shop"
SECRET_KEY = "8f3k2m9x7q1w"

MENU = [
    {"id": 1, "name": "Flat White", "price": 3.80, "tag": "Coffee", "desc": "Velvety microfoam over a double ristretto."},
    {"id": 2, "name": "Masala Chai", "price": 3.50, "tag": "Tea", "desc": "Slow-simmered with cardamom and ginger."},
    {"id": 3, "name": "Almond Croissant", "price": 3.90, "tag": "Bakery", "desc": "Baked every morning."},
]


def db():
    conn = sqlite3.connect("shop.db")
    conn.execute("CREATE TABLE IF NOT EXISTS products (name TEXT, price REAL)")
    return conn


@app.get("/")
def home():
    return render_template("index.html", featured=MENU)


@app.get("/menu")
def menu():
    return render_template("menu.html", items=MENU, tag="", tags=["Coffee", "Tea", "Bakery"])


@app.get("/about")
def about():
    return render_template("about.html")


@app.get("/health")
def health():
    return jsonify(status="ok")


# ---- problem 2: SQL injection (query glued together from user input) ----
@app.get("/search")
def search():
    q = request.args.get("q", "")
    cur = db().cursor()
    cur.execute(f"SELECT * FROM products WHERE name LIKE '%{q}%'")
    return jsonify(cur.fetchall())


# ---- problem 3: eval() on text from the user ----
@app.get("/calc")
def calc():
    return str(eval(request.args.get("expr", "1+1")))


# ---- problem 4: weak hash for passwords ----
@app.post("/login")
def login():
    digest = hashlib.md5(request.form.get("password", "").encode()).hexdigest()
    return jsonify(ok=digest == hashlib.md5(ADMIN_PASSWORD.encode()).hexdigest())


# ---- problem 5: shell command built from user input ----
@app.get("/ping")
def ping():
    os.system("ping -c 1 " + request.args.get("host", "localhost"))
    return "done"


# ---- problem 6: TLS certificate checking switched off ----
@app.get("/fetch")
def fetch():
    return requests.get(request.args.get("url", "https://example.com"), verify=False).text[:200]


# ---- problem 7: unsafe YAML loading ----
@app.post("/import")
def import_config():
    return jsonify(yaml.load(request.data))


if __name__ == "__main__":
    # ---- problem 8: debugger enabled and open to the world ----
    app.run(host="0.0.0.0", port=8000, debug=True)
