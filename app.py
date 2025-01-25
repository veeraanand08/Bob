from flask import Flask, request, jsonify, redirect
from flask_pymongo import PyMongo
from flask_cors import CORS

# Initialize Flask app and MongoDB connection
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/userDB"
mongo = PyMongo(app)
CORS(app)  # To allow frontend to make requests to this backend

# User collection in MongoDB
users = mongo.db.users

@app.route('/check_user', methods=['POST'])
def check_user():
    # Get user data from frontend
    user_data = request.json
    google_id = user_data.get("googleId")
    email = user_data.get("email")
    name = user_data.get("name")
    
    # Check if the user already exists by googleId
    existing_user = users.find_one({"googleId": google_id})

    if existing_user:
        # If user exists, return that they are existing
        return jsonify({"exists": True})
    else:
        # If user does not exist, create a new user
        new_user = {
            "googleId": google_id,
            "email": email,
            "name": name
        }
        users.insert_one(new_user)
        return jsonify({"exists": False})

if __name__ == "__main__":
    app.run(debug=True)
