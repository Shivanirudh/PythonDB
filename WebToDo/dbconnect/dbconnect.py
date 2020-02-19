import mysql.connector

def connection():
    conn = mysql.connector.connect(host="localhost",
                           user = "root",
                           passwd = "$$Shiva123",
                           db = "sample")
    c = conn.cursor()

    return c, conn