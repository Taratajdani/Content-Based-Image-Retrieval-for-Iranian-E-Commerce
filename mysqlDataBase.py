import mysql.connector
from urllib.parse import quote

password = "Ta@1382TD!"
encoded_password = quote(password)
DATABASE_URL = f"mysql+mysqlconnector://root:{encoded_password}@127.0.0.1/ecommerce_search"
def get_db_connection():
    connection = mysql.connector.connect(
    user="root",
    password=password,
    host="127.0.0.1",
    database="ecommerce_search"
    )
    return connection
import sqlite3

def create_session_db():
    conn = sqlite3.connect('session.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        uploaded_image BLOB,
                        search_results TEXT)''')
    conn.commit()

def store_session_data(session_id, uploaded_image, search_results):
    conn = sqlite3.connect('session.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO sessions (session_id, uploaded_image, search_results)
                      VALUES (?, ?, ?)''', (session_id, uploaded_image, search_results))
    conn.commit()

def clear_session_data(session_id):
    conn = sqlite3.connect('session.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
    conn.commit()
