# Coding Agents Guide - Sky-Sec Inventory CTF Project

This document provides guidance for coding agents working on the Sky-Sec İç Ağ Envanter Sistemi CTF challenge, a medium-difficulty Capture The Flag educational project.

## Project Overview

This is a **multi-language CTF project** consisting of:
- **Python TCP Socket Server** with intentional SQL injection vulnerability
- **Golang CLI Client** with hardcoded encryption for reverse engineering
- **MySQL Database** with inventory and secret vault tables
- **Docker deployment** for easy setup and distribution

## Project Structure

```
skysec-inventory/
├── server/
│   ├── requirements.txt     # Python dependencies
│   ├── server.py           # TCP server with MySQL integration
│   ├── setup_db.py         # Database initialization script
│   └── docker-compose.yml  # MySQL and Server deployment
├── client/
│   ├── main.go            # Golang CLI application
│   └── go.mod             # Go module definition
└── solution/
    └── solver.py          # Reference exploit script
```

## Build/Lint/Test Commands

### Python Server Development
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r server/requirements.txt

# Run database setup
python server/setup_db.py

# Start server (port 1337 by default)
python server/server.py

# Run with Docker
docker-compose -f server/docker-compose.yml up -d
```

### Golang Client Development
```bash
# Initialize Go module (if not exists)
cd client && go mod init skysec-client

# Build client binary
go build -o skysec_client main.go

# Build statically linked binary for distribution
go build -ldflags "-s -w" -o skysec_client main.go

# Cross-compile for different platforms
GOOS=linux GOARCH=amd64 go build -o skysec_client_linux main.go
GOOS=windows GOARCH=amd64 go build -o skysec_client.exe main.go

# Format code
go fmt ./...

# Vet code for common issues
go vet ./...

# Test compilation
go build -v ./...
```

### Testing Commands
```bash
# Test server connectivity
python solution/solver.py

# Test client connection
./client/skysec_client -h 127.0.0.1 -p 1337

# Test database queries directly
mysql -u root -p -e "USE skysec_inventory; SELECT * FROM inventory;"

# Validate Docker deployment
docker ps | grep skysec
docker logs skysec-mysql
docker logs skysec-server
```

## Code Style Guidelines

### Python Server Standards
```python
# Import order: standard library, third-party, local
import socket
import base64
import mysql.connector
from threading import Thread

# Function naming: snake_case
def decode_xor_message(encrypted_data: str) -> str:
    """Decode Base64 and XOR decrypt message."""
    pass

# Constants: UPPER_SNAKE_CASE
XOR_KEY = "SkY_S3c_P4ssW0rd_99"
DEFAULT_PORT = 1337

# Intentional vulnerability comments
def execute_read_command(user_input):
    # INTENTIONAL VULNERABILITY: String concatenation for SQL injection
    query = f"SELECT details FROM inventory WHERE id = '{user_input}' AND status = 'public'"
    return execute_query(query)
```

### Golang Client Standards
```go
// Package and import organization
package main

import (
    "encoding/base64"
    "flag"
    "fmt"
    "net"
    "bufio"
    "os"
)

// Constants: PascalCase for exported, camelCase for unexported
const XORKey = "SkY_S3c_P4ssW0rd_99"  // Hardcoded for reverse engineering
const defaultPort = "1337"

// Function naming: PascalCase for exported, camelCase for unexported
func encryptMessage(message string) string {
    // XOR encryption implementation
    encrypted := make([]byte, len(message))
    key := []byte(XORKey)
    for i, b := range []byte(message) {
        encrypted[i] = b ^ key[i%len(key)]
    }
    return base64.StdEncoding.EncodeToString(encrypted)
}

// Error handling patterns
func connectToServer(host, port string) (net.Conn, error) {
    conn, err := net.Dial("tcp", host+":"+port)
    if err != nil {
        return nil, fmt.Errorf("failed to connect to %s:%s: %v", host, port, err)
    }
    return conn, nil
}
```

### MySQL Database Standards
```sql
-- Table naming: snake_case
-- Column naming: snake_case
-- Comments for educational context

CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    details TEXT,
    status VARCHAR(50) DEFAULT 'public',
    INDEX idx_status (status)
);

-- Intentional data for CTF challenge
INSERT INTO inventory (item_name, details, status) VALUES 
    ('Router-A', 'Cisco 2901 - IP: 10.0.0.1', 'public'),
    ('Switch-Core', 'HP ProCurve - IP: 10.0.0.2', 'public'),
    ('Firewall-Ext', 'Palo Alto - IP: 192.168.1.1', 'private');
```

## Naming Conventions

### Files and Directories
- **Python files**: snake_case (`server.py`, `setup_db.py`)
- **Go files**: snake_case (`main.go`)
- **Directories**: kebab-case (`skysec-inventory`, `docker-compose`)

### Variables and Functions
- **Python**: snake_case (`xor_key`, `handle_client_connection`)
- **Go**: camelCase for unexported, PascalCase for exported
- **SQL**: snake_case for tables and columns

### Constants
- **All languages**: UPPER_SNAKE_CASE (`XOR_KEY`, `DEFAULT_PORT`)

## Error Handling Patterns

### Python Server
```python
try:
    result = mysql_cursor.execute(query)
    return format_response(result)
except mysql.connector.Error as e:
    if e.errno == 1064:  # Syntax error - give hint to CTF player
        return "EMS Error: Internal processing failure (Code: 1064)"
    else:
        return "EMS Error: Database connection failed"
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    return "EMS Error: Internal server error"
```

### Golang Client
```go
if err != nil {
    fmt.Fprintf(os.Stderr, "Error: %v\n", err)
    os.Exit(1)
}

// Graceful connection handling
defer func() {
    if conn != nil {
        conn.Close()
    }
}()
```

## Security Guidelines (CTF Context)

### Intentional Vulnerabilities
⚠️ **This project contains deliberate security flaws for educational purposes:**

1. **SQL Injection**: Use string concatenation, NOT prepared statements
2. **Hardcoded Secrets**: XOR key must be easily discoverable
3. **Weak Encryption**: Simple XOR + Base64 for reverse engineering

### Implementation Requirements
```python
# CORRECT (Vulnerable) Implementation
query = f"SELECT details FROM inventory WHERE id = '{user_input}' AND status = 'public'"

# WRONG (Secure) Implementation - DO NOT USE
cursor.execute("SELECT details FROM inventory WHERE id = %s AND status = 'public'", (user_input,))
```

### WAF Bypass Patterns
Implement filtering that can be bypassed:
- Block spaces (bypassable with `/**/`)
- Block `UNION` and `SELECT` keywords
- Force Boolean-based blind SQL injection

## Testing and Validation

### Integration Testing Workflow
1. **Start MySQL database** via Docker
2. **Run database setup script** to populate tables
3. **Start Python TCP server** on port 1337
4. **Test Golang client** connects and encrypts properly
5. **Validate SQL injection** vulnerability works as intended
6. **Test intended solution path** with solver script

### Quality Assurance
- Python code follows PEP 8 standards
- Go code passes `go vet` and `go fmt`
- All intentional vulnerabilities documented with comments
- Docker deployment tested on clean system
- Binary reverse engineering path validated

## Documentation Requirements

### Code Comments
```python
# Turkish/English comments for maintainability
def handle_read_command(self, user_input: str) -> str:
    """
    Handle 'read <id>' command with intentional SQL injection vulnerability.
    
    INTENTIONAL VULNERABILITY: Uses string concatenation instead of
    parameterized queries to enable CTF exploitation.
    
    Args:
        user_input: User-provided ID parameter (potentially malicious)
    
    Returns:
        Query results or error message
    """
```

### README Requirements
Each component should include:
- Setup instructions
- Usage examples
- Dependency requirements
- Educational context explanation

---

**Remember**: This is an educational CTF project. Maintain intentional vulnerabilities while following clean code practices for everything else. The goal is teachable, exploitable code that demonstrates real-world security issues.