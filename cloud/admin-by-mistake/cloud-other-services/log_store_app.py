from flask import Flask, request, jsonify, abort
import random
import uuid
import base64

app = Flask(__name__)


app_logs = []
error_logs = []
access_logs = []

for i in range(1000):
    app_logs.append({"_id": str(uuid.uuid4()), "level": "info", "msg": f"Worker {random.randint(1, 100)} processed job {uuid.uuid4()}"})
    if i % 5 == 0:
        error_logs.append({"_id": str(uuid.uuid4()), "level": "warn", "msg": f"Connection timeout to redis from worker {random.randint(1, 100)}"})
    access_logs.append({"_id": str(uuid.uuid4()), "ip": f"192.168.1.{random.randint(1, 255)}", "path": f"/api/v1/{random.choice(['users', 'posts', 'comments'])}"})


quotes = []
for i in range(5000):
    quotes.append({"_id": str(uuid.uuid4()), "value": base64.b64encode(f"Standard motivational quote #{i}".encode()).decode()})


secret_quote = "\"Are you a one or a zero? That's the question you have to ask yourself. Are you a yes or a no? Are you going to act or not?\" - Mr. Robot"
quotes.insert(3133, {"_id": "message_legacy_001", "value": base64.b64encode(secret_quote.encode()).decode()})

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    if not path:
        return jsonify({"ok": 0, "errmsg": "MongoError: database name cannot be empty", "code": 73, "codeName": "InvalidNamespace"})

    if "admin" not in path and "system" not in path and "logs" not in path:
        return jsonify({"ok": 0, "errmsg": "MongoError: auth failed", "code": 18, "codeName": "AuthenticationFailed"})

    if "logs/collections" in path:
        return jsonify({"ok": 1, "collections": ["app_logs", "error_logs", "access_logs"]})

    if "logs/app_logs" in path:
        return jsonify({
            "ok": 1,
            "cursor": {
                "id": 0,
                "ns": "logs.app_logs",
                "firstBatch": app_logs
            }
        })
    if "logs/error_logs" in path:
        return jsonify({
            "ok": 1,
            "cursor": {
                "id": 0,
                "ns": "logs.error_logs",
                "firstBatch": error_logs
            }
        })
    if "logs/access_logs" in path:
        return jsonify({
            "ok": 1,
            "cursor": {
                "id": 0,
                "ns": "logs.access_logs",
                "firstBatch": access_logs
            }
        })

    if "admin/collections" in path:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
             return jsonify({"ok": 0, "errmsg": "MongoError: command requires authentication", "code": 13, "codeName": "Unauthorized"})
        return jsonify({"ok": 1, "collections": ["system.users", "system.version", "quotes", "audit_logs"]})

    if "admin/quotes" in path:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
             return jsonify({"ok": 0, "errmsg": "MongoError: command requires authentication", "code": 13, "codeName": "Unauthorized"})

        return jsonify({
            "ok": 1,
            "cursor": {
                "id": 0,
                "ns": "admin.quotes",
                "firstBatch": quotes
            }
        })

    if "admin/audit_logs" in path:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
             return jsonify({"ok": 0, "errmsg": "MongoError: command requires authentication", "code": 13, "codeName": "Unauthorized"})

        return jsonify({
            "ok": 1,
            "cursor": {
                "id": 0,
                "ns": "admin.audit_logs",
                "firstBatch": [{"_id": "1", "event": "admin login"}, {"_id": "2", "event": "config changed"}]
            }
        })

    return jsonify({"ok": 0, "errmsg": "MongoError: no such command", "code": 59, "codeName": "CommandNotFound"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=27017)
