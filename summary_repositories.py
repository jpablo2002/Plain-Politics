from os import link
import mysql.connector

mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

def get_links() -> list:
    statement1 = 'SELECT * FROM BILLCOMMITIES'
    cursor = mydb.cursor()
    cursor.execute(statement1)
    result = cursor.fetchall()
    links = []
    for row in result:
        links.append((row[0], row[3]))

    return links

def insert_to_table2(item: tuple) -> None:
    stmt = "INSERT INTO categories (id, categories) VALUES (%s, %s);"
    cursor = mydb.cursor()
    val = (item[0], item[1])
    cursor.execute(stmt, val)
    mydb.commit()





    


