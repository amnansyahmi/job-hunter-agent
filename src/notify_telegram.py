import os
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

today = datetime.now().strftime("%Y-%m-%d")
input_path = DATA_DIR / f"ranked_jobs_{today}.xlsx"

df = pd.read_excel(input_path)

top_jobs = df[df["Recommendation"].isin(["Apply", "Maybe"])].head(10)

if top_jobs.empty:
    message = "Good morning Nan. No suitable jobs found today."
else:
    lines = [f"Good morning Nan. Found {len(top_jobs)} suitable jobs today.\n"]

    for idx, row in top_jobs.iterrows():
        lines.append(
            f"{len(lines)}. {row['Job Title']}\n"
            f"Company: {row['Company Name']}\n"
            f"Location: {row['Location']}\n"
            f"Salary: {row['Salary Range']}\n"
            f"Match: {row['Match Score']}/10\n"
            f"Recommendation: {row['Recommendation']}\n"
            f"Reason: {row['Reason']}\n"
            f"URL: {row['Job URL']}\n"
        )

    message = "\n".join(lines)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(url, json={
    "chat_id": CHAT_ID,
    "text": message,
    "disable_web_page_preview": True
})

response.raise_for_status()

print("Telegram notification sent")
