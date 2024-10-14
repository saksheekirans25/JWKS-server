#Sakshee Kiran Shrestha
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import base64

app = Flask(__name__)

# Generating RSA keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

def base64_url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

# Using a consistent 'kid' value
kid_value = "my-key-id"

# Storing keys for JWKS with expiry
keys = [{
    "kty": "RSA",
    "kid": kid_value,
    "n": base64_url_encode(public_key.public_numbers().n.to_bytes(256, 'big')),
    "e": base64_url_encode(public_key.public_numbers().e.to_bytes(3, 'big')),
    "expiry": (datetime.utcnow() + timedelta(days=365)).isoformat()  # Future expiry for valid key
}]

# Function to check if a key is expired
def is_key_expired(key):
    expiry = datetime.fromisoformat(key['expiry'])
    return expiry < datetime.utcnow()

@app.route('/.well-known/jwks.json', methods=['GET'])
def get_jwks():
    # Only return non-expired keys in the JWKS response
    non_expired_keys = [key for key in keys if not is_key_expired(key)]
    return jsonify({"keys": non_expired_keys})

@app.route('/auth', methods=['POST'])
def authenticate():
    user_id = "example_user"  # Mock user ID
    expired = request.args.get('expired')  # Check for 'expired' query parameter

    if keys:
        current_key = keys[-1]  # Get the latest key

        # Set expiration time for JWT (expired if 'expired=true')
        exp_time = datetime.utcnow() - timedelta(hours=1) if expired == 'true' else datetime.utcnow() + timedelta(hours=1)

        # Create the JWT token
        token = jwt.encode(
            {"user_id": user_id, "exp": exp_time, "kid": current_key['kid']},
            private_key,
            algorithm='RS256',
            headers={"kid": current_key['kid']}  # Add 'kid' to the JWT header
        )
        return jsonify({"token": token})  # JSON response with the token
    return jsonify({"error": "No keys available"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
