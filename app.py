from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["HealthCareSystem"]
user_table = db["Users"]

@app.route('/')
def home():
    return render_template('login_dbms.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = user_table.find_one({"username": username, "password": password})
    if user:
        return "<h2>Login successful!</h2>"
    else:
        return "<h2>Login failed!</h2>"

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if user_table.find_one({"username": username}):
        return "<h2>Username already exists!</h2>"
    user_table.insert_one({"username": username, "email": email, "password": password})
    return render_template('login_dbms.html')

if __name__ == '__main__':
    app.run(debug=True)
