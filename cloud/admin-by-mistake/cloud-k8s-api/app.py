from flask import Flask, jsonify, request
import base64
import json
import uuid

app = Flask(__name__)



single_use_tokens = {}

def create_k8s_error(message, reason, code):
    return jsonify({
        "kind": "Status",
        "apiVersion": "v1",
        "metadata": {},
        "status": "Failure",
        "message": message,
        "reason": reason,
        "code": code
    }), code


@app.route('/api', methods=['GET'])
def api_versions():
    return jsonify({
        "kind": "APIVersions",
        "versions": ["v1"],
        "serverAddressByClientCIDRs": [
            {
                "clientCIDR": "0.0.0.0/0",
                "serverAddress": "127.0.0.1:8443"
            }
        ]
    })

@app.route('/api/v1', methods=['GET'])
def api_v1_resources():
    return jsonify({
        "kind": "APIResourceList",
        "groupVersion": "v1",
        "resources": [
            {"name": "namespaces", "singularName": "", "namespaced": False, "kind": "Namespace", "verbs": ["create", "delete", "get", "list", "patch", "update", "watch"]},
            {"name": "pods", "singularName": "", "namespaced": True, "kind": "Pod", "verbs": ["create", "delete", "deletecollection", "get", "list", "patch", "update", "watch"]},
            {"name": "secrets", "singularName": "", "namespaced": True, "kind": "Secret", "verbs": ["create", "delete", "deletecollection", "get", "list", "patch", "update", "watch"]}
        ]
    })

@app.route('/apis', methods=['GET'])
def apis_versions():
    return jsonify({
        "kind": "APIGroupList",
        "apiVersion": "v1",
        "groups": [
            {
                "name": "authorization.k8s.io",
                "versions": [{"groupVersion": "authorization.k8s.io/v1", "version": "v1"}],
                "preferredVersion": {"groupVersion": "authorization.k8s.io/v1", "version": "v1"}
            },
            {
                "name": "rbac.authorization.k8s.io",
                "versions": [{"groupVersion": "rbac.authorization.k8s.io/v1", "version": "v1"}],
                "preferredVersion": {"groupVersion": "rbac.authorization.k8s.io/v1", "version": "v1"}
            }
        ]
    })

@app.route('/openapi/v2', methods=['GET'])
def openapi_v2():
    return jsonify({"swagger": "2.0", "info": {"title": "Kubernetes", "version": "v1.27.0"}, "paths": {}})

@app.route('/apis/authorization.k8s.io/v1', methods=['GET'])
def api_authorization_v1_resources():
    return jsonify({
        "kind": "APIResourceList",
        "apiVersion": "v1",
        "groupVersion": "authorization.k8s.io/v1",
        "resources": [
            {"name": "selfsubjectrulesreviews", "singularName": "", "namespaced": False, "kind": "SelfSubjectRulesReview", "verbs": ["create"]}
        ]
    })

@app.route('/apis/rbac.authorization.k8s.io/v1', methods=['GET'])
def api_rbac_v1_resources():
    return jsonify({
        "kind": "APIResourceList",
        "apiVersion": "v1",
        "groupVersion": "rbac.authorization.k8s.io/v1",
        "resources": [
            {"name": "rolebindings", "singularName": "", "namespaced": True, "kind": "RoleBinding", "verbs": ["create", "delete", "get", "list", "patch", "update", "watch"]},
            {"name": "roles", "singularName": "", "namespaced": True, "kind": "Role", "verbs": ["create", "delete", "get", "list", "patch", "update", "watch"]}
        ]
    })

@app.route('/apis/authorization.k8s.io/v1/selfsubjectrulesreviews', methods=['POST'])
def self_subject_rules_review():

    return jsonify({
        "kind": "SelfSubjectRulesReview",
        "apiVersion": "authorization.k8s.io/v1",
        "metadata": {"creationTimestamp": None},
        "spec": {},
        "status": {
            "resourceRules": [
                {
                    "verbs": ["create"],
                    "apiGroups": ["rbac.authorization.k8s.io"],
                    "resources": ["rolebindings"],
                    "namespaces": ["default"]
                }
            ],
            "nonResourceRules": [],
            "incomplete": False
        }
    }), 201

