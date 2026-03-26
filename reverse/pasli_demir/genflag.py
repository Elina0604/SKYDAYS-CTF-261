def rotate_left(n, d):
    d %= 8
    return ((n << d) & 0xFF) | (n >> (8 - d))

def generate():
    xor_keys = [0x1a, 0x69, 0xe5, 0x02, 0x91, 0xde, 0x66, 0x53, 0x3e, 0x77, 0xd4, 0x6a, 0x89, 0x93, 0x64, 0x54]
    s_box = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
    
    try:
        with open("flag.txt", "r") as f:
            flag = f.read().strip()
    except:
        print("flag.txt bulunamadı!")
        return

    expected = []
    prev = 0xA5
    
    for i, char in enumerate(flag):
        c_val = ord(char)
        nc = (c_val ^ xor_keys[i % 16] ^ prev) & 0xFF
        
        high = nc >> 4
        low = nc & 0x0F
        nc = (s_box[high] << 4) | s_box[low]
        
        shift = (i % 5) + 1
        nc = rotate_left(nc, shift)
        
        nc = (nc + (0x37 ^ i)) & 0xFF
        
        expected.append(nc)
        prev = nc
        
    print(f"Rust 'expected' dizisi:\n{expected}")

if __name__ == "__main__":
    generate()
