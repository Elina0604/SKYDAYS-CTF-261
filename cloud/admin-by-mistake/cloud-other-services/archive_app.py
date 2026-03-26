from flask import Flask, jsonify, request, abort
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

app = Flask(__name__)










FAKE_AES_KEY = b"deep_archive_k_16"
FAKE_AES_IV  = b"deep_archive_i_16"
FAKE_QUOTE   = b"\"It's no use going back to yesterday, because I was a different person then.\" - Alice in Wonderland"

def get_encrypted_quote():
    cipher = AES.new(FAKE_AES_KEY, AES.MODE_CBC, FAKE_AES_IV)
    ct_bytes = cipher.encrypt(pad(FAKE_QUOTE, AES.block_size))
    return base64.b64encode(ct_bytes).decode('utf-8')

@app.route('/api/v1/nebula/init', methods=['GET'])
def stage_1():
    token = request.headers.get("X-Project-Token")
    if not token or token != "nebula-init-token-7x92q":
         return jsonify({"error": "Unauthorized. Project token required."}), 401


    next_stage_url = "/api/v1/nebula/archives"
    encoded_url = base64.b64encode(next_stage_url.encode()).decode('utf-8')
    return jsonify({
        "message": "Welcome to Project Nebula. The next coordinate is encoded.",
        "coordinate": encoded_url
    })

@app.route('/api/v1/nebula/archives', methods=['GET'])
def stage_2():

    files = []
    for i in range(1, 1000):
        files.append(f"syslog_{i}.tar.gz")


    files.insert(42, "README_key_is_deep_archive_k_16.txt")
    files.insert(400, "README_iv_is_deep_archive_i_16.txt")
    files.insert(800, "secret_manifest.enc")

    return jsonify({
        "directory": "nebula/archives/",
        "files": files,
        "message": "Explore the archives."
    })

@app.route('/api/v1/nebula/archives/<filename>', methods=['GET'])
def stage_3(filename):
    if filename == "secret_manifest.enc":
         return jsonify({
             "file": filename,
             "type": "AES-128-CBC",
             "content": get_encrypted_quote()
         })
    elif filename.startswith("README_"):
         return jsonify({
             "file": filename,
             "content": "This file contains critical structural information. Or does it?"
         })
    elif filename.startswith("syslog_"):
         return jsonify({
             "file": filename,
             "content": "bWFzc2l2ZSBhbW91bnQgb2YganVuayBsb2dzIGhlcmU="
         })

    return abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
