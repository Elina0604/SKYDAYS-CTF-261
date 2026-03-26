import sqlite3
import random
import string
import base64
import os

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

db_path = "app.db"

if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    role TEXT,
    last_login TEXT,
    secret_note TEXT
)
''')

cursor.execute('''
CREATE TABLE system_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_name TEXT,
    key_value TEXT,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE secret_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT,
    endpoint TEXT,
    access_token TEXT
)
''')

roles = ["viewer", "editor", "contributor", "manager", "auditor"]

for i in range(1, 501):
    username = f"user_{generate_random_string(6)}"
    role = random.choice(roles)
    last_login = f"2023-10-{random.randint(10, 26):02d}T10:00:00Z"

    if i == 404:
        username = "sysadmin_legacy"
        role = "superuser"
        secret_msg = "\"Control is an illusion.\" - Mr. Robot"
        secret_note = base64.b64encode(secret_msg.encode()).decode()
    else:
        secret_note = base64.b64encode(f"Routine check for user {i}".encode()).decode()

    cursor.execute('INSERT INTO users (username, role, last_login, secret_note) VALUES (?, ?, ?, ?)', (username, role, last_login, secret_note))


cursor.execute('INSERT INTO system_config (key_name, key_value, description) VALUES (?, ?, ?)',
               ('identity_portal_pass', 'cloud access', 'Password required for cloud-identity-portal access. DO NOT SHARE.'))

cursor.execute('INSERT INTO system_config (key_name, key_value, description) VALUES (?, ?, ?)',
               ('db_version', 'v1.4.2', 'Database Schema Version'))

cursor.execute('INSERT INTO system_config (key_name, key_value, description) VALUES (?, ?, ?)',
               ('auth_method', 'X-Admin-Key', 'Primary Authentication Method'))


cursor.execute('INSERT INTO secret_projects (project_name, endpoint, access_token) VALUES (?, ?, ?)',
               ('Project_Nebula', 'http://cloud-deep-archive:8081/api/v1/nebula/init', 'nebula-init-token-7x92q'))


conn.commit()
conn.close()

print(f"Database {db_path} generated.")
