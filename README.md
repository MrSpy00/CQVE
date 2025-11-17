# 🛡️ CQVE - CodexCore Quantum Vortex Engine

![Version](https://img.shields.io/badge/version-3.0-blueviolet.svg)
![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Security](https://img.shields.io/badge/Encryption-Hybrid-red.svg)

> **"Sıradan şifrelemenin ötesinde: Kaotik, Akışkan ve Kırılamaz."**

**CQVE (CodexCore Quantum Vortex Engine)**, standart şifreleme algoritmalarının öngörülebilirliğine meydan okuyan, Python tabanlı, yeni nesil hibrit bir şifreleme protokolüdür. Feistel ağları, Kafes (Lattice) tabanlı gürültü üretimi ve akışkan difüzyon tekniklerini birleştirerek verilerinizi çok katmanlı bir koruma altına alır.

---

## 🚀 Özellikler

### 🔐 3-Katmanlı Kriptografik Çekirdek
CQVE, veriyi tek bir algoritma ile şifrelemek yerine, onu üç farklı matematiksel evrenden geçirir:

1.  **Feistel Network (64 Tur):** Veri blokları, 64 tur boyunca sağ ve sol bloklar arasında karmaşık XOR ve bit kaydırma işlemlerine tabi tutulur.
2.  **Lattice Noise Injection:** Veriye, anahtar türevli matematiksel bir gürültü enjekte edilerek frekans analizi imkansız hale getirilir.
3.  **Fluid Diffusion (Akışkan Difüzyon):** Veri baytları, "Chaos Theory" prensiplerine benzer şekilde, anahtara bağlı rastgelelik ile yeniden konumlandırılır.

### 🛡️ Askeri Düzeyde Bütünlük
* **SHA3-512 & HMAC:** Veri sadece şifrelenmez, aynı zamanda imzalanır. Şifreli metin üzerinde yapılan en ufak bir değişiklik (bit-flip saldırıları), şifre çözme sırasında tespit edilir.
* **Dinamik Tuzlama (Salting):** Her işlemde benzersiz bir `salt` ve `timestamp` kullanılır. Aynı metin ve şifre ile yapılan işlemler bile her seferinde farklı çıktı üretir.

### 💻 Kullanıcı Deneyimi
* **Cross-Platform Pano Desteği:** Windows, Linux ve macOS üzerinde panodan otomatik kopyalama/yapıştırma.
* **Akıllı Dosya Yönetimi:** Çıktıları masaüstüne çakışma olmadan otomatik kaydeder.
* **CLI Arayüzü:** Hacker estetiğine sahip, renkli ve daktilo efektli komut satırı arayüzü.

---

## 📦 Kurulum

Projeyi klonlayın ve çalıştırın. Harici bir kütüphane gerektirmez (Standart Python kütüphaneleri kullanılır).

```bash
git clone [https://github.com/MrSpy00/CQVE.git](https://github.com/MrSpy00/CQVE.git)
cd CQVE
python CQVE.py
