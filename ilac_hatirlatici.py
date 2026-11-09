from datetime import datetime


def hatirlatici_ekle(hatirlaticilar):
    """Kullanıcıdan bilgi alır, doğrular ve hatırlatıcıyı listeye ekler."""
    ad = input("İlaç/tedavi adı: ").strip()

    if not ad:
        print("Uyarı: Ad boş bırakılamaz.")
        return

    saat = input("Saat (HH:MM, örnek 08:30): ").strip()

    try:
        if len(saat) != 5 or saat[2] != ":":
            raise ValueError
        datetime.strptime(saat, "%H:%M")
    except ValueError:
        print("Uyarı: Geçerli bir saat gir. Örnek: 08:30")
        return

    print("Tekrar türü:")
    print("1. Tek seferlik")
    print("2. Günlük")
    tekrar_secimi = input("Seçimin (1/2): ").strip()

    if tekrar_secimi == "1":
        tekrar = "Tek seferlik"
    elif tekrar_secimi == "2":
        tekrar = "Günlük"
    else:
        print("Uyarı: Tekrar türü için 1 veya 2 seçmelisin.")
        return

    hatirlaticilar.append({
        "ad": ad,
        "saat": saat,
        "tekrar": tekrar,
    })
    print("Hatırlatıcı eklendi.")


def hatirlaticilari_goster(hatirlaticilar):
    """Kayıtlı hatırlatıcıları ekrana düzenli biçimde yazdırır."""
    if not hatirlaticilar:
        print("Henüz kayıtlı hatırlatıcı yok.")
        return

    print("\n--- Hatırlatıcılar ---")
    for sira, hatirlatici in enumerate(hatirlaticilar, start=1):
        print(
            f"{sira}. {hatirlatici['saat']} - "
            f"{hatirlatici['ad']} ({hatirlatici['tekrar']})"
        )


def dosyaya_kaydet(hatirlaticilar):
    """Hatırlatıcıları metin dosyasına kaydeder."""
    try:
        with open("hatirlaticilar.txt", "w", encoding="utf-8") as dosya:
            dosya.write("İLAÇ / TEDAVİ HATIRLATICI PLANI\n")
            dosya.write("=" * 34 + "\n")

            if not hatirlaticilar:
                dosya.write("Henüz kayıtlı hatırlatıcı yok.\n")
            else:
                for sira, hatirlatici in enumerate(hatirlaticilar, start=1):
                    dosya.write(
                        f"{sira}. {hatirlatici['saat']} - "
                        f"{hatirlatici['ad']} ({hatirlatici['tekrar']})\n"
                    )

        print("Hatırlatıcılar hatirlaticilar.txt dosyasına kaydedildi.")
    except OSError as hata:
        print(f"Dosya kaydedilemedi: {hata}")


def ana_program():
    hatirlaticilar = []

    while True:
        print("\n=== İlaç / Tedavi Hatırlatıcı Planlayıcı ===")
        print("1. Hatırlatıcı ekle")
        print("2. Hatırlatıcıları göster")
        print("3. Dosyaya kaydet")
        print("0. Çıkış")

        secim = input("Seçimin: ").strip()

        if secim == "1":
            hatirlatici_ekle(hatirlaticilar)
        elif secim == "2":
            hatirlaticilari_goster(hatirlaticilar)
        elif secim == "3":
            dosyaya_kaydet(hatirlaticilar)
        elif secim == "0":
            print("Program kapatıldı.")
            break
        else:
            print("Uyarı: Menüden 0, 1, 2 veya 3 seçmelisin.")


if __name__ == "__main__":
    ana_program()
