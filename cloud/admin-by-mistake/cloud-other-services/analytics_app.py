from flask import Flask, jsonify, request
import json
import uuid
import random
import base64

app = Flask(__name__)


app_logs_data = []
for i in range(1000):
    app_logs_data.append({
        "_index": "app-logs",
        "_type": "_doc",
        "_id": str(uuid.uuid4()),
        "_score": 1.0,
        "_source": {
            "timestamp": f"2023-10-26T12:{random.randint(10,59)}:00Z",
            "level": random.choice(["INFO", "WARN", "DEBUG"]),
            "message": f"Service operation {random.randint(1000, 9999)} completed"
        }
    })

system_metrics_data = []
for i in range(1000):
    system_metrics_data.append({
        "_index": "system-metrics",
        "_type": "_doc",
        "_id": str(uuid.uuid4()),
        "_score": 1.0,
        "_source": {
            "timestamp": f"2023-10-26T12:{random.randint(10,59)}:00Z",
            "cpu_usage": random.uniform(10.0, 99.0),
            "memory_usage": random.uniform(10.0, 99.0)
        }
    })

secret_storage_data = []
for i in range(2500):
    secret_storage_data.append({
        "_index": "secret-storage",
        "_type": "_doc",
        "_id": str(uuid.uuid4()),
        "_score": 1.0,
        "_source": {
            "description": f"Internal mapping {i}",
            "payload": base64.b64encode(f"System identifier chunk {uuid.uuid4()}".encode()).decode()
        }
    })

secret_storage_data.insert(1899, {
    "_index": "secret-storage",
    "_type": "_doc",
    "_id": str(uuid.uuid4()),
    "_score": 1.0,
    "_source": {
        "description": "Important Quote",
        "payload": base64.b64encode("\"There is no spoon.\" - The Matrix".encode()).decode()
    }
})

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    if path == "":
        return jsonify({
            "name" : "analytics-node-1",
            "cluster_name" : "analytics-cluster",
            "cluster_uuid" : "a1b2c3d4e5",
            "version" : {
                "number" : "7.10.2",
                "build_flavor" : "default",
                "build_type" : "docker",
                "build_hash" : "747e1cc71def077253878a59143c1f785afa92b9",
                "build_date" : "2021-01-13T00:42:12.435326Z",
                "build_snapshot" : False,
                "lucene_version" : "8.7.0",
                "minimum_wire_compatibility_version" : "6.8.0",
                "minimum_index_compatibility_version" : "6.0.0-beta1"
            },
            "tagline" : "You Know, for Search"
        })

    if path == "_cat/indices":
        return "green open app-logs 1 1 1500 0 2000kb 1000kb\ngreen open system-metrics 1 1 5000 0 10mb 5000kb\ngreen open secret-storage 1 1 2501 0 500kb 250kb\n", 200

    if path.startswith("app-logs/_search"):
        q = request.args.get('q')

        return jsonify({
            "took": 2,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": len(app_logs_data), "relation": "eq"},
                "max_score": 1.0,
                "hits": app_logs_data if not q else app_logs_data[:50]
            }
        })

    if path.startswith("system-metrics/_search"):
        q = request.args.get('q')
        return jsonify({
            "took": 3,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": len(system_metrics_data), "relation": "eq"},
                "max_score": 1.0,
                "hits": system_metrics_data if not q else system_metrics_data[:50]
            }
        })

    if path.startswith("secret-storage/_search"):
        q = request.args.get('q')
        return jsonify({
            "took": 4,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": len(secret_storage_data), "relation": "eq"},
                "max_score": 1.0,
                "hits": secret_storage_data if not q else [s for s in secret_storage_data if q.lower() in json.dumps(s).lower()]
            }
        })

    if "_search" not in path:
         return jsonify({
            "error": {
                "root_cause": [
                    {
                        "type": "index_not_found_exception",
                        "reason": f"no such index [{path}]",
                        "resource.type": "index_or_alias",
                        "resource.id": path,
                        "index_uuid": "_na_",
                        "index": path
                    }
                ],
                "type": "index_not_found_exception",
                "reason": f"no such index [{path}]",
                "resource.type": "index_or_alias",
                "resource.id": path,
                "index_uuid": "_na_",
                "index": path
            },
            "status": 404
        }), 404

    return jsonify({
        "error": {
            "root_cause": [
                {
                    "type": "search_phase_execution_exception",
                    "reason": "all shards failed",
                    "phase": "query",
                    "grouped": True,
                    "failed_shards": []
                }
            ],
            "type": "search_phase_execution_exception",
            "reason": "all shards failed",
            "phase": "query",
            "grouped": True,
            "failed_shards": [],
            "caused_by": {
                "type": "parse_exception",
                "reason": "Cannot parse '', expected query string or query body"
            }
        },
        "status": 400
    }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9200)
