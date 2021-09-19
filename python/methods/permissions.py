import os
import hashlib
from hmac import compare_digest
import jwt
from dotenv import load_dotenv
from services import connections

load_dotenv() # hook to environment variables

JWT_SECRET = os.getenv("TOKEN_SECRET")

def generate_token(input_username, input_password):
    """
    Gets data for the specified user from DB and compares the stored and encrypted password
    with a newly encoded salted password (generated from user input and stored salt)
    :return: a JWT access token as a string
    """

    user_info = connections.query_user_info(input_username)

    if user_info is None:
        return None

    db_password, db_salt, db_role = user_info

    if verify_login(input_password, db_password, db_salt):
        jwt_token = jwt.encode(
            payload={"role": db_role},
            key = JWT_SECRET,
            algorithm = "HS256"
        )
        return jwt_token
    
    return None


def access_data(auth_token): 
    """
    Verifies that the JWT was created with the given secret and the HS256 alg.
    :return: boolean that indicates whether the user has access 
    """

    try:
        payload = jwt.decode(auth_token, key=JWT_SECRET, algorithms=["HS256", ])
    except jwt.exceptions.InvalidSignatureError:
        return False

    return "role" in payload


def verify_login(input_password, db_password, salt):
    """
    Verifies that login credentials are correct
    :return: boolean (if credentials are valid)
    """
    # Encode password using salt
    salted_password = input_password + salt
    encoded_password = hashlib.sha512(salted_password.encode()).hexdigest()

    return compare_digest(encoded_password, db_password) # will return True if password is correct

