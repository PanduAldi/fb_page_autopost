import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import requests
import json
import time
import random
import threading
from datetime import datetime


class FacebookAutoPostApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook AutoPost - Python Desktop")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Variabel input
        self.page_id = tk.StringVar()
        self.access_token = tk.StringVar()
        self.json_path = tk.StringVar()

        # Frame Input
        frame = tk.LabelFrame(root, text="Konfigurasi", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="Page ID:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.page_id, width=50).grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame, text="Access Token:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.access_token, width=50, show="*").grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame, text="File JSON Produk:").grid(row=2, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.json_path, width=50, state="readonly").grid(row=2, column=1, padx=5, pady=2)
        tk.Button(frame, text="Browse...", command=self.browse_json).grid(row=2, column=2, padx=5)

        # Tombol mulai
        self.start_button = tk.Button(root, text="🚀 Mulai Posting", command=self.start_autopost, bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"))
        self.start_button.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=650, mode="determinate")
        self.progress.pack(pady=5)

        # Log box
        log_frame = tk.LabelFrame(root, text="Log Aktivitas", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = tk.Text(log_frame, wrap="word", height=15, state="disabled", bg="#1E1E1E", fg="#00FF00")
        self.log_text.pack(fill="both", expand=True)

        # Default config
        self.delay_min = 120
        self.delay_max = 300

    def browse_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filename:
            self.json_path.set(filename)

    def log(self, message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.log_text.config(state="normal")
        self.log_text.insert("end", timestamp + message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.root.update()

    def start_autopost(self):
        if not self.page_id.get() or not self.access_token.get() or not self.json_path.get():
            messagebox.showerror("Error", "Isi semua field terlebih dahulu!")
            return

        # Nonaktifkan tombol
        self.start_button.config(state="disabled", text="Sedang berjalan...")

        thread = threading.Thread(target=self.run_autopost)
        thread.start()

    def run_autopost(self):
        try:
            with open(self.json_path.get(), "r", encoding="utf-8") as f:
                produk_list = json.load(f)

            if not isinstance(produk_list, list):
                raise ValueError("Format JSON tidak valid")

        except Exception as e:
            self.log(f"❌ Gagal membaca file JSON: {e}")
            self.start_button.config(state="normal", text="🚀 Mulai Posting")
            return

        self.log(f"🚀 Memulai autopost untuk {len(produk_list)} produk...")

        self.progress["value"] = 0
        self.progress["maximum"] = len(produk_list)

        for index, produk in enumerate(produk_list):
            nama = produk.get("Nama Produk", "")
            harga = produk.get("Harga", "")
            penjualan = produk.get("Penjualan", "")
            toko = produk.get("Nama Toko", "")
            komisi = produk.get("Komisi", "")
            komisi_hingga = produk.get("Komisi hingga", "")
            link_komisi = produk.get("Link Komisi Ekstra", "")

            if not link_komisi:
                self.log(f"⚠️ [{index}] Lewati: {nama} (tanpa Link Komisi)")
                continue

            message = f"""🛍️ {nama}
💰 Harga: {harga}
🔥 Terjual: {penjualan}
🏪 Toko: {toko}
💸 Komisi: {komisi} ({komisi_hingga})

Klik untuk detail:
{link_komisi}"""

            url = f"https://graph.facebook.com/{self.page_id.get()}/feed"
            data = {
                "message": message,
                "link": link_komisi,
                "access_token": self.access_token.get(),
            }

            try:
                response = requests.post(url, data=data, timeout=20)
                if response.status_code == 200:
                    self.log(f"✅ [{index}] Berhasil posting: {nama}")
                else:
                    self.log(f"❌ [{index}] Gagal posting: {nama} — {response.text}")
            except Exception as e:
                self.log(f"❌ [{index}] Error: {e}")

            # Update progress
            self.progress["value"] = index + 1

            # Delay acak
            if index < len(produk_list) - 1:
                delay = random.randint(self.delay_min, self.delay_max)
                menit = round(delay / 60, 1)
                self.log(f"⏳ Menunggu {menit} menit ({delay} detik) sebelum posting berikutnya...\n")
                for i in range(delay):
                    time.sleep(1)

        self.log("🎉 Selesai autopost semua produk!\n")
        self.start_button.config(state="normal", text="🚀 Mulai Posting")


if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookAutoPostApp(root)
    root.mainloop()