@app.route('/api/v1/namespaces/nebula-system/secrets', methods=['GET'])
def get_secrets():



    auth_header = request.headers.get("Authorization")
    is_admin = False

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

        val = single_use_tokens.pop(token, None)
        if val is not None:
            is_admin = True

    if not is_admin:
        return create_k8s_error('User "guest-sa" cannot list resource "secrets" in API group "" in the namespace "nebula-system"', "Forbidden", 403)

    terraform_state = {
        "version": 4,
        "terraform_version": "1.5.0",
        "serial": 1,
        "lineage": "abc-123",
        "outputs": {
            "flag": {
                "value": "SKYDAYS{th3r35_n0_cl0ud_1ts_jU5t_50m30n3_eL5e5_c0mPUt3R_8a9b}",
                "type": "string"
            }
        }
    }
    encoded_state = base64.b64encode(json.dumps(terraform_state).encode()).decode()

    return jsonify({
        "kind": "SecretList",
        "apiVersion": "v1",
        "metadata": {},
        "items": [
            {
                "metadata": {
                    "name": "terraform-backend-state",
                    "namespace": "nebula-system",
                },
                "type": "Opaque",
                "data": {
                    "terraform.tfstate": encoded_state
                }
            }
        ]
    })

@app.route('/apis/rbac.authorization.k8s.io/v1/namespaces/default/rolebindings', methods=['POST'])
def create_rolebinding():


    try:
        payload = request.get_json()
        if not payload:
            return create_k8s_error("Invalid JSON payload", "BadRequest", 400)

        role_ref = payload.get('roleRef', {})
        subjects = payload.get('subjects', [])

        if not subjects:
             return create_k8s_error("RoleBinding must specify subjects", "BadRequest", 400)

        role_name = role_ref.get('name')
        subject_name = subjects[0].get('name')

        if role_name == "nebula-admin-role" and subject_name == "guest-sa":

            auth_header = request.headers.get("Authorization")
            user_token = "unknown"
            if auth_header and auth_header.startswith("Bearer "):
                user_token = auth_header.split(" ")[1]


            new_token = f"admin-tmp-token-{uuid.uuid4().hex[:8]}"
            single_use_tokens[new_token] = user_token


            base_name = payload.get('metadata', {}).get('name', 'exploit-binding')
            unique_name = f"{base_name}-{new_token.split('-')[-1]}"

            return jsonify({
                "kind": "RoleBinding",
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "metadata": {
                    "name": unique_name,
                    "namespace": "default",
                    "creationTimestamp": "2023-10-27T10:00:00Z",
                    "annotations": {
                        "skydays/hint": f"RoleBinding created successfully. However, standard state mapping is restricted. To list secrets as admin, you must use this single-use temporary admin token in your Authorization header: {new_token}"
                    }
                },
                "roleRef": role_ref,
                "subjects": subjects
            }), 201
        else:
            return create_k8s_error("RoleBinding creation successful, but no admin privileges granted.", "Created", 201)

    except Exception as e:
        return create_k8s_error(f"Internal server error: {str(e)}", "InternalError", 500)

@app.route('/apis/rbac.authorization.k8s.io/v1/namespaces/default/rolebindings', methods=['GET'])
@app.route('/apis/rbac.authorization.k8s.io/v1/rolebindings', methods=['GET'])
def get_rolebindings():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return create_k8s_error('Unauthorized', "Unauthorized", 401)

    user_token = auth_header.split(" ")[1]

    items = []

    for stored_token, creator_token in single_use_tokens.items():
        if creator_token == user_token:
            items.append({
                "kind": "RoleBinding",
                "apiVersion": "rbac.authorization.k8s.io/v1",
                "metadata": {
                    "name": f"exploit-binding-{stored_token.split('-')[-1]}",
                    "namespace": "default",
                    "creationTimestamp": "2023-10-27T10:00:00Z",
                    "annotations": {
                        "skydays/hint": f"RoleBinding created successfully. However, standard state mapping is restricted. To list secrets as admin, you must use this single-use temporary admin token in your Authorization header: {stored_token}"
                    }
                },
                "roleRef": {
                    "apiGroup": "rbac.authorization.k8s.io",
                    "kind": "Role",
                    "name": "nebula-admin-role"
                },
                "subjects": [{
                    "kind": "ServiceAccount",
                    "name": "guest-sa",
                    "namespace": "default"
                }]
            })

    return jsonify({
        "kind": "RoleBindingList",
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "metadata": {},
        "items": items
    })

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    return create_k8s_error("the server could not find the requested resource", "NotFound", 404)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8443, ssl_context='adhoc')
