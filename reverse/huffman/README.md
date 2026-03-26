# Rust

build etmek için rust lazım

```
# Deploy için build
cargo build --release
cp ./target/release/huffman ./chal

# Huffman'ı print etmek (dev) build
cargo build --release --features dev

# ya da direkt
./build.sh
```

# Yarışmacıya Verilecek Dosyalar

`chal` dosyası yarışmacıya verilecek.

# Flag

iki tane flag dosyası olacak:

`flag.txt` ve `secret`

bu flaglardan sadece `flag.txt` olanı ctfd'de sunulacak, diğer flag
ise yarışmacı bulduktan sonra bize gösterecek ve puan manuel olarak verilecek.

# Docker build etme:

```
docker build -t huffmand .

docker run --privileged -p 1337:1337 huffmand
```


