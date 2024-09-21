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

