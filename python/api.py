from flask import Flask, abort, jsonify, request 
from methods import permissions, conversions

app = Flask(__name__)

def authorize_and_convert(authorization, value, iscidr=True):
    """
    Validates the credentials and proceeds to the conversion of
    input value.
    :return: a dictionary indicating input and output values as well as wheter 
    it was a Cidr to Mask conversion or viceversa
    """
    auth_token = str.replace(str(authorization), "Bearer ", "")

    if not permissions.access_data(auth_token):
        abort(401)   

    return conversions.cidr_mask_conversion_handler(value, iscidr)

# Just a health check
@app.route("/")
def url_root():  
    return "OK"

# Just a health check
@app.route("/_health")
def url_health():
    return "OK"  

# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def url_login():
    username = request.form['username']
    password = request.form['password']
    
    res = {
        "data": permissions.generate_token(username, password)
    }
    
    return jsonify(res)

# e.g. http://127.0.0.1:8000/cidr-to-mask?value=8
@app.route("/cidr-to-mask")
def url_cidr_to_mask():
    authorization = request.headers.get('Authorization')
    cidr = request.args.get('value')
    
    res = authorize_and_convert(authorization, cidr)
    return jsonify(res)
    
# # e.g. http://127.0.0.1:8000/mask-to-cidr?value=255.0.0.0
@app.route("/mask-to-cidr")
def url_mask_to_cidr():  
    authorization = request.headers.get('Authorization')
    mask = request.args.get('value')

    res = authorize_and_convert(authorization, mask, False)
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

