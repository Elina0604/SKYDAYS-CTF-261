#!/usr/bin/env python3

def rotate_left(n, d):
    d %= 8
    return ((n << d) & 0xFF) | (n >> (8 - d))

def solve():
    xor_keys = [0x1a, 0x69, 0xe5, 0x02, 0x91, 0xde, 0x66, 0x53, 0x3e, 0x77, 0xd4, 0x6a, 0x89, 0x93, 0x64, 0x54]
    s_box = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
    
    expected = [95, 149, 168, 69, 79, 184, 13, 51, 217, 44, 16, 182, 15, 28, 132, 156, 127, 41, 132, 102, 131, 61, 100, 192, 21, 157, 11, 246, 183, 253, 24, 18, 157]

    flag = ""
    prev = 0xA5
    
    for i, target in enumerate(expected):
        shift = (i % 5) + 1
        key = xor_keys[i % 16]
        found = False
        
        for char_code in range(256):
            nc = (char_code ^ key ^ prev) & 0xFF
            
            high = nc >> 4
            low = nc & 0x0F
            nc_s = (s_box[high] << 4) | s_box[low]
            
            res = rotate_left(nc_s, shift)
            res = (res + (0x37 ^ i)) & 0xFF
            
            if res == target:
                flag += chr(char_code)
                prev = target
                found = True
                break
        
        if not found:
            flag += "?"
            
    print(f"Bulunan Flag: {flag}")

if __name__ == "__main__":
    solve()
