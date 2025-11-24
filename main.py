import requests
import time
import re
import json
import os

from bot_manager import BotManager
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# إعدادات الصفحة
load_dotenv()
PAGE_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
PAGE_ID = os.getenv("FB_PAGE_ID")


# ملف الردود الموجود بجانب السكريبت
RESPONSES_FILE = os.path.join(os.path.dirname(__file__), "responses.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "log.txt")
SEEN_FILE = os.path.join(os.path.dirname(__file__), "seen_comments.json")

if not PAGE_ACCESS_TOKEN or not PAGE_ID:
    raise ValueError("❌ Please set FB_ACCESS_TOKEN and FB_PAGE_ID in environment.")

# تشغيل البوت
def run_bot():
    manager = BotManager()
    print("🤖 Bot is running... (Ctrl + C to stop)")
    seen_comments = BotManager.load_seen_comments()
    last_reload_time = 0
    reload_interval = 60

    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            try:
                current_time = time.time()
                if current_time - last_reload_time > reload_interval:
                    responses_data = manager.load_responses()
                    last_reload_time = current_time

                posts = manager.get_all_posts(limit=50)
                futures = [executor.submit(manager.process_post, post, responses_data, seen_comments) for post in posts]
                for future in as_completed(futures):
                    future.result()

                manager.save_seen_comments(seen_comments)
                
                time.sleep(10)

            except Exception:
                time.sleep(30)

# نقطة البداية
if __name__ == "__main__":
    run_bot()
