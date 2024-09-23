/#Sakshee Kiran Shrestha
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

# Generating RSA keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# Storing keys for JWKS
keys = [{
    "kty": "RSA",
    "kid": "0",
    "n": public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).hex(),
    "e": 65537,
    "expiry": datetime.utcnow() + timedelta(days=365)  
}]

@app.route('/.well-known/jwks.json', methods=['GET'])
def get_jwks():
    return jsonify({"keys": keys})

@app.route('/auth', methods=['POST'])
def authenticate():
    user_id = "example_user"  # Mock user ID
    if keys:
        current_key = keys[-1]  # Get the latest key

        # Validate the JWT token
        # Use the private key directly for signing
        token = jwt.encode(
            {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1), "kid": current_key['kid']},
            private_key,
            algorithm='RS256'
        )
        return jsonify({"token": token}) #JSON response with the token
    return jsonify({"error": "No keys available"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081) #Assign the port to the application.
