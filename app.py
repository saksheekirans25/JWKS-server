from flask import Flask, jsonify
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt

app = Flask(__name__)

# Global variable to store keys
keys = []

# Key generation function
def generate_key():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    kid = str(len(keys))  # Simple kid generation
    expiry = datetime.utcnow() + timedelta(days=1)  # Key expiry time
    keys.append({
        'kid': kid,
        'n': public_key.public_numbers().n,
        'e': public_key.public_numbers().e,
        'expiry': expiry.timestamp()  # Store expiry as timestamp
    })

# JWKS endpoint
@app.route('/.well-known/jwks.json', methods=['GET'])
def get_jwks():
    current_time = datetime.utcnow().timestamp()
    valid_keys = [key for key in keys if key['expiry'] > current_time]
    print(f"Current time: {current_time}, Valid keys: {valid_keys}")  # Debugging line
    return jsonify({'keys': valid_keys})

if __name__ == '__main__':
    generate_key()  # Generate at least one key at startup
    app.run(host='0.0.0.0', port=8081)
