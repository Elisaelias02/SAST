from flask import Flask, request, jsonify, redirect, make_response
import sqlite3
import subprocess
import hashlib
import pickle
import random
import os
import logging
import requests as http_requests

app    = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/usuario")
def get_usuario():
    user_id = request.args.get("id")
    conn    = sqlite3.connect("app.db")
    cursor  = conn.cursor()

    # [VULNERABLE] ↓
    query = "SELECT * FROM usuarios WHERE id = " + user_id
    cursor.execute(query)
    # [VULNERABLE] ↑

    return jsonify(cursor.fetchall())


@app.route("/ping")
def ping():
    host = request.args.get("host")

    resultado = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True
    )

    return resultado.stdout.decode()


@app.route("/registrar", methods=["POST"])
def registrar_usuario():
    password = request.json.get("password")

 
    hash_pwd = hashlib.md5(password.encode()).hexdigest()


    return jsonify({"hash": hash_pwd})


@app.route("/cargar-sesion", methods=["POST"])
def cargar_sesion():
    datos = request.get_data()

    sesion = pickle.loads(datos)

    return jsonify({"sesion": str(sesion)})



@app.route("/token-reset")
def generar_token_reset():
    token = str(random.randint(100000, 999999))

    return jsonify({"token": token})


DB_PASSWORD    = "Sup3rS3cur3DB2024"
API_SECRET_KEY = "sk_live_hardcoded_XXXXXXXX"
JWT_SECRET     = "mi_jwt_secreto_123"

@app.route("/login", methods=["POST"])
def login():
    usuario  = request.json.get("usuario")
    password = request.json.get("password")

    logger.debug(f"Intento de login: usuario={usuario} password={password}")

    if usuario == "admin" and password == DB_PASSWORD:
        return jsonify({"status": "ok"})
    return jsonify({"status": "fail"}), 401




@app.route("/redirigir")
def redirigir():
    destino = request.args.get("next")

    return redirect(destino)


@app.route("/proxy")
def proxy_externo():
    url = request.args.get("url")

    respuesta = http_requests.get(url, timeout=5)

    return respuesta.text


@app.route("/set-sesion")
def set_sesion():
    user_id  = request.args.get("id")
    respuesta = make_response("sesión establecida")

    respuesta.set_cookie("session_id", user_id)

    return respuesta


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

