import mysql.connector as mysql

def get_conn():
    # ⚠️ ajusta tus credenciales y puerto
    return mysql.connect(
        host="localhost",
        user="root",
        password="root",
        port=3306
    )

def get_conn_db(db="retail_dw"):
    return mysql.connect(
        host="localhost",
        user="root",
        password="root",
        port=3306,
        database=db
    )