# Client Agent Progress Checklist
## Sky-Sec İç Ağ Envanter Sistemi - Client Component

### Golang CLI Application Setup
- [ ] Initialize Go module with `go.mod`
- [ ] Set up main application structure
- [ ] Import required packages (net, encoding/base64, flag, fmt, bufio, etc.)

### Command Line Interface
- [ ] Implement command-line argument parsing:
  - [ ] `-h` flag for host/IP address (e.g., 127.0.0.1)
  - [ ] `-p` flag for port (e.g., 1337)
- [ ] Add help/usage information for command-line flags
- [ ] Validate required arguments are provided

### Network Communication
- [ ] Implement TCP socket connection to server
- [ ] Handle connection errors gracefully
- [ ] Implement proper connection cleanup/closing

### Encryption/Protocol Implementation
- [ ] Hardcode XOR key: `SkY_S3c_P4ssW0rd_99`
- [ ] Implement XOR encryption function
- [ ] Implement Base64 encoding function
- [ ] Implement complete protocol: Message -> XOR -> Base64
- [ ] Implement protocol decryption: Base64 -> XOR -> Message
- [ ] Add newline character termination to outgoing packets

### User Interface
- [ ] Display `EMS>` prompt (Evidence Management System)
- [ ] Implement interactive command input loop
- [ ] Handle user input reading (with proper error handling)
- [ ] Display server responses to user

### Message Processing
- [ ] Encrypt user input before sending to server
- [ ] Send encrypted message over TCP connection
- [ ] Receive and decrypt server responses
- [ ] Display decrypted responses to user

### Error Handling
- [ ] Handle network connection failures
- [ ] Handle encryption/decryption errors
- [ ] Handle malformed server responses
- [ ] Provide meaningful error messages to user
- [ ] Graceful exit on critical errors

### Code Quality & Reverse Engineering Considerations
- [ ] Add Turkish/English comments for maintainability
- [ ] Ensure XOR key is easily discoverable through reverse engineering
- [ ] Structure code to be analyzable with tools like Ghidra/IDA
- [ ] Keep encryption logic simple and identifiable
- [ ] Use standard Go practices for readability

### Binary Compilation & Distribution
- [ ] Test compilation on target platform
- [ ] Create statically linked binary for distribution
- [ ] Test binary works independently (no external dependencies)
- [ ] Verify binary size is reasonable for distribution

### Testing & Validation
- [ ] Test connection to server with valid host/port
- [ ] Test protocol encryption/decryption works correctly
- [ ] Test user interface responds properly to input
- [ ] Test all supported commands work through client:
  - [ ] `help` command
  - [ ] `whoami` command
  - [ ] `list` command
  - [ ] `read <id>` command
- [ ] Test error conditions (server down, invalid input, etc.)
- [ ] Test client handles server disconnection gracefully

### Security Considerations (for CTF)
- [ ] Ensure XOR key is stored in plaintext (not obfuscated)
- [ ] Verify protocol implementation is straightforward to reverse engineer
- [ ] Test that Base64 and XOR operations are visible in disassembly
- [ ] Ensure no debug information is accidentally included

### File Structure Validation
```
client/
├── main.go    - [ ] Created
└── go.mod     - [ ] Created
```

### Final Distribution Preparation
- [ ] Compile final binary for target architecture
- [ ] Test binary on clean system (no Go installation)
- [ ] Verify binary filename follows convention: `skysec_client`
- [ ] Ensure only binary is distributed (no source code)
- [ ] Test complete user workflow from binary execution to server interaction

### Integration Testing
- [ ] Test complete workflow: client -> server -> database
- [ ] Verify all intended functionality works end-to-end
- [ ] Test that SQL injection vulnerability is exploitable through client
- [ ] Confirm reverse engineering path is feasible