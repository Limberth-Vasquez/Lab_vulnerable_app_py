
from flask import Flask, request
import pyodbc

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


@app.route("/")
def home():
    return "Aplicación Vulnerable - SQL Injection Demo"

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    # VULNERABLE A SQL INJECTION
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("Query ejecutado:", query)

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return "Login exitoso"
    else:
        return "Login fallido"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
