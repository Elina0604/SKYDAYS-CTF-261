use std::io::Write;


fn main() {
    // let mut xor_keys = std::vec::Vec::<u8>::new();
    // xor_keys.reserve(16);
    let xor_keys = vec![0x1a, 0x69, 0xe5, 0x02, 0x91, 0xde, 0x66, 0x53, 0x3e, 0x77, 0xd4, 0x6a, 0x89, 0x93, 0x64, 0x54];
    let expected = vec![73, 34, 203, 65, 92, 152, 209, 98, 212, 27, 126, 19, 206, 223, 32, 49, 214, 88, 121, 82, 90, 218, 50, 98, 74, 26, 224, 16, 79];

    let mut s = String::new();

    let _ = std::io::stdout().flush();
    std::io::stdin().read_line(&mut s)
        .expect("Failed to read user input!");

    let mut result = std::vec::Vec::<u8>::new();

    let inp = s.trim();

    let mut idx = 0;
    for c in inp.as_bytes() {
        let mut nc = c.clone();
        nc ^= xor_keys[idx % 16];
        let shift = nc & 0xfc;

        if (idx % 2) == 0 {
            // rotate-left
            nc = nc.rotate_left(shift as u32);
        } else {
            // rotate-right
            nc = nc.rotate_right(shift as u32);
        }

        result.push(nc);

        idx += 1;
    }

    assert!(expected == result, "en fazla DoS olurum");

    println!("Tebrikler, paslanmamışsınız!");

}
