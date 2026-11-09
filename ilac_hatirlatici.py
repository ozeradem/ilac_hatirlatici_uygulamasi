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
        print_hatirlatici(sira, hatirlatici)


def print_hatirlatici(sira, hatirlatici):
    print(
        f"{sira}. {hatirlatici['saat']} - "
        f"{hatirlatici['ad']} ({hatirlatici['tekrar']})"
    )


def hatirlatici_sec(hatirlaticilar, islem):
    """Düzenlenecek veya silinecek hatırlatıcıyı seçer."""
    if not hatirlaticilar:
        print("İşlem yapılabilecek kayıtlı hatırlatıcı yok.")
        return None

    hatirlaticilari_goster(hatirlaticilar)
    secim = input(f"{islem} için sıra numarası (iptal için 0): ").strip()

    try:
        sira = int(secim)
    except ValueError:
        print("Uyarı: Geçerli bir sıra numarası gir.")
        return None

    if sira == 0:
        print("İşlem iptal edildi.")
        return None
    if sira < 1 or sira > len(hatirlaticilar):
        print("Uyarı: Bu sıra numarasında bir hatırlatıcı yok.")
        return None

    return sira - 1


def hatirlatici_duzenle(hatirlaticilar):
    """Seçilen hatırlatıcının bilgilerini günceller."""
    sira = hatirlatici_sec(hatirlaticilar, "Düzenleme")
    if sira is None:
        return

    mevcut = hatirlaticilar[sira]
    ad = input(f"İlaç/tedavi adı [{mevcut['ad']}]: ").strip() or mevcut["ad"]
    saat_girdisi = input(f"Saat HH:MM [{mevcut['saat']}]: ").strip()

    if saat_girdisi:
        try:
            if len(saat_girdisi) != 5 or saat_girdisi[2] != ":":
                raise ValueError
            datetime.strptime(saat_girdisi, "%H:%M")
        except ValueError:
            print("Uyarı: Geçerli bir saat gir. Örnek: 08:30")
            return
        saat = saat_girdisi
    else:
        saat = mevcut["saat"]

    print("Tekrar türü (boş bırakırsan mevcut değer korunur):")
    print("1. Tek seferlik")
    print("2. Günlük")
    tekrar_secimi = input(f"Seçimin [{mevcut['tekrar']}]: ").strip()

    if tekrar_secimi == "1":
        tekrar = "Tek seferlik"
    elif tekrar_secimi == "2":
        tekrar = "Günlük"
    elif not tekrar_secimi:
        tekrar = mevcut["tekrar"]
    else:
        print("Uyarı: Tekrar türü için 1 veya 2 seçmelisin.")
        return

    hatirlaticilar[sira] = {"ad": ad, "saat": saat, "tekrar": tekrar}
    print("Hatırlatıcı güncellendi.")


def hatirlatici_sil(hatirlaticilar):
    """Seçilen hatırlatıcıyı onaydan sonra siler."""
    sira = hatirlatici_sec(hatirlaticilar, "Silme")
    if sira is None:
        return

    hatirlatici = hatirlaticilar[sira]
    onay = input(
        f"{hatirlatici['ad']} hatırlatıcısı silinsin mi? (E/H): "
    ).strip().lower()
    if onay == "e":
        del hatirlaticilar[sira]
        print("Hatırlatıcı silindi.")
    else:
        print("Silme işlemi iptal edildi.")


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
        print("4. Hatırlatıcı düzenle")
        print("5. Hatırlatıcı sil")
        print("0. Çıkış")

        secim = input("Seçimin: ").strip()

        if secim == "1":
            hatirlatici_ekle(hatirlaticilar)
        elif secim == "2":
            hatirlaticilari_goster(hatirlaticilar)
        elif secim == "3":
            dosyaya_kaydet(hatirlaticilar)
        elif secim == "4":
            hatirlatici_duzenle(hatirlaticilar)
        elif secim == "5":
            hatirlatici_sil(hatirlaticilar)
        elif secim == "0":
            print("Program kapatıldı.")
            break
        else:
            print("Uyarı: Menüden 0, 1, 2, 3, 4 veya 5 seçmelisin.")


if __name__ == "__main__":
    ana_program()
