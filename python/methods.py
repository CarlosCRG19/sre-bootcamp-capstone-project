import os
import hashlib
import jwt
import connections
from hmac import compare_digest
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("TOKEN_SECRET")

class Token:
    def generate_token(self, input_username, input_password):

        user_info = connections.query_user_info(input_username)

        if user_info == None:
            return None

        db_password, db_salt, db_role = user_info

        if Authorization.verify_login(input_username, input_password, db_password, db_salt):
            jwt_token = jwt.encode(
                payload={"role": db_role},
                key = JWT_SECRET,
                algorithm = "HS256"
            )
            return jwt_token
        else:
            return None


class Restricted:
    def access_data(self, auth_token): 
        """
        Verifies that the JWT was created with the given secret and the HS256 alg.
        :return: string  
        """

        try:
            payload = jwt.decode(auth_token, key=JWT_SECRET, algorithms=["HS256", ])
        except jwt.exceptions.InvalidSignatureError:
            return False

        return "role" in payload

class Authorization:

    @staticmethod
    def verify_login(username, input_password, db_password, salt):
        """
        Verifies that login credentials are correct
        :return: boolean (if credentials are valid)
        """
        # Encode password using salt
        salted_password = input_password + salt
        encoded_password = hashlib.sha512(salted_password.encode()).hexdigest()

        return compare_digest(encoded_password, db_password) # will return True if password is correct

