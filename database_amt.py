import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def conectar_amt():
    return mysql.connector.connect(
        host=os.getenv("AMT_DB_HOST"),
        port=int(os.getenv("AMT_DB_PORT")),
        user=os.getenv("AMT_DB_USER"),
        password=os.getenv("AMT_DB_PASSWORD"),
        database=os.getenv("AMT_DB_NAME")
    )