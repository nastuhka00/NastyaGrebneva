import sqlite3
from sqlite3 import Error
import logging

CREATE_DATABASE_QUERY1 = """
CREATE TABLE IF NOT EXISTS lectures (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT NOT NULL,
  theme TEXT NOT NULL,
  number INTEGER NOT NULL,
  text_file TEXT NOT NULL,
  video_file TEXT NOT NULL
);
"""

DROP_DATABASE_QUERY1 = """
DROP TABLE lectures;
"""

logging.basicConfig(level=logging.INFO, filename="logs.log",filemode="a")

def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return conn

def execute_query(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print("Query executed successfully -", query.replace("\n", " "))
        logging.info("Query executed successfully -" + query.replace("\n", " "))
    except Error as e:
        print(query)
        print(f"The error '{e}' occurred")
        logging.info(f"The error '{e}' occurred in '" + query + "'")

def execute_read_query(conn, query):
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        return result
    except Error as e:
        print(query)
        print(f"The error '{e}' occurred")

def INIT(conn):
    """Creating database if not created"""
    print("***********\nDB initialization!\n***********")
    execute_query(conn, CREATE_DATABASE_QUERY1)

def DROP_ALL(conn):
    """Dropping database. Warning, may remove something important"""
    print("***********\nDB dropping!\n***********")
    execute_query(conn, DROP_DATABASE_QUERY1)

def RECREATE(conn):
    """Just... dropping database and creating it again"""
    DROP_ALL(conn)
    INIT(conn)

def load_lecture(conn, subject, theme, number, text_file, video_file):
    """Loading a lecture into database"""
    execute_query(conn, f"INSERT INTO lectures (subject, theme, number, text_file, video_file) VALUES (\"{subject}\", \"{theme}\", {number}, \"{text_file}\", \"{video_file}\")")

def get_lectures(conn, subject):
    """Reading all the lectures with given subject"""
    return execute_read_query(conn, f"SELECT * FROM lectures WHERE subject=\"{subject}\"")

if __name__ == "__main__":
    conn = create_connection("db.db")
    INIT(conn)
    load_lecture(conn, "Математика", "Дифференциальные уравнения", 1, "./say.gex", "..")
    print(get_lectures(conn, "Математика"))