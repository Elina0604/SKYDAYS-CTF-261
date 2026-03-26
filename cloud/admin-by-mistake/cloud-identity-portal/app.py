from flask import Flask, render_template, request, make_response, send_file
import os

app = Flask(__name__)




TARGET_PASSWORD = "\u0441\u006c\u043e\u0075\u0501\u200b\u0430\u0441\u0441\u0435\u0455\u0455"



TARGET_HINT = "b\u0430\u0441k\u200b\u0501\u043e\u043er"

import uuid
from io import BytesIO

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password', '')

        if password == TARGET_PASSWORD:

            unique_token = f"guest-token-{uuid.uuid4().hex[:8]}"



            kubeconfig_path = os.path.join(os.path.dirname(__file__), 'kubeconfig.yaml')
            if not os.path.exists(kubeconfig_path):
                kubeconfig_path = '/app/kubeconfig.yaml'

            with open(kubeconfig_path, 'r') as f:
                content = f.read()


            content = content.replace('dummy-bearer-token-12345', unique_token)


            mem_file = BytesIO()
            mem_file.write(content.encode('utf-8'))
            mem_file.seek(0)

            return send_file(mem_file, as_attachment=True, download_name='kubeconfig.yaml', mimetype='application/x-yaml')
        else:
            error = "Invalid credentials or malformed input."

    return render_template('index.html', error=error, hint=TARGET_HINT)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
