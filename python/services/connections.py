import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Get environment vars
hostname = os.getenv("DB_ENDPOINT")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

def connect_mysql():
    """
    Returns a connection to the MySQL DB. 
    The connection args are received from env variables
    """

    my_connection = mysql.connector.connect(
        host=hostname,
        user=username,
        passwd=password,
        db=database
    )
    return my_connection

def query_user_info(input_username):
    """
    Gets the user in the DB related to the given username and returns its 
    password, salt and role as a tuple
    """

    connection = connect_mysql()
    cursor = connection.cursor()

    query = f"SELECT password, salt, role FROM users WHERE username='{input_username}'"

    cursor.execute(query)
    user_info = cursor.fetchone() # get only the first one that matches

    cursor.close()
    connection.close()
    
    return user_info
    