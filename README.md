# 🤖 Telegram Reminder Bot - by Airdrop Sambil Rebahan

Bot Telegram ini memungkinkan kamu untuk mengatur pengingat (reminder) berdasarkan waktu tertentu yang ditentukan berisi link garapanmu.

---

## ✨ Fitur

- Atur reminder berdasarkan detik, menit, jam, atau hari.
- Reminder harian otomatis pada jam tertentu (format `HH:MM`).
- Tersimpan secara otomatis ke dalam file (`reminders.json`).
- Perintah: `/set`, `/list`, `/delete`.

---

## 📦 Instalasi

1. **Clone repositori**

```bash
git clone https://github.com/yonarebahan/reminder-telegram-BOT.git
cd reminder-telegram-BOT
```
2. **masuk ke venv**
```bash
python3 -m venv venv
source venv/bin/activate
```
2. **jalankan script auto install**

```bash
chmod +x install.sh
./install.sh
```
3. **ubah token**
```bash
nano .env
```
4. **jalankan script**
```bash
python3 bot.py
```
