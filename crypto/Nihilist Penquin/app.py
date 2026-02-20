import os
import sqlite3
from datetime import datetime, timedelta, timezone

import base64
import json
import hmac
import hashlib

from flask import Flask, request, jsonify, Response, render_template
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


app = Flask(__name__)

FLAG = os.getenv("FLAG", "SKYDAYS{lo_siento_wilson}")
DB_PATH = os.getenv("DB_PATH", "/tmp/app.db")

# Login token TTL (minutes)
TOKEN_TTL_MINUTES = int(os.getenv("TOKEN_TTL_MINUTES", "30"))


# -----------------------------
# Keypair (generated on start)
# -----------------------------
def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem.decode(), public_pem.decode()


PRIVATE_KEY_PEM, PUBLIC_KEY_PEM = generate_rsa_keypair()


# -----------------------------
# Database
# -----------------------------
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


# -----------------------------
# JWT helpers
# -----------------------------
def issue_token(username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": "user",
        "admin": False,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=TOKEN_TTL_MINUTES)).timestamp()),
        "iss": "service",
    }
    return jwt.encode(payload, PRIVATE_KEY_PEM, algorithm="RS256")


def get_bearer_token():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    return auth.split(" ", 1)[1].strip()


def b64url_decode(s: str) -> bytes:
    s += "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s.encode())


def verify_token(token: str):
    """
    INTENTIONALLY VULNERABLE (medium):
    - If alg == HS256: verify signature manually using PUBLIC_KEY_PEM as HMAC secret (BAD!)
    - If alg == RS256: verify normally using PyJWT + PUBLIC_KEY_PEM
    This enables RS256 <-> HS256 algorithm confusion.
    """
    parts = token.split(".")
    if len(parts) != 3:
        raise Exception("malformed token")

    header_b64, payload_b64, sig_b64 = parts
    header = json.loads(b64url_decode(header_b64))
    alg = header.get("alg")

    if alg == "HS256":
        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected = hmac.new(PUBLIC_KEY_PEM.encode(), signing_input, hashlib.sha256).digest()
        expected_b64 = base64.urlsafe_b64encode(expected).rstrip(b"=").decode()

        if not hmac.compare_digest(expected_b64, sig_b64):
            raise Exception("bad signature")

        payload = json.loads(b64url_decode(payload_b64))

        # minimal claim checks
        now = int(datetime.now(timezone.utc).timestamp())
        if payload.get("iss") != "service":
            raise Exception("bad issuer")
        if "exp" not in payload or int(payload["exp"]) < now:
            raise Exception("token expired")
        if "iat" not in payload or "sub" not in payload:
            raise Exception("missing claims")

        return payload

    # RS256 path
    return jwt.decode(
        token,
        PUBLIC_KEY_PEM,
        algorithms=["RS256"],
        options={"require": ["exp", "iat", "sub"]},
        issuer="service",
    )


# -----------------------------
# Site routes (templates)
# -----------------------------
@app.get("/")
def home():
    return render_template("home.html", title="JWT Challenge")


@app.get("/register")
def register_page():
    return render_template("register.html", title="Register")


@app.get("/login")
def login_page():
    return render_template("login.html", title="Login")


@app.get("/me")
def me_page():
    return render_template("me.html", title="Me")


@app.get("/admin")
def admin_page():
    return render_template("admin.html", title="Admin")


@app.get("/about")
def about_page():
    return render_template("about.html", title="About")


# -----------------------------
# API routes
# -----------------------------
@app.get("/.well-known/public.pem")
def public_pem():
    return Response(PUBLIC_KEY_PEM, mimetype="application/x-pem-file")


@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    conn = db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "username already exists"}), 409
    finally:
        conn.close()

    return jsonify({"ok": True, "message": "registered"})


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if not row or not check_password_hash(row["password_hash"], password):
        return jsonify({"error": "invalid credentials"}), 401

    token = issue_token(username)
    return jsonify({"token": token})


@app.get("/api/me")
def api_me():
    token = get_bearer_token()
    if not token:
        return jsonify({"error": "missing bearer token"}), 401

    try:
        decoded = verify_token(token)
    except Exception as e:
        return jsonify({"error": "invalid token", "details": str(e)}), 401

    return jsonify(
        {
            "sub": decoded.get("sub"),
            "role": decoded.get("role"),
            "admin": decoded.get("admin"),
            "iss": decoded.get("iss"),
            "exp": decoded.get("exp"),
        }
    )


@app.get("/api/admin/flag")
def api_admin_flag():
    token = get_bearer_token()
    if not token:
        return jsonify({"error": "missing bearer token"}), 401

    try:
        decoded = verify_token(token)
    except Exception as e:
        return jsonify({"error": "invalid token", "details": str(e)}), 401

    is_admin = bool(decoded.get("admin")) or decoded.get("role") == "admin"
    if not is_admin:
        return jsonify({"error": "admin only"}), 403

    return jsonify({"flag": FLAG})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
