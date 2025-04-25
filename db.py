import pymysql

def get_connection():
    return pymysql.connect(
        host="MySQL-8.0",
        user="root",
        password="",
        database="ex1",
        cursorclass=pymysql.cursors.DictCursor
    )
