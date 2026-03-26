use std::io::{self, Write};

fn main() {
    let mut out = io::stdout();

    let xor_keys = vec![0x1a, 0x69, 0xe5, 0x02, 0x91, 0xde, 0x66, 0x53, 0x3e, 0x77, 0xd4, 0x6a, 0x89, 0x93, 0x64, 0x54];
    
    let s_box: [u8; 16] = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2];

    let expected = vec![95, 149, 168, 69, 79, 184, 13, 51, 217, 44, 16, 182, 15, 28, 132, 156, 127, 41, 132, 102, 131, 61, 100, 192, 21, 157, 11, 246, 183, 253, 24, 18, 157];

    write!(out, "Flag'ı giriniz: ").unwrap();
    out.flush().unwrap();

    let mut s = String::new();
    io::stdin().read_line(&mut s).expect("Hata!");
    let inp = s.trim();

    let mut result = Vec::new();
    let mut prev = 0xA5; // Başlangıç vektörü (IV)

    for (idx, &c) in inp.as_bytes().iter().enumerate() {
        let mut nc = c ^ xor_keys[idx % 16] ^ prev;
        
        let high = (nc >> 4) as usize;
        let low = (nc & 0x0F) as usize;
        nc = (s_box[high] << 4) | s_box[low];

        let shift = ((idx % 5) + 1) as u32;
        nc = nc.rotate_left(shift);

        nc = nc.wrapping_add(0x37 ^ (idx as u8));

        result.push(nc);
        prev = nc;
    }

    if expected == result {
        println!("Tebrikler, paslanmamışsınız!");
    } else {
        println!("Hatalı flag, tekrar dene.");
    }

}
