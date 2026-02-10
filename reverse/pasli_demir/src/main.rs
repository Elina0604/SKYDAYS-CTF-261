use std::io::Write;


fn main() {
    // let mut xor_keys = std::vec::Vec::<u8>::new();
    // xor_keys.reserve(16);
    let xor_keys = vec![0x1a, 0x69, 0xe5, 0x02, 0x91, 0xde, 0x66, 0x53, 0x3e, 0x77, 0xd4, 0x6a, 0x89, 0x93, 0x64, 0x54];
    let expected = vec![73, 34, 203, 100, 208, 120, 83, 40, 117, 64, 184, 89, 240, 111, 10, 11, 231, 90, 136, 107, 227, 129, 97, 50, 212, 40, 160, 241, 223, 239, 80, 226, 118];

    let mut s = String::new();

    println!("Flag'ı giriniz: ");

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

    println!("Tebrikler, paslanmamışsınız. Birden fazla flag olabilir ancak sadece biri doğru ;)");

}
