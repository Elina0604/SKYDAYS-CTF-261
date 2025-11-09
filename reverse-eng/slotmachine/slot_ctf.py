import random

FLAG = "skydays{bu_bir_hacklenmis_slot_makinesi_algoritmasi}"

def slot_cheater_ctf():
    bakiye = 100
    print("✨ SADECE HİLE YAPANLAR İÇİN SLOT MAKİNESİ ✨")
    print("100$ ile başlıyorsunuz. Amacınız: 1000$'a ulaşmak.")

    try:
        isim = input("\nLütfen bir kullanıcı kodu girin (herhangi bir string olabilir): ")
        seed_input = sum(ord(char) for char in isim)
        seed_degeri = seed_input % 256
    except Exception:
        print("Geçersiz giriş. Çıkılıyor.")
        return

    random.seed(seed_degeri)
    KAZANMA_SAYISI = 7
    KAZANMA_CEVIRMESI = 3

    while bakiye > 0 and bakiye < 1000:
        print(f"\n💰 Mevcut Bakiyeniz: ${bakiye}")
        try:
            bahis = int(input("🎰 Bahis miktarınızı girin (1-10$): "))
        except ValueError:
            print("Geçersiz giriş.")
            continue

        if not (1 <= bahis <= 10) or bahis > bakiye:
            print("Geçersiz bahis miktarı veya yetersiz bakiye.")
            continue

        bakiye -= bahis

        sonuclar = []
        for _ in range(KAZANMA_CEVIRMESI):
            sayi = random.randint(1, 9)
            sonuclar.append(sayi)

        print(f"Çevirme Sonucu: {sonuclar}")

        if sonuclar == [KAZANMA_SAYISI] * KAZANMA_CEVIRMESI:
            kazanc = bahis * 100
            bakiye += kazanc
            print(f"🎉 JACKPOT! ${kazanc} kazandınız! 🍀")
        elif sonuclar[0] == sonuclar[1] or sonuclar[1] == sonuclar[2]:
            kazanc = bahis * 2
            bakiye += kazanc
            print(f"💰 Küçük İkramiye! ${kazanc} kazandınız.")
        else:
            print("Kasa kazandı. Tekrar deneyin.")

    if bakiye >= 1000:
        print("\n🏆 TEBRİKLER! Makinenin sırrını çözdünüz ve kasayı boşalttınız!")
        print(f"🔑 Bayrağınız: {FLAG}")
    else:
        print("\nOyun Bitti. Bakiyeniz tükendi. İyi şanslar bir dahaki sefere!")

if __name__ == "__main__":
    slot_cheater_ctf()
