
import os
from telegram import Bot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)

if __name__ == "__main__":
    updates = bot.get_updates()
    if not updates:
        print("❗ 尚未收到任何訊息，請先在 Telegram 群組發一條訊息。")
    else:
        print("✅ Chat IDs recently interacted with:")
        for u in updates:
            chat = u.message.chat
            print(f"- {chat.id} ({chat.title or chat.username or 'Private'})")
