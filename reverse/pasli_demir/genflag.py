xor_keys = [
    0x1a, 0x69, 0xe5, 0x02,
    0x91, 0xde, 0x66, 0x53,
    0x3e, 0x77, 0xd4, 0x6a,
    0x89, 0x93, 0x64, 0x54
]

def rol(val, r):
    r %= 8
    return ((val << r) | (val >> (8 - r))) & 0xff

def ror(val, r):
    r %= 8
    return ((val >> r) | (val << (8 - r))) & 0xff

def generate_expected(flag: str):
    result = []
    data = flag.encode()

    for idx, b in enumerate(data):
        nc = b ^ xor_keys[idx % 16]
        shift = nc & 0xfc

        if idx % 2 == 0:
            nc = rol(nc, shift)
        else:
            nc = ror(nc, shift)

        result.append(nc)

    return result


flag = "SKYDAYS{isl3yen_d3mir_pas_tutm4z}"
expected = generate_expected(flag)

print(expected)

