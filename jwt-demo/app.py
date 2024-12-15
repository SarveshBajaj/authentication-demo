from flask import Flask, jsonify, request
from auth import token_required
import jwt
import datetime
from config import SECRET_KEY

app = Flask(__name__)

# Public endpoint for generating a JWT
@app.route('/generate-token', methods=['POST'])
def generate_token():
    data = request.json
    if not data or 'username' not in data:
        return jsonify({'message': 'Invalid request!'}), 400
    
    payload = {
        'username': data['username'],  # Example user data
        'role': data.get('role', 'user'),  # Optional
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)  # Token expiry
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token})

# Protected endpoint using the token_required decorator
@app.route('/secure-data', methods=['GET'])
@token_required
def secure_data():
    # Access user data attached by the middleware
    user = getattr(request, 'user', {})
    return jsonify({'message': 'This is secured data', 'user': user})

if __name__ == '__main__':
    app.run(debug=True)
