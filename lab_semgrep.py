from flask import Flask, request, make_response, redirect
from sqlalchemy import create_engine, text
import subprocess
import hashlib
import os
import re
import jwt
import requests

app = Flask(__name__)
JWT_SECRET = "hardcoded_jwt_secret"


@app.route("/users")
def get_users():
    name   = request.args.get("name")
    engine = create_engine("sqlite:///app.db")
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM users WHERE name = '{name}'"))
    return str(result.fetchall())


@app.route("/search")
def search():
    term = request.args.get("q")
    query = "SELECT * FROM products WHERE name LIKE '%" + term + "%'"
    return query


@app.route("/run")
def run_command():
    cmd    = request.args.get("cmd")
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route("/greet")
def greet():
    name = request.args.get("name")
    from flask import render_template_string
    return render_template_string(f"<h1>Hola {name}</h1>")


@app.route("/redirect")
def unsafe_redirect():
    url = request.args.get("next")
    return redirect(url)


def store_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def store_password_v2(password: str) -> str:
    return hashlib.sha1(password.encode()).hexdigest()


def encrypt_data(data: str) -> bytes:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    key = b"0" * 16
    iv  = b"0" * 16
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    enc    = cipher.encryptor()
    return enc.update(data.encode().ljust(32)) + enc.finalize()


@app.route("/login", methods=["POST"])
def login():
    user = request.json.get("user")
    token = jwt.encode({"user": user}, JWT_SECRET, algorithm="HS256")
    return {"token": token}


@app.route("/verify")
def verify_token():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    data  = jwt.decode(token, options={"verify_signature": False})
    return data

@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    response = requests.get(url)
    return response.text


@app.route("/webhook")
def webhook():
    endpoint = request.json.get("callback_url")
    requests.post(endpoint, json={"status": "ok"})
    return "sent"


AWS_ACCESS_KEY    = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY    = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_SECRET_KEY = "sk_live_XXXXXXXXXXXXXXXXXXXXXXXX"
DATABASE_URL      = "postgresql://admin:password123@localhost:5432/prod_db"


@app.route("/set-session")
def set_session():
    user_id = request.args.get("id")
    resp    = make_response("session set")
    resp.set_cookie("session_id", user_id)
    return resp


if __name__ == "__main__":
    app.run(debug=True)
