from flask import Flask, jsonify, request
import random
import string
import base64

app = Flask(__name__)

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


namespaces = ["default", "kube-system", "kube-public", "monitoring", "logging", "ingress-nginx", "matrix"]

all_pods = {ns: [] for ns in namespaces}

services = ["web-server", "db-node", "auth-service", "cache-layer", "api-gateway", "worker-queue", "cron-job", "log-aggregator", "metrics-exporter"]


for ns in namespaces:
    num_pods = random.randint(50, 200) if ns != "matrix" else 300
    for i in range(num_pods):
        pod_name = f"{random.choice(services)}-{generate_random_string(5)}"
        all_pods[ns].append({
            "metadata": {
                "name": pod_name,
                "namespace": ns,
                "annotations": {
                    "k8s.io/created-by": "replicaset-controller",
                    "monitoring.coreos.com/scrape": "true"
                }
            },
            "spec": {"containers": [{"name": "app", "image": f"repo.internal/{pod_name.split('-')[0]}:latest"}]},
            "status": {"phase": random.choice(["Running", "Pending", "Succeeded", "Failed"])}
        })


target_pod_name = "legacy-auth-pod-x89j"
quote_b64 = base64.b64encode("\"Ignorance is bliss.\" - The Matrix".encode()).decode()

all_pods["matrix"].insert(150, {
    "metadata": {
        "name": target_pod_name,
        "namespace": "matrix",
        "annotations": {
            "legacy-annotation": quote_b64,
            "owner": "sysadmin"
        }
    },
    "spec": {"containers": [{"name": "auth-legacy", "image": "auth:v1.0"}]},
    "status": {"phase": "Running"}
})

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    if not path.startswith("api/v1"):
        return jsonify({
            "kind": "Status",
            "apiVersion": "v1",
            "metadata": {},
            "status": "Failure",
            "message": "the server could not find the requested resource",
            "reason": "NotFound",
            "details": {},
            "code": 404
        }), 404

    if path == "api/v1/namespaces":
        items = [{"metadata": {"name": ns}} for ns in namespaces]
        return jsonify({
            "kind": "NamespaceList",
            "apiVersion": "v1",
            "metadata": {"resourceVersion": "1234"},
            "items": items
        })

    if "pods" not in path:
         return jsonify({
            "kind": "Status",
            "apiVersion": "v1",
            "metadata": {},
            "status": "Failure",
            "message": "pods is forbidden: User \"system:anonymous\" cannot list resource \"pods\" in API group \"\" at the cluster scope",
            "reason": "Forbidden",
            "details": {"group": "", "kind": "pods"},
            "code": 403
         }), 403

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({
            "kind": "Status",
            "apiVersion": "v1",
            "metadata": {},
            "status": "Failure",
            "message": "Unauthorized",
            "reason": "Unauthorized",
            "code": 401
        }), 401

    if path.startswith("api/v1/namespaces/") and path.endswith("/pods"):
        ns = path.split("/")[3]
        if ns in namespaces:
             return jsonify({
                "kind": "PodList",
                "apiVersion": "v1",
                "metadata": {"resourceVersion": "5678"},
                "items": all_pods[ns]
             })
        else:
            return jsonify({
                "kind": "Status",
                "apiVersion": "v1",
                "metadata": {},
                "status": "Failure",
                "message": f"namespaces \"{ns}\" not found",
                "reason": "NotFound",
                "details": {"name": ns, "kind": "namespaces"},
                "code": 404
            }), 404



    all_pods_flat = []
    for pods_in_ns in all_pods.values():
        all_pods_flat.extend(pods_in_ns)

    return jsonify({
        "kind": "PodList",
        "apiVersion": "v1",
        "metadata": {"resourceVersion": "9012"},
        "items": all_pods_flat
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443)
