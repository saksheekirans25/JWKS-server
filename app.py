from flask import Flask, jsonify

# Create a Flask application
app = Flask(__name__)

# A simple home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the JWKS Server!"})

# Run the app on port 8080
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import time
import json
import base64

# Function to generate a new RSA key pair
def generate_rsa_key_pair():
    # Generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Generate the public key from the private key
    public_key = private_key.public_key()

    # Convert the public key to the JWK format
    public_numbers = public_key.public_numbers()
    e = base64.urlsafe_b64encode(public_numbers.e.to_bytes(3, 'big')).decode('utf-8').rstrip('=')
    n = base64.urlsafe_b64encode(public_numbers.n.to_bytes(256, 'big')).decode('utf-8').rstrip('=')

    # Generate Key ID (kid) based on the current timestamp
    kid = str(int(time.time()))

    # Create the JWK object
    jwk = {
        "kty": "RSA",
        "use": "sig",
        "kid": kid,
        "n": n,
        "e": e,
        "alg": "RS256"
    }

    return private_key, jwk

# Store public keys (JWKs)
jwks_keys = []

# Generate and store an initial key pair
private_key, jwk = generate_rsa_key_pair()
jwks_keys.append(jwk)

# JWKS endpoint to serve the public keys
@app.route('/.well-known/jwks.json')
def jwks():
    return jsonify({"keys": jwks_keys})
