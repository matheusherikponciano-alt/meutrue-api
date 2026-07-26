import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def conectar():
    print("HOST:", os.getenv("DB_HOST"))
    print("PORT:", os.getenv("DB_PORT"))
    print("USER:", os.getenv("DB_USER"))
    print("DB:", os.getenv("DB_NAME"))
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )