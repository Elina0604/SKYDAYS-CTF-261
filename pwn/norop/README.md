
docker calistir:
```
docker build -t norop .

docker run --privileged -p 1337:1337 norop
```

Bu soru için not (yarışmacıya verilecek):
```
Bu soruda basit bir Shadow Stack mekanizması simüle edilmiştir.
Klasik ROP çözümü başarısız olacaktır.

Verilen vuln binary'si bir debugger altında çalıştırılmaktadır. Debugger, tüm CALL ve RET instruction'larını izleyerek gerekli PUSH ve POP işlemlerini simüle eder. Shadow stack ile gerçek stack arasında bir uyumsuzluk tespit edildiğinde program sonlandırılır.

Binary debugger altında çalıştığı için remote bağlantıda program oldukça yavaş olabilir (ilk çıktının gelmesi ~30 saniye sürebilir).

Verilen libc ve ld ile kararlı bir exploit geliştirerek flag'a erişebilirsiniz.
```

yarismaciya verilecekler:

```
./vuln
./libc/ld-linux-x86-64.so.2
./libc/libc.so.6
```

ayrica, exploit.py'yi REMOTE ile calistirirsaniz localhost:1337'den deneyecekir
```
python3 exploit.py REMOTE
```

