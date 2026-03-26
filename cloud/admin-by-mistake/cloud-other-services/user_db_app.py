from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_PATH = 'app.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    if not path.startswith("api"):
        return jsonify({"status": "error", "message": "Invalid endpoint. Available endpoints: /api/v1/config, /api/v1/users, /api/v1/search"}), 404

    if path == "api/v1/config":
        return jsonify({
            "status": "success",
            "data": {
                "db_version": "v1.4.2",
                "auth_method": "X-Admin-Key",
                "default_key_hint": "admin123",
                "max_connections": 1000
            }
        })

    if "users" not in path and "search" not in path:
        return jsonify({"status": "error", "message": "Access denied"}), 403

    admin_auth = request.headers.get("X-Admin-Key")
    if not admin_auth or admin_auth != "admin123":
        return jsonify({"status": "error", "message": "Missing or invalid X-Admin-Key"}), 401

    if path == "api/v1/users":
        conn = get_db_connection()
        users = conn.execute('SELECT id, username, role FROM users LIMIT 10').fetchall()
        conn.close()
        return jsonify({
            "status": "success",
            "data": [dict(ix) for ix in users],
            "message": "Showing first 10 users. Use search endpoint for details."
        })

    if path == "api/v1/search":


        username_query = request.args.get('username')
        if not username_query:
            return jsonify({"status": "error", "message": "Missing 'username' parameter in query string."}), 400

        conn = get_db_connection()
        try:

            query = f"SELECT id, username, role, last_login, secret_note FROM users WHERE username = '{username_query}'"
            results = conn.execute(query).fetchall()
            conn.close()

            if results:
                return jsonify({
                    "status": "success",
                    "data": [dict(ix) for ix in results]
                })
            else:
                return jsonify({"status": "error", "message": "User not found"}), 404
        except sqlite3.Error as e:
            conn.close()


            return jsonify({"status": "db_error", "message": str(e)}), 500

    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
