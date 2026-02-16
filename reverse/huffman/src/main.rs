use rand::prelude::*;
use std::collections::BinaryHeap;
use std::io::{self, Write};

#[derive(Debug)]
struct PQItem {
    weight: u32,
    node: HufNode,
}

impl Ord for PQItem {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        other.weight.cmp(&self.weight)   // min-heap için ters
    }
}
impl PartialOrd for PQItem {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}
impl PartialEq for PQItem {
    fn eq(&self, other: &Self) -> bool {
        self.weight == other.weight
    }
}
impl Eq for PQItem {}

#[derive(Debug)]
enum HufNode {
    Leaf(char),
    Node(Box<HufNode>, Box<HufNode>),
}

struct HufKey {
    key: char,
    value: u8,
}

impl HufKey {
    fn rand(key: char) -> Self {
        let mut rng = rand::rng();

        Self {
            key,
            value: rng.random::<u8>(),
        }
    }
}

fn build_huffman(keys: Vec<HufKey>) -> HufNode {
    let mut heap = BinaryHeap::new();

    for k in keys {
        heap.push(PQItem {
            weight: k.value as u32,
            node: HufNode::Leaf(k.key),
        });
    }

    while heap.len() > 1 {
        let left = heap.pop().unwrap();
        let right = heap.pop().unwrap();

        heap.push(PQItem {
            weight: left.weight + right.weight,
            node: HufNode::Node(Box::new(left.node), Box::new(right.node)),
        });
    }

    heap.pop().unwrap().node
}

fn decode_bits(root: &HufNode, bits: &str) -> Option<String> {
    let mut output = String::new();
    let mut node = root;

    for b in bits.chars() {
        // 0 → sağ, 1 → sol
        match (b, node) {
            ('0', HufNode::Node(_, right)) => {
                node = right;
            }
            ('1', HufNode::Node(left, _)) => {
                node = left;
            }
            _ => {
                return None;
            }
        }

        // Yaprak düğüme ulaştık
        if let HufNode::Leaf(c) = node {
            output.push(*c);
            node = root; // tekrar root'tan devam edilir
        }
    }

    Some(output)
}

#[cfg(feature = "dev")]
fn print_leaf_codes(node: &HufNode, prefix: String) {
    let mut out = std::io::stdout();

    match node {
        HufNode::Leaf(c) => {
            write!(out, "{} = {}\n", c, prefix).unwrap();
            out.flush().unwrap();
        }
        HufNode::Node(left, right) => {
            // sol = 1
            print_leaf_codes(left, format!("{}1", prefix));
            // sağ = 0
            print_leaf_codes(right, format!("{}0", prefix));
        }
    }
}

fn print_keys(key: &Vec<HufKey>) {
    let mut out = std::io::stdout();

    for k in key {
        write!(out, "{}({})\n", k.key, k.value).unwrap();
        out.flush().unwrap();
    }
}

fn read_input(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap(); // Prompt hemen yazılsın

    let mut buf = String::new();
    io::stdin().read_line(&mut buf).expect("input okunamadı");
    buf.trim().to_string()
}

fn get_flag() -> String {
    std::fs::read_to_string("flag.txt")
        .expect("FLAG DOSYASI DOCKER ICINDE DEGIL HEMEN ENSAR'I CAGIRIN ACIL")
}

fn get_secret_flag() -> String {
    std::fs::read_to_string("secret")
        .expect("DEVDEVDEV")
}

fn handle_secret(_secret: &[u8]) -> String {
    get_secret_flag()
}

pub fn run_fake_shell(cmd: &str) -> Option<String> {
    match cmd {
        "help" => Some("Komutlar: help, echo, whoami, exit, flag\nBelkide daha fazlası.".to_string()),
        c if c.starts_with("echo ") => Some(c[5..].to_string()),
        "whoami" => Some("huffman".to_string()),
        "flag" => Some(get_flag()),
        c if c.starts_with("secret") => Some(handle_secret(c[7..].as_bytes())),
        "exit" => None,
        _ => Some(format!("Bilinmeyen komut: {}", String::from_utf8_lossy(cmd.as_bytes()))),
    }
}

fn main() {
    // set_hook();
    let mut out = std::io::stdout();

    write!(out, "Zip nasıl çalışıyor öğrendim.\n\
        Hemen sorusunu yazdım.\n\
        İşte kullandığım karakterlerin sıklığı:\n").unwrap();
    out.flush().unwrap();

    let mut az: Vec<HufKey> = ('a'..='z')
        .map(HufKey::rand)
        .collect();

    az.push(HufKey::rand(' '));
    az.push(HufKey::rand('-'));

    print_keys(&az);
    let node = build_huffman(az);

    #[cfg(feature = "dev")]
    print_leaf_codes(&node, "".to_string());

    loop {
        let inp = read_input("huffman@SKYDAYS:/$ ");
        match decode_bits(&node, &inp) {
            Some(cmd) => {
                match run_fake_shell(&cmd) {
                    Some(output) => {
                        write!(out, "{}\n", output).unwrap();
                        out.flush().unwrap();
                    },
                    None => {
                        break;
                    },
                }
            },
            None => {
                write!(out, "Geçersiz giriş! Sadece binary! (001101010)\n").unwrap();
                out.flush().unwrap();
                break;
            },
        }
    }
}
