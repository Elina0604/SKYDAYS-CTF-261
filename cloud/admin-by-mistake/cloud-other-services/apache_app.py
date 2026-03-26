from flask import Flask, request, Response

app = Flask(__name__)

@app.before_request
def handle_cve():
    raw_uri = request.environ.get('REQUEST_URI', request.url)

    if '.%2e/' in raw_uri.lower() or '%2e%2e/' in raw_uri.lower() or '%2e%2e%2f' in raw_uri.lower() or '..%2f' in raw_uri.lower() or '.%2e%2f' in raw_uri.lower():
        if 'redis.conf' in raw_uri:
            return Response("requirepass R3d1sP@ssw0rd!\n", mimetype="text/plain")
        if 'passwd' in raw_uri:
            return Response("root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n", mimetype="text/plain")

        return Response("<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">\n<html><head>\n<title>404 Not Found</title>\n</head><body>\n<h1>Not Found</h1>\n<p>The requested URL was not found on this server.</p>\n</body></html>", status=404)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return Response("<html><body><h1>It works!</h1></body></html>", mimetype="text/html")

@app.after_request
def add_header(response):
    response.headers['Server'] = 'Apache/2.4.49 (Unix)'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
