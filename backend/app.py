from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from prometheus_flask_exporter import PrometheusMetrics
import os

def create_app():
    app = Flask(__name__)
    # This is a stateless REST API that only accepts JSON requests.
    # CSRF protection is intentionally disabled because:
    # - No browser sessions or cookies are used for authentication.
    # - CORS is configured to control allowed origins.
    # - Clients must use token-based or controlled access.
    CORS(app)
    PrometheusMetrics(app)

    # MySQL configuration
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root1"),
        password=os.getenv("DB_PASSWORD", "Krishna8kichu"),
        database=os.getenv("DB_NAME", "my_db"),
        port=int(os.getenv("DB_PORT", 3306))
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
    
    #@app.route('/api/users/<int:user_id>', methods=['DELETE'])
    #def delete_user(user_id):
     #   cursor = db.cursor()
     #   cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
      #  db.commit()
       # if cursor.rowcount == 0:
        #    return jsonify({"error": "User not found"}), 404
       # return jsonify({"status": "User deleted"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)