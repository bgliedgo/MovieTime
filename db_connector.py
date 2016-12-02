import mysql.connector

def append_row(call, data):
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    print("\nExecuting: " + call + '\n')
    cursor.execute(call, data)
    cnx.commit()
    cnx.close()

def query_db(query):
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    print("\nExecuting: " + query + '\n')
    cursor.execute(query)
    query_set = cursor.fetchall()
    cnx.close()
    return query_set

def query_db_param(query, data):
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    print("\nExecuting: " + query + '\n')
    cursor.execute(query, data)
    query_set = cursor.fetchall()
    cnx.close()
    return query_set
