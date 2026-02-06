# Rust

build etmek için rust lazım

```
# Deploy için build
cargo build --release

# Huffman'ı print etmek (dev) build
cargo build --release --features dev
```

# Flag

iki tane flag dosyası olacak:

`flag.txt` ve `secret`

# Docker build etme:

`docker build -t huffmand .`

# Docker çalıştırma

mount işlemi vs için capability gerekiyor, başka bir yolu var mı bilmiyorum ama şu anlık capabilit'ler ile çalıştırmalıyız:

`docker run --rm --cap-add=SYS_ADMIN --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -p 9002:1337 --name huffman huffmand`

Dikkat ederseniz, bu komut `-d`eteach modda çalışmıyor, istenilirse `-d` eklenebilir.

