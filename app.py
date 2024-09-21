from flask import Flask, jsonify, request
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta

app = Flask(__name__)

# Global keys list
keys = []

# JWKS endpoint
@app.route('/.well-known/jwks.json', methods=['GET'])
def get_jwks():
    current_time = datetime.utcnow().timestamp()
    valid_keys = [key for key in keys if key['expiry'] > current_time]
    return jsonify({'keys': valid_keys})

# Generate and store a key
@app.route('/generate-key', methods=['POST'])
def generate_key():
    try:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        public_key = private_key.public_key()
        
        # Store key info
        key_info = {
            "kid": str(len(keys)),  # Simple key ID based on the number of keys
            "n": public_key.public_numbers().n,
            "e": public_key.public_numbers().e,
            "expiry": (datetime.utcnow() + timedelta(days=365)).timestamp()  # Example expiry
        }
        keys.append(key_info)
        
        return jsonify({"message": "Key generated", "key_id": key_info["kid"]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Authentication endpoint
@app.route('/auth', methods=['POST'])
def authenticate():
    user_id = "example_user"  # Mock user ID

    if keys:
        current_key = keys[-1]  # Get the latest key
        private_key = rsa.PrivateKey(current_key['n'], 65537)  # Use n and e from the current key

        try:
            token = jwt.encode(
                {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1), "kid": current_key['kid']},
                private_key,
                algorithm="RS256"
            )
            return jsonify({"token": token}), 200
        except Exception as e:
            return jsonify({"error": "Failed to generate token", "details": str(e)}), 500
    else:
        return jsonify({"error": "No available keys"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug = True)
