import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import requests
import json
import time
import random
import threading
from datetime import datetime, timedelta
import os


class FacebookAutoPostApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Page AutoPost - By Pandu Aldi P.")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Variabel input
        self.app_id = tk.StringVar()
        self.app_secret = tk.StringVar()
        self.page_id = tk.StringVar()
        self.access_token = tk.StringVar()
        self.json_path = tk.StringVar()

        # File penyimpanan token
        self.token_file = "token.json"

        # Frame Input
        frame = tk.LabelFrame(root, text="Konfigurasi", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=10)

        tk.Label(frame, text="App ID:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.app_id, width=50).grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame, text="App Secret:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.app_secret, width=50, show="*").grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame, text="Page ID:").grid(row=2, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.page_id, width=50).grid(row=2, column=1, padx=5, pady=2)

        tk.Label(frame, text="Access Token:").grid(row=3, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.access_token, width=50, show="*").grid(row=3, column=1, padx=5, pady=2)

        # Tombol Simpan & Refresh Token
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=3, column=2, padx=5)

        tk.Button(btn_frame, text="💾 Simpan", command=self.save_token, width=10).pack(side="left", padx=2)
        tk.Button(btn_frame, text="🔄 Refresh", command=self.manual_refresh_token, width=10).pack(side="left", padx=2)

        tk.Label(frame, text="File JSON Produk:").grid(row=4, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.json_path, width=50, state="readonly").grid(row=4, column=1, padx=5, pady=2)
        tk.Button(frame, text="Browse...", command=self.browse_json).grid(row=4, column=2, padx=5)

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

        # Load token jika sudah tersimpan
        self.load_token()

    # === FILE TOKEN ===
    def load_token(self):
        """Load token dari file, dan otomatis refresh jika expired."""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, "r") as f:
                    data = json.load(f)
                    token = data.get("access_token")
                    expires_at = datetime.fromisoformat(data.get("expires_at", datetime.now().isoformat()))

                    # Cek validitas token langsung ke Graph API
                    self.log("🔎 Mengecek validitas token di server Facebook...")
                    check = requests.get(
                        "https://graph.facebook.com/debug_token",
                        params={
                            "input_token": token,
                            "access_token": f"{self.app_id.get()}|{self.app_secret.get()}"
                        }
                    ).json()

                    is_valid = check.get("data", {}).get("is_valid", False)

                    if not is_valid or datetime.now() >= expires_at:
                        self.log("⚠️ Token kadaluarsa atau tidak valid, mencoba refresh otomatis...")
                        refreshed = self.refresh_token(token)
                        if refreshed:
                            self.log("✅ Token berhasil diperbarui otomatis saat startup!")
                        else:
                            self.log("❌ Gagal refresh token otomatis, silakan isi token baru.")
                    else:
                        self.access_token.set(token)
                        self.log("🔑 Token masih valid dan siap digunakan.")

            except Exception as e:
                self.log(f"⚠️ Gagal membaca token.json: {e}")
        else:
            self.log("ℹ️ Belum ada file token.json, silakan masukkan token lalu klik 'Simpan Token'.")

    def save_token(self):
        token_data = {
            "access_token": self.access_token.get(),
            "expires_at": (datetime.now() + timedelta(days=60)).isoformat()
        }
        with open(self.token_file, "w") as f:
            json.dump(token_data, f, indent=4)
        self.log("💾 Token disimpan ke token.json")

    def manual_refresh_token(self):
        """Fungsi tombol Refresh Token manual"""
        token_data = self.get_token_data()
        if not token_data:
            messagebox.showerror("Error", "Token belum disimpan. Simpan token terlebih dahulu.")
            return

        old_token = token_data["access_token"]
        new_token = self.refresh_token(old_token)
        if new_token:
            self.access_token.set(new_token)
            messagebox.showinfo("Sukses", "Token berhasil diperbarui!")
        else:
            messagebox.showerror("Gagal", "Gagal memperbarui token. Periksa App ID & Secret Anda.")

    def get_token_data(self):
        if not os.path.exists(self.token_file):
            return None
        with open(self.token_file, "r") as f:
            return json.load(f)

    def refresh_token(self, old_token):
        self.log("🔄 Refreshing token otomatis...")
        url = (
            f"https://graph.facebook.com/v20.0/oauth/access_token?"
            f"grant_type=fb_exchange_token&"
            f"client_id={self.app_id.get()}&"
            f"client_secret={self.app_secret.get()}&"
            f"fb_exchange_token={old_token}"
        )

        try:
            response = requests.get(url)
            data = response.json()

            if "access_token" in data:
                new_token = data["access_token"]
                expires_in = data.get("expires_in", 5184000)  # default 60 hari
                expires_at = (datetime.now() + timedelta(seconds=expires_in)).isoformat()

                token_data = {
                    "access_token": new_token,
                    "expires_at": expires_at
                }
                with open(self.token_file, "w") as f:
                    json.dump(token_data, f, indent=4)

                self.access_token.set(new_token)
                self.log("✅ Token berhasil diperbarui dan disimpan.")
                return new_token
            else:
                self.log(f"❌ Gagal refresh token: {data}")
        except Exception as e:
            self.log(f"❌ Error saat refresh token: {e}")
        return None

    def get_valid_token(self):
        """Pastikan token valid sebelum dipakai posting."""
        token_data = self.get_token_data()
        if not token_data:
            return self.access_token.get()

        expires_at = datetime.fromisoformat(token_data["expires_at"])
        if datetime.now() >= expires_at:
            self.log("⚠️ Token expired, mencoba refresh otomatis...")
            new_token = self.refresh_token(token_data["access_token"])
            return new_token if new_token else token_data["access_token"]

        return token_data["access_token"]

    # === LOGIC APLIKASI ===
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

        token = self.get_valid_token()
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
            data = {"message": message, "link": link_komisi, "access_token": token}

            try:
                response = requests.post(url, data=data, timeout=20)
                if response.status_code == 200:
                    self.log(f"✅ [{index}] Berhasil posting: {nama}")
                else:
                    self.log(f"❌ [{index}] Gagal posting: {nama} — {response.text}")
            except Exception as e:
                self.log(f"❌ [{index}] Error: {e}")

            self.progress["value"] = index + 1

            if index < len(produk_list) - 1:
                delay = random.randint(self.delay_min, self.delay_max)
                menit = round(delay / 60, 1)
                self.log(f"⏳ Menunggu {menit} menit ({delay} detik) sebelum posting berikutnya...\n")
                for _ in range(delay):
                    time.sleep(1)

        self.log("🎉 Selesai autopost semua produk!\n")
        self.start_button.config(state="normal", text="🚀 Mulai Posting")


if __name__ == "__main__":
    root = tk.Tk()
    app = FacebookAutoPostApp(root)
    root.mainloop()
