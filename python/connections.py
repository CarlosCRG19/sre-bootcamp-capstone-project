import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

hostname = os.getenv("DB_ENDPOINT")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

def connect_mysql():
    my_connection = mysql.connector.connect(
        host=hostname,
        user=username,
        passwd=password,
        db=database
    )
    return my_connection

def query_user_info(input_username):

    connection = connect_mysql()
    cursor = connection.cursor()

    query = f"SELECT password, salt, role FROM users WHERE username='{input_username}'"
    print(query)

    cursor.execute(query)
    user_info = cursor.fetchone()
    print(user_info)

    cursor.close()
    connection.close()
    
    return user_info
    