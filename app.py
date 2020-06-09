from flask import Flask, jsonify
from classes import User

app = Flask(__name__)

u1 = User.User("karol", 10)

@app.route('/')
def index():

    data = u1.getAllUsers()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)