from flask import Flask, request
import pyodbc
import re

app = Flask(__name__)

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=db;"
        "DATABASE=vulnerable_db;"
        "UID=sa;"
        "PWD=PasswordSegura123!;"
        "TrustServerCertificate=yes;"
    )
    return conn


def validate_input(value):
    # Solo letras, números y guiones bajos
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, value)

@app.route("/")
def home():
    return "Aplicación SEGURA - SQL Injection Mitigado"

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    # Validación básica
    if not validate_input(username) or not validate_input(password):
        return "Entrada inválida"

    conn = get_connection()
    cursor = conn.cursor()

    # CONSULTA PARAMETRIZADA
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()

    if result:
        return "Login exitoso"
    else:
        return "Login fallido"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

