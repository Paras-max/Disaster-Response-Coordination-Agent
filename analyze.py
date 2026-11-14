# analyze.py
import pandas as pd
import schedule
import time
from nlp import is_distress, extract_location
from predictor import predict_flood_risk

# -------------------------------
# 🔍 STEP 1: READ MESSAGE DATA
# -------------------------------
def analyze_tweets_and_predict():
    print("\n📊 Starting Disaster Analysis...\n")

    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        print("⚠️ data.csv not found. Make sure it’s in the same folder.")
        return

    # ✅ Accept both 'text' or 'message' columns
    if "message" in df.columns:
        text_column = "message"
    elif "text" in df.columns:
        text_column = "text"
    else:
        print("⚠️ No valid column found. Please include 'message' or 'text' in data.csv.")
        return

    # Track distress counts per city
    city_counts = {}

    for _, row in df.iterrows():
        text = str(row.get(text_column, ""))
        if is_distress(text):
            city = extract_location(text) or "Unknown"
            city_counts[city] = city_counts.get(city, 0) + 1
            print(f"🚨 Distress Detected: {text}")
        else:
            print(f"✅ No distress: {text}")

    print("\n-----------------------------")
    print("🌍 Distress Summary by City:")
    print("-----------------------------")

    if not city_counts:
        print("No distress messages found.")
        return

    for city, count in city_counts.items():
        print(f"🏙 {city}: {count} distress reports")
        predict_flood_risk(city, distress_count=count)

    print("\n✅ Analysis Complete.\n")


# -------------------------------
# ⏰ STEP 2: AUTO-SCHEDULER
# -------------------------------
def start_scheduler():
    # Run once at startup
    analyze_tweets_and_predict()

    # Schedule to run every 15 minutes
    schedule.every(15).minutes.do(analyze_tweets_and_predict)

    print("🕒 Scheduler started... running every 15 minutes.\n")

    while True:
        schedule.run_pending()
        time.sleep(10)


# -------------------------------
# ▶️ MAIN RUN
# -------------------------------
if __name__ == "__main__":
    start_scheduler()
