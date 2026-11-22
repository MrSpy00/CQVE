# CQVE (Experimental / Educational Cryptography Exercise)

> **UYARI / WARNING:** Bu proje **yalnızca eğitim ve deneysel amaçlı** yazılmış özel bir şifreleme denemesidir. **Production ortamında, gerçek veri güvenliği veya hassas iletişim için KULLANMAYIN.** Gerçek uygulamalar için AES-GCM, ChaCha20-Poly1305 ve Argon2id gibi standart, doğrulanmış kütüphaneleri (`cryptography`, `libsodium`, OpenMLS vb.) kullanın.
>
> *This repository is an **experimental, educational exercise** (late 2025). **Do NOT use it in production** or for real confidentiality. Use audited standard primitives such as AES-GCM, ChaCha20-Poly1305, and Argon2id instead.*

![Status](https://img.shields.io/badge/Status-Experimental%20%2F%20Educational-orange.svg)
![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## Nedir / Ne Değildir?

`CQVE.py`, kriptografik yapı taşlarını (blok şifreleme turları, permütasyon, tuzlama ve Encrypt-then-MAC) sıfırdan Python ile denemek amacıyla yazılmış bir CLI prototipidir. Kod içindeki sınıf ve metot isimleri ("Quantum Vortex", "Lattice", "Fluid Diffusion") erken dönem deneysel adlandırmalardır; gerçekte kuantum dirençli kafes (lattice) veya kaos matematiği içermez.

### Kodun Gerçekte Uyguladığı Yapı (`CQVE.py`)

| Bileşen | Kodda Gerçekte Kullanılan Yöntem | Güvenlik Notu |
|---|---|---|
| **Anahtar Türetme (KDF)** | Tek geçiş `SHAKE-256(SHA3-512(password + salt + timestamp))` | PBKDF2/Argon2 iterasyonu veya bellek zorluğu yoktur; parola tahmin saldırılarına açıktır. |
| **Blok Dönüşümü** | 64-bit bloklar üzerinde 64 turlu Feistel ağı (`rotl5 * 2654435761`) | Eğitim amaçlı özel round fonksiyonudur; standart blok şifrelerin (AES) yerini tutmaz. |
| **Akış Katmanı (`_lattice_transform`)** | Lineer Eşlenik Üreteç (LCG: `(k * 1664525 + 1013904223) % 256`) ile toplamsal bayt kaydırma | Kafes kriptografisi değildir; LCG kriptografik olarak güvenli değildir. |
| **Permütasyon (`_fluid_diffusion`)** | `random.Random(seed).shuffle(indices)` (Mersenne Twister) | `random` modülü CSPRNG değildir; yalnızca bayt yer değiştirme (transpozisyon) yapar. |
| **Bütünlük & Tuzlama** | `os.urandom(32)` salt + şifreli metin üzerinde `HMAC-SHA3-512` (`hmac.compare_digest`) | Standart Encrypt-then-MAC yaklaşımıdır. |

---

## Kurulum ve Çalıştırma (Yalnızca İnceleme / Test İçin)

Harici bağımlılık gerektirmez, Python 3 standart kütüphaneleriyle çalışır:

```bash
git clone https://github.com/MrSpy00/CQVE.git
cd CQVE
python CQVE.py
```

*Not: Proje erken dönem bir öğrenme çalışmasıdır. Güncel kriptografi kullanımım için standart OpenMLS, Double Ratchet ve AES-256-GCM kullanan [veilanon](https://github.com/MrSpy00/veilanon) projesine bakabilirsiniz.*
