# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)

# MySQL configuration
db = mysql.connector.connect(
    host="db",
    user="root1",
    password="Krishna8kichu@",
    database="my_db"
)

@app.route('/api/users', methods=['GET'])
def get_users():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email FROM users;")
    users = cursor.fetchall()
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (data['name'], data['email'],)
    )
    db.commit()
    return jsonify({"status": "User added"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
