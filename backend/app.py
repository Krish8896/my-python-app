from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from prometheus_flask_exporter import PrometheusMetrics

def create_app():
    app = Flask(__name__)
    CORS(app)
    metrics = PrometheusMetrics(app)

    @app.route('/')
    def index():
        return jsonify({"message": "Flask app with Prometheus metrics"})

    # MySQL configuration
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root1"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "my_db"),
        port=os.getenv("DB_PORT", "3306")
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
            (data['name'], data['email'])
        )
        db.commit()
        return jsonify({"status": "User added"}), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)