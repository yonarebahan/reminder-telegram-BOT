from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import threading
import time
import re
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

# --- Load environment variable ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

REMINDER_FILE = "reminders.json"
active_reminders = {}

# --- File Handling ---
def save_reminders():
    with open(REMINDER_FILE, "w") as f:
        json.dump(active_reminders, f, default=str)

def load_reminders():
    global active_reminders
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            raw = json.load(f)
            for chat_id in raw:
                for r in raw[chat_id]:
                    r["start_time"] = datetime.fromisoformat(r["start_time"])
                    r["delay"] = int(r.get("delay", 0))
                    r["repeat"] = r.get("repeat", False)
                    r["daily_time"] = r.get("daily_time", None)
            active_reminders = raw

# --- Helper ---
def parse_time(time_str):
    match = re.match(r"(\d+)\s*(detik|menit|jam|hari)s?", time_str)
    if not match:
        return None
    value, unit = int(match[1]), match[2]
    multiplier = {
        "detik": 1,
        "menit": 60,
        "jam": 3600,
        "hari": 86400
    }
    return value * multiplier[unit]

def get_seconds_until(hour, minute):
    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return int((target - now).total_seconds())

def get_remaining_time(remaining_seconds):
    if remaining_seconds >= 86400:
        return f"{int(remaining_seconds // 86400)} hari"
    elif remaining_seconds >= 3600:
        return f"{int(remaining_seconds // 3600)} jam"
    elif remaining_seconds >= 60:
        return f"{int(remaining_seconds // 60)} menit"
    else:
        return f"{int(remaining_seconds)} detik"

# --- Reminder Thread ---
def reminder_thread(chat_id, name, message, bot, delay, repeat, daily_time=None):
    time.sleep(delay)
    bot.send_message(chat_id=chat_id, text=f"✅ Reminder '{name}': {message}")

    if chat_id in active_reminders:
        for r in active_reminders[chat_id]:
            if r["name"] == name:
                if repeat:
                    if daily_time:
                        hour, minute = map(int, daily_time.split(":"))
                        next_delay = get_seconds_until(hour, minute)
                        r["start_time"] = datetime.now()
                        save_reminders()
                        threading.Thread(target=reminder_thread, args=(
                            chat_id, name, message, bot, next_delay, True, daily_time)).start()
                    else:
                        r["start_time"] = datetime.now()
                        save_reminders()
                        threading.Thread(target=reminder_thread, args=(
                            chat_id, name, message, bot, r["delay"], True)).start()
                else:
                    active_reminders[chat_id] = [rem for rem in active_reminders[chat_id] if rem["name"] != name]
                    save_reminders()
                break

# --- Command: /set ---
def set_reminder(update: Update, context: CallbackContext):
    if len(context.args) < 3:
        update.message.reply_text("⏳ Penggunaan: /set <nama> <link> <waktu/jam> [daily]")
        return

    name = context.args[0]
    link = context.args[1]
    last_arg = context.args[-1].lower()
    repeat = last_arg == "daily"
    daily_time = None
    delay = None

    time_input = " ".join(context.args[2:-1]) if repeat else " ".join(context.args[2:])

    if repeat:
        if re.match(r"\d{1,2}:\d{2}", time_input):
            try:
                hour, minute = map(int, time_input.split(":"))
                delay = get_seconds_until(hour, minute)
                daily_time = f"{hour:02}:{minute:02}"
            except:
                update.message.reply_text("❌ Format jam salah. Contoh: 08:30")
                return
        else:
            delay = parse_time(time_input)
            if delay is None:
                update.message.reply_text("⏳ Format waktu salah. Gunakan seperti '10 detik', '1 menit', atau jam (HH:MM).")
                return
    else:
        delay = parse_time(time_input)
        if delay is None:
            update.message.reply_text("⏳ Format waktu salah. Gunakan seperti '10 detik', '1 menit', atau '2 jam'.")
            return

    chat_id = str(update.message.chat_id)

    if chat_id not in active_reminders:
        active_reminders[chat_id] = []

    active_reminders[chat_id].append({
        "name": name,
        "link": link,
        "time": time_input,
        "start_time": datetime.now(),
        "delay": delay,
        "repeat": repeat,
        "daily_time": daily_time
    })

    save_reminders()

    mode = f" (daily setiap jam {daily_time})" if daily_time else (" (daily)" if repeat else "")
    update.message.reply_text(f"✅ Reminder '{name}' diset untuk link {link} dalam {time_input}{mode}.")
    threading.Thread(target=reminder_thread, args=(chat_id, name, link, context.bot, delay, repeat, daily_time)).start()

# --- Command: /list ---
def list_reminders(update: Update, context: CallbackContext):
    chat_id = str(update.message.chat_id)
    if chat_id not in active_reminders or not active_reminders[chat_id]:
        update.message.reply_text("❌ Tidak ada reminder aktif saat ini.")
        return

    response = "📌 **Daftar Reminder Aktif:**\n\n"
    now = datetime.now()

    for reminder in active_reminders[chat_id]:
        elapsed_time = (now - reminder["start_time"]).total_seconds()
        remaining_time = reminder["delay"] - elapsed_time
        if remaining_time <= 0:
            continue
        remaining_time_str = get_remaining_time(remaining_time)
        repeat_str = f" 🔁 (daily {reminder['daily_time']})" if reminder.get("daily_time") else (" 🔁 (daily)" if reminder.get("repeat") else "")
        response += f"🎁 *{reminder['name']}* | 🔗 [{reminder['link']}]({reminder['link']}) | ⏳ {remaining_time_str}{repeat_str}\n"

    update.message.reply_text(response, parse_mode="Markdown")

# --- Command: /delete ---
def delete_reminder(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        update.message.reply_text("🤖 Penggunaan: /delete <nama>")
        return

    name_to_delete = " ".join(context.args)
    chat_id = str(update.message.chat_id)

    if chat_id not in active_reminders or not active_reminders[chat_id]:
        update.message.reply_text("❌ Tidak ada reminder untuk dihapus.")
        return

    initial_length = len(active_reminders[chat_id])
    active_reminders[chat_id] = [r for r in active_reminders[chat_id] if r["name"] != name_to_delete]

    if len(active_reminders[chat_id]) < initial_length:
        save_reminders()
        update.message.reply_text(f"✅ Reminder '{name_to_delete}' berhasil dihapus.")
    else:
        update.message.reply_text(f"❌ Reminder dengan nama '{name_to_delete}' tidak ditemukan.")

# --- Main ---
def main():
    load_reminders()
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("set", set_reminder))  
    dp.add_handler(CommandHandler("list", list_reminders))
    dp.add_handler(CommandHandler("delete", delete_reminder))  

    now = datetime.now()
    for chat_id, reminders in active_reminders.items():
        for r in reminders:
            if r.get("daily_time"):
                hour, minute = map(int, r["daily_time"].split(":"))
                delay = get_seconds_until(hour, minute)
            else:
                elapsed = (now - r["start_time"]).total_seconds()
                delay = r["delay"] - elapsed
            if delay > 0:
                threading.Thread(target=reminder_thread, args=(
                    chat_id, r["name"], r["link"], updater.bot, delay, r.get("repeat", False), r.get("daily_time"))).start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
