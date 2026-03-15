# Database Agent Progress Checklist
## Sky-Sec İç Ağ Envanter Sistemi - Database & Server Components

### MySQL Database Setup
- [ ] Create `inventory` table with schema:
  - [ ] `id` (INT AUTO_INCREMENT PRIMARY KEY)
  - [ ] `item_name` (VARCHAR(255))
  - [ ] `details` (TEXT)
  - [ ] `status` (VARCHAR(50)) - 'public' or 'private'
- [ ] Create `secret_vault` table with schema:
  - [ ] `id` (INT AUTO_INCREMENT PRIMARY KEY)
  - [ ] `vault_key` (VARCHAR(255))
  - [ ] `flag_value` (TEXT)
- [ ] Insert sample data into `inventory` table:
  - [ ] (1, 'Router-A', 'Cisco 2901 - IP: 10.0.0.1', 'public')
  - [ ] (2, 'Switch-Core', 'HP ProCurve - IP: 10.0.0.2', 'public')
  - [ ] (3, 'Firewall-Ext', 'Palo Alto - IP: 192.168.1.1', 'private')
- [ ] Insert flag data into `secret_vault` table:
  - [ ] (1, 'master_key', 'FLAG{SkyS3c_L3g4cy_Syst3ms_4r3_D4ng3r0us}')

### Python TCP Server Development
- [ ] Create TCP socket server listening on port 1337
- [ ] Implement protocol decryption (Base64 decode -> XOR with `SkY_S3c_P4ssW0rd_99`)
- [ ] Implement protocol encryption (XOR with `SkY_S3c_P4ssW0rd_99` -> Base64 encode)
- [ ] Add newline termination to all outgoing packets

### Command Implementation
- [ ] Implement `help` command:
  - [ ] Return available commands: `list`, `read <id>`, `whoami`
- [ ] Implement `whoami` command:
  - [ ] Return: `Current User: Guest (Privilege Level: 0)`
- [ ] Implement `list` command:
  - [ ] Execute safe query: `SELECT id, item_name FROM inventory WHERE status = 'public'`
- [ ] Implement `read <id>` command:
  - [ ] **INTENTIONAL VULNERABILITY**: Use string concatenation (NOT prepared statements)
  - [ ] Use vulnerable query: `f"SELECT details FROM inventory WHERE id = '{user_input}' AND status = 'public'"`

### WAF (Web Application Firewall) Implementation
- [ ] Block space characters in user input
- [ ] Block `UNION` keyword (case-insensitive)
- [ ] Block `SELECT` keyword (case-insensitive)
- [ ] Return error message: `EMS Error: Invalid characters detected in ID.` for blocked input
- [ ] Return MySQL syntax error as: `EMS Error: Internal processing failure (Code: 1064)`

### Database Configuration Files
- [ ] Create `setup_db.py` - Database initialization script
- [ ] Create `requirements.txt` - Python dependencies
- [ ] Create `docker-compose.yml` - MySQL and Server deployment
- [ ] Create `server.py` - Main TCP server with MySQL logic

### Code Quality & Security
- [ ] Add Turkish/English comments throughout code
- [ ] Mark intentional vulnerabilities with `# INTENTIONAL VULNERABILITY` comments
- [ ] Ensure clean, readable code structure
- [ ] Test database connection and error handling
- [ ] Verify all sample data is correctly inserted

### Testing & Validation
- [ ] Test legitimate commands work correctly
- [ ] Test WAF blocks forbidden characters/keywords
- [ ] Test SQL injection vulnerability works as intended
- [ ] Test MySQL error handling returns Code: 1064
- [ ] Verify protocol encryption/decryption works correctly
- [ ] Test server handles multiple client connections
- [ ] Test Docker deployment works properly

### File Structure Validation
```
server/
├── requirements.txt     - [ ] Created
├── server.py           - [ ] Created
├── setup_db.py         - [ ] Created
└── docker-compose.yml  - [ ] Created
```

### Final Checks
- [ ] Ensure no database schema files are exposed to contestants
- [ ] Verify only intended vulnerability exists (SQL injection in `read` command)
- [ ] Test complete intended solution path
- [ ] Document any deployment requirements