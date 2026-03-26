from flask import Flask, request, render_template, make_response
import socket
import re
import os
from urllib.parse import urlparse, unquote

app = Flask(__name__)

import ipaddress


WAF_REGEX = re.compile(
    r"(127\.|^localhost|172\.19\.|^10\.|^0\.|^0$|::1)",
    re.IGNORECASE
)

def is_blocked(hostname):
    if not hostname:
        return True
    if WAF_REGEX.search(hostname):
        return True
    return False

def is_ip_blocked(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)

        if ip in ipaddress.ip_network('172.19.0.0/16'):
            return False

#        if ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_unspecified:
 #           return True
        return False
    except ValueError:
        return True

def fetch_url_raw(url_str):
    try:
        parsed = urlparse(url_str)
        hostname = parsed.hostname
        port = parsed.port if parsed.port else 80

        if is_blocked(hostname):
             return "WAF Blocked! Access to internal resources is restricted."

        try:
            target_ip = socket.gethostbyname(hostname)
        except socket.gaierror:
             return f"Could not resolve hostname: {hostname}"


        if is_ip_blocked(target_ip):
             return "WAF Blocked! Resolved IP belongs to a restricted internal network."

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect((target_ip, port))
        except Exception as e:
            return f"Connection failed: {str(e)}"

        path = parsed.path if parsed.path else "/"
        if parsed.query:
            path += "?" + parsed.query


        if '%0d' in path.lower() or '%0a' in path.lower() or '\r' in path or '\n' in path:
            return "WAF Blocked! Illegal characters detected in URL."





        path = path.replace(' ', '%20')
        decoded_path = path.replace('%250d', '\r').replace('%250D', '\r').replace('%250a', '\n').replace('%250A', '\n').replace('%2520', ' ')


        request_data = f"GET {decoded_path} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"

        s.sendall(request_data.encode('utf-8'))

        response = b""
        while True:
            try:
                data = s.recv(4096)
                if not data:
                    break
                response += data
            except socket.timeout:
                break

        s.close()
        return response.decode('utf-8', errors='replace')

    except Exception as e:
        return f"Error fetching URL: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return render_template('index.html', result="URL parameter required")

        if not url.startswith('http'):
            return render_template('index.html', result="Only HTTP/HTTPS allowed")

        result = fetch_url_raw(url)
        resp = make_response(render_template('index.html', result=result))

        resp.headers['X-Cloud-Metadata-Endpoint'] = 'cloud-metadata-service:8080'
        return resp

    resp = make_response(render_template('index.html'))

    resp.headers['X-Cloud-Metadata-Endpoint'] = 'cloud-metadata-service:8080'
    return resp

@app.route('/api/webhook/test', methods=['POST'])
def webhook_test():
    url = request.form.get('url')
    if not url:
        return "URL parameter required", 400

    if not url.startswith('http'):
        return "Only HTTP/HTTPS allowed", 400

    result = fetch_url_raw(url)
    resp = make_response(result)
    resp.headers['X-Cloud-Metadata-Endpoint'] = 'cloud-metadata-service:8080'
    return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    try:
        app.run(host='0.0.0.0', port=port)
    except PermissionError:
        print(f"Permission denied on port {port}, falling back to 8080")
        app.run(host='0.0.0.0', port=8080)
