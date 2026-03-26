#!/usr/bin/env python3
from pwn import *
import re

HOST = "localhost"
PORT = 1337
context.log_level = "info"

class Node:
    def __init__(self, weight, char=None, left=None, right=None):
        self.weight = weight
        self.char = char
        self.left = left
        self.right = right

    # Rust'taki #[derive(Ord)] ve tie-break mantığını simüle ediyoruz
    def __lt__(self, other):
        if self.weight != other.weight:
            return self.weight < other.weight
        
        # Ağırlıklar eşitse: Rust'ta Leaf < Node (enum sırası)
        if self.char is not None and other.char is None:
            return True # Leaf, Node'dan küçüktür
        if self.char is None and other.char is not None:
            return False
        
        # İkisi de Leaf ise: Karakterleri karşılaştır
        if self.char is not None and other.char is not None:
            return self.char < other.char
        
        # İkisi de Node ise: Rust'ta Boxed içerik karşılaştırılır (rekürsif)
        # Genellikle bu seviyeye inilmez ama stabilite için False dönüyoruz
        return False

def build_huffman(freq):
    # Düğümleri oluştur ve başlangıçta sırala
    nodes = [Node(w, c) for c, w in freq.items()]
    
    while len(nodes) > 1:
        # Rust'ın BinaryHeap (Min-priority) mantığı için her adımda sıralıyoruz
        nodes.sort() 
        left = nodes.pop(0)
        right = nodes.pop(0)
        
        # Yeni Node oluştur
        merged = Node(left.weight + right.weight, left=left, right=right)
        nodes.append(merged)
        
    return nodes[0]

def get_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}
    
    if node.char is not None:
        codes[node.char] = prefix
        return codes
    
    # Rust: 1=Left, 0=Right (Rust kodundaki decode_bits ile uyumlu)
    if node.left: get_codes(node.left, prefix + "1", codes)
    if node.right: get_codes(node.right, prefix + "0", codes)
    return codes

def parse_freqs(data):
    """Karakterleri ve frekansları daha güvenli bir şekilde ayıklar."""
    freq = {}
    # Sadece parantezli kısımları hedefle: "karakter(sayı)"
    lines = data.splitlines()
    for line in lines:
        match = re.search(r"(.)\((\d+)\)$", line)
        if match:
            char = match.group(1)
            weight = int(match.group(2))
            freq[char] = weight
    return freq

def main():
    try:
        io = remote(HOST, PORT)
    except:
        log.error("Bağlantı kurulamadı!")
        return

    # Başlangıç verisini ve frekans tablosunu al
    raw_data = io.recvuntil(b"huffman@SKYDAYS:/$ ").decode()
    freq = parse_freqs(raw_data)
    
    if not freq:
        log.error("Frekans tablosu okunamadı!")
        return

    log.info(f"Yakalnan karakter sayısı: {len(freq)}")

    # Ağacı kur ve kodları üret
    root = build_huffman(freq)
    codes = get_codes(root)

    def send_cmd(cmd_str):
        try:
            encoded = "".join(codes[c] for c in cmd_str)
            io.sendline(encoded.encode())
            res = io.recvuntil(b"huffman@SKYDAYS:/$ ").decode()
            # Prompt'u temizle
            return res.replace("huffman@SKYDAYS:/$ ", "").strip()
        except KeyError as e:
            return f"HATA: '{e.args[0]}' karakteri Huffman tablosunda yok!"

    # Otomatik Flag'leri al
    log.success(f"Flag: {send_cmd('flag')}")
    log.success(f"Secret: {send_cmd('secretx')}")

    # İnteraktif Shell
    while True:
        try:
            cmd = input("huffman@SKYDAYS:/$ ")
            if cmd.lower() in ["exit", "quit"]: break
            print(send_cmd(cmd))
        except EOFError:
            break

    io.close()

if __name__ == "__main__":
    main()
