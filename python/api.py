from flask import *   
from convert import *  
from methods import *  
from convert import *

app = Flask(__name__)
login = Token()
protected = Restricted()
convert = CidrMaskConvert()
validate = IpValidate()

# Just a health check
@app.route("/")
def urlRoot():  
    return "OK"

# Just a health check
@app.route("/_health")
def urlHealth():
    return "OK"  

# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def urlLogin():
    
    username = request.form['username']
    password = request.form['password']
    
    res = {
        "data": login.generate_token(username, password)
    }
    
    return jsonify(res)

# e.g. http://127.0.0.1:8000/cidr-to-mask?value=8
@app.route("/cidr-to-mask")
def urlCidrToMask():
    username = request.headers.get('Authorization')
    if not protected.access_Data(username):
        abort(401)   
    val = request.args.get('value')
    r = {"function": "cidrToMask","input": val,"output": convert.cidr_to_mask(val), }
    return jsonify(r)  

# # e.g. http://127.0.0.1:8000/mask-to-cidr?value=255.0.0.0
@app.route("/mask-to-cidr")
def urlMaskToCidr():  
    username = request.headers.get('Authorization')
    if not protected.access_Data(username):
        abort(401) 
    val = request.args.get('value')
    r = { "function": "maskToCidr","input": val,"output": convert.mask_to_cidr(val),}
    return jsonify(r)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

