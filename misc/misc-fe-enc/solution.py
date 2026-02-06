#!/usr/bin/env python3
"""
CTF Python Solution Script
Brooklyn 99 Heist Challenge Solver

This script demonstrates how to solve the CTF using Python
after obtaining the encryption parameters from the browser.
"""

import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def solve_ctf():
    """
    Solve the Brooklyn 99 CTF Challenge

    Prerequisites:
    1. Complete Phase 1: Find login password "DijitalCorba" from source code
    2. Phase 2: Extract encryption parameters from browser console:
       - window.PERALTA_SECRET_KEY
       - window.IV_VALUE
       - Encrypted flag from console output
    """

    # Step 1: Parameters found from browser DevTools/Console
    key = "YTU_TEKNOPARK_99_NINE_NINE"  # from window.PERALTA_SECRET_KEY
    iv = "TERRY_LOVES_YOGURT"  # from window.IV_VALUE
    encrypted_flag = "0zhFrJXRebjn/KokmYkHy+47g4g/RSkv5Js6ul+NkYaxn4P75ymvsWdelFkj26YP"

    print("🔍 Brooklyn 99 CTF - Python Solution")
    print("=" * 50)
    print(f"🔑 Key: {key}")
    print(f"🔀 IV: {iv}")
    print(f"🔒 Encrypted Flag: {encrypted_flag}")
    print()

    # Step 2: Prepare key and IV (match CryptoJS behavior)
    # CryptoJS pads/truncates to required sizes
    key_bytes = key.encode("utf-8")[:32].ljust(32, b"\x00")  # AES-256 needs 32 bytes
    iv_bytes = iv.encode("utf-8")[:16].ljust(16, b"\x00")  # CBC mode needs 16 bytes

    print("🔧 Processing encryption parameters...")
    print(f"   Key length: {len(key_bytes)} bytes")
    print(f"   IV length: {len(iv_bytes)} bytes")
    print()

    try:
        # Step 3: Decrypt the flag
        encrypted_data = base64.b64decode(encrypted_flag)

        # Initialize AES cipher in CBC mode
        cipher = Cipher(
            algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend()
        )
        decryptor = cipher.decryptor()

        # Decrypt
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

        # Step 4: Remove PKCS7 padding
        padding_length = decrypted_padded[-1]
        decrypted_data = decrypted_padded[:-padding_length]

        # Step 5: Convert to string
        flag = decrypted_data.decode("utf-8")

        print("🎉 SUCCESS! Flag found:")
        print(f"🏆 {flag}")
        print()
        print("✅ Heist completed! The sacred 850 bus card is yours!")

        return flag

    except Exception as e:
        print(f"❌ Decryption failed: {e}")
        print(
            "💡 Make sure you have the correct key, IV, and encrypted flag from the browser."
        )
        return None


def alternative_cryptojs_method():
    """
    Alternative method using the same approach as the browser console
    This mimics the window.decryptEvidence() function
    """
    print("\n" + "=" * 50)
    print("🔄 Alternative Method (Browser Console Style)")
    print("=" * 50)

    # You can also use pycryptodome library which is closer to CryptoJS
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        import base64

        key = "YTU_TEKNOPARK_99_NINE_NINE".encode("utf-8")[:32].ljust(32, b"\x00")
        iv = "TERRY_LOVES_YOGURT".encode("utf-8")[:16]
        encrypted_flag = (
            "0zhFrJXRebjn/KokmYkHy+47g4g/RSkv5Js6ul+NkYaxn4P75ymvsWdelFkj26YP"
        )

        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = base64.b64decode(encrypted_flag)
        decrypted = cipher.decrypt(encrypted_data)
        flag = unpad(decrypted, AES.block_size).decode("utf-8")

        print(f"🏆 Flag (using pycryptodome): {flag}")

    except ImportError:
        print("💡 To use this method, install: pip install pycryptodome")
        print("   This provides a CryptoJS-like interface")


flag = solve_ctf()
print(flag)
# Alternative method (if pycryptodome is available)
alternative_cryptojs_method()

print("\n" + "=" * 50)
print("📝 Solution Summary:")
print("=" * 50)
print("Phase 1: Login bypass")
print("  - Find base64 encoded password in source code")
print("  - Decode 'RGlqaXRhbENvcmJh' → 'DijitalCorba'")
print()
print("Phase 2: AES decryption")
print("  - Extract key/IV from browser console global variables")
print("  - Use Python AES decryption or browser console")
print("  - Both methods lead to the same flag!")
print()
print("🎯 This CTF teaches: Client-side security is not security!")
