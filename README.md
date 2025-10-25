# 🧠 Facebook AutoPost - Desktop App (Python GUI)

Aplikasi desktop sederhana untuk **auto posting ke Facebook Page** menggunakan **Facebook Graph API**.  
Dibuat dengan **Python + Tkinter**, menampilkan **progress bar, log realtime**, dan **penundaan acak antar posting** agar terlihat natural.

---

## 🚀 Fitur Utama

- Input **Page ID** dan **Access Token** langsung dari GUI  
- Upload file **produk JSON**  
- Posting otomatis ke halaman Facebook  
- Menampilkan **thumbnail (OG link)** otomatis  
- Log aktivitas lengkap  
- Progress bar posting  
- Delay acak antar posting (bisa diatur)  
- Deteksi token invalid / expired  

---

## 🧩 Struktur Proyek

```
facebook_autopost/
│
├── facebook_autopost.py     # Script utama aplikasi GUI
├── produk25102025.json      # Contoh file produk (input)
├── app.ico                  # (opsional) Icon aplikasi
├── README.md                # Dokumentasi ini
└── dist/                    # Folder hasil build (.exe)
```

---

## 📦 Instalasi & Menjalankan

### 1️⃣ Instal Dependensi

Pastikan Python 3.10+ sudah terpasang, lalu jalankan:

```bash
pip install requests
```

### 2️⃣ Jalankan Aplikasi

```bash
python facebook_autopost.py
```

Aplikasi GUI akan muncul.  
Isi **Page ID**, **Access Token**, dan pilih file JSON produk → klik **🚀 Mulai Posting**.

---

## 🧰 Build Menjadi File .EXE

Gunakan [PyInstaller](https://pyinstaller.org/en/stable/) untuk membungkus menjadi aplikasi Windows:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --icon=app.ico facebook_autopost.py
```

Hasilnya akan berada di:
```
dist/facebook_autopost.exe
```

---

## 📁 Format File JSON

Pastikan file JSON berisi daftar produk seperti contoh berikut:

```json
[
  {
    "Nama Produk": "Setelan Anak Perempuan Katun",
    "Harga": "56,0RB",
    "Penjualan": "27",
    "Nama Toko": "Toko Ceria",
    "Komisi": "5%",
    "Komisi hingga": "10%",
    "Link Komisi Ekstra": "https://shope.ee/xxxx"
  },
  {
    "Nama Produk": "Kaos Pria Dewasa",
    "Harga": "80,0RB",
    "Penjualan": "13",
    "Nama Toko": "FashionStore",
    "Komisi": "4%",
    "Komisi hingga": "9%",
    "Link Komisi Ekstra": "https://tokopedia.link/xxxx"
  }
]
```

---

## 🔐 Token Facebook

Gunakan **Page Access Token** dari [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer/).

> ⚠️ **Catatan:**  
> Token bisa **kedaluwarsa**.  
> Jika aplikasi mendeteksi error `code 190`, kamu perlu memperbarui token.  
> Untuk membuat **token jangka panjang**, ikuti panduan resmi:  
> [https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/)

---

## 🧠 Tips Keamanan

- **Jangan commit token** ke GitHub publik!  
- Simpan token di file lokal `.env` atau `config.json` yang diabaikan oleh `.gitignore`.
- Token adalah kredensial sensitif seperti password.

Contoh `.gitignore`:
```
config.json
.env
autopost.log
__pycache__/
dist/
build/
```

---

## 🧩 Todo / Pengembangan Selanjutnya

- [ ] Fitur refresh token otomatis
- [ ] Simpan konfigurasi (`Page ID`, `Token`, `Delay`) di `config.json`
- [ ] Support multi-page posting
- [ ] Integrasi login OAuth Facebook

---

## 👨‍💻 Pengembang

**Nama:** Pandu Aldi  
**Bahasa:** Python 3.10 + Tkinter  
**Lisensi:** MIT  
**Repository:** [GitHub](https://github.com/yourusername/facebook-autopost-desktop)

---

## 📸 Screenshot

![Preview GUI](docs/screenshot.png)

> GUI sederhana dengan input konfigurasi, progress bar, dan log aktivitas.

---

## ❤️ Terima Kasih

Dibuat dengan niat membantu mempermudah posting otomatis ke Facebook tanpa harus membuka browser.  
Gunakan secara bertanggung jawab dan ikuti [Facebook Platform Policy](https://developers.facebook.com/policy/).

## Dukungan

Kalo kamu suka sama proyek ini dan ngerasa kebantu, boleh banget lho traktir aku kopi! Biar makin semangat ngodingnya!

<a href="https://saweria.co/pandualdi" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me a Coffee" style="height: 41px !important;width: 174px !important;" ></a>
