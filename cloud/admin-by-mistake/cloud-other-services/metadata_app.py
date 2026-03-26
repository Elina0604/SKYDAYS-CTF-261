from flask import Flask, Response, request, abort, jsonify
import os
import json

app = Flask(__name__)



@app.route('/')
def index():
    return Response("latest\n", mimetype='text/plain')

@app.route('/latest')
def latest():
    return Response("meta-data\nuser-data\n", mimetype='text/plain')

@app.route('/latest/user-data')
def user_data():
    return Response("#cloud-config\n# Configuration initialized.\n", mimetype='text/plain')

@app.route('/latest/meta-data/')
def meta_data():
    endpoints = [
        "ami-id",
        "hostname",
        "iam/",
        "instance-action",
        "instance-id",
        "instance-type",
        "local-hostname",
        "local-ipv4",
        "mac",
        "metrics/",
        "network/",
        "placement/",
        "profile",
        "public-hostname",
        "public-ipv4",
        "public-keys/",
        "reservation-id",
        "security-groups",
        "services/",
        "tags/"
    ]
    return Response("\n".join(endpoints) + "\n", mimetype='text/plain')

@app.route('/latest/meta-data/<path:subpath>')
def meta_data_subpath(subpath):
    if subpath == "iam":
        return Response("info\nsecurity-credentials/\n", mimetype='text/plain')
    elif subpath == "iam/info":
        info = {
            "Code": "Success",
            "LastUpdated": "2023-10-26T15:00:00Z",
            "InstanceProfileArn": "arn:aws:iam::123456789012:instance-profile/CloudVaultAccessRole",
            "InstanceProfileId": "AIPAxxxxxxxxxxxxxxxxx"
        }
        return jsonify(info)
    elif subpath == "iam/security-credentials":
        return Response("CloudVaultAccessRole\n", mimetype='text/plain')
    elif subpath == "iam/security-credentials/CloudVaultAccessRole":



        creds = {
            "Code": "Success",
            "LastUpdated": "2023-10-26T15:00:00Z",
            "Type": "AWS-HMAC",
            "AccessKeyId": "AKIA-VAULT-ACCESS-XYZ",
            "Notice": "SecretAccessKey is stored in the internal Redis cache (cloud-internal-redis:6379)",
            "Token": "IQoJb3JpZ2luX2VjEJv...",
            "Expiration": "2023-10-26T21:00:00Z"
        }
        return jsonify(creds)
    elif subpath == "tags":
        return Response("instance/\n", mimetype='text/plain')
    elif subpath == "tags/instance":
        return Response("Name\nEnvironment\nVaultEndpoint\nInternalServices\n", mimetype='text/plain')
    elif subpath == "tags/instance/Name":
        return Response("CloudVaultAccessor\n", mimetype='text/plain')
    elif subpath == "tags/instance/Environment":
        return Response("Production\n", mimetype='text/plain')
    elif subpath == "tags/instance/VaultEndpoint":

        return Response("http://cloud-internal-vault:5000/api/v1/vault/state\n", mimetype='text/plain')
    elif subpath == "tags/instance/InternalServices":

        return Response("cloud-internal-redis:6379\ncloud-apache-server:80\ncloud-log-store:27017\ncloud-k8s-api:8443\ncloud-analytics-engine:9200\ncloud-user-db:3000\n", mimetype='text/plain')
    elif subpath == "services":
        return Response("apache/\nkubernetes/\nlog-store/\nanalytics-engine/\nuser-db/\n", mimetype='text/plain')
    elif subpath == "services/apache":

        return Response("Legacy web server. Version: Apache/2.4.49 (Unix). Holds Redis auth configuration in /usr/local/apache2/conf/internal/redis.conf\n", mimetype='text/plain')
    elif subpath == "services/kubernetes":
        return Response("Internal K8s API endpoint. Check /api/v1/namespaces. Requires Bearer token for advanced access.\n", mimetype='text/plain')
    elif subpath == "services/log-store":
        return Response("Logs database. Explore /logs/ collections. Requires standard admin database auth for deeper access.\n", mimetype='text/plain')
    elif subpath == "services/analytics-engine":
        return Response("Search cluster. You know, for Search. Check /_cat/indices for available data.\n", mimetype='text/plain')
    elif subpath == "services/user-db":
        return Response("User database API. Start at /api/v1/config. Header X-Admin-Key is required for deeper access.\n", mimetype='text/plain')
    elif subpath in ["ami-id", "hostname", "instance-action", "instance-id", "instance-type", "local-hostname", "local-ipv4", "mac", "profile", "public-hostname", "public-ipv4", "reservation-id", "security-groups"]:
        return Response(f"mock-data-for-{subpath}\n", mimetype='text/plain')
    else:
        abort(404)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080)
