
docker calistir:
```
docker build -t whatlibc .

docker run --privileged -p 1337:1337 -it whatlibc
```

yarismaciya verilecekler:

```
./solve
./libc/ld-linux-x86-64.so.2
./libc/libc.so.6
```

ayrica, exploit.py'yi REMOTE ile calistirirsaniz localhost:1337'den deneyecekir
```
python3 exploit.py REMOTE
```

