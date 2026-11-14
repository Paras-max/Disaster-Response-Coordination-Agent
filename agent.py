# # src/agent.py

# import time
# import schedule
# from collector import get_current_weather, collect_tweets
# from nlp import analyze_tweets

# def job():
#     print("\n🔄 Running Disaster Response Agent...\n")

#     # Fetch weather (you can set coordinates as needed)
#     weather = get_current_weather(19.07, 72.87)
#     if weather and "weather" in weather:
#         print(f"🌦 Weather: {weather['weather'][0]['description'].capitalize()}, Temp: {weather['main']['temp']}°C")
#     else:
#         print("⚠️ Could not fetch weather data.")

#     # Analyze tweets for distress
#     analyze_tweets()

#     print("✅ Task completed. Waiting for next cycle...\n")

# # Schedule the task to run automatically every 10 minutes
# schedule.every(10).minutes.do(job)

# if __name__ == "__main__":
#     print("🚀 Disaster Response Agent Started...")
#     job()  # run once immediately

#     while True:
#         schedule.run_pending()
#         time.sleep(1)
# import time
# import schedule
# from collector import get_current_weather, collect_tweets
# from nlp import analyze_tweets, is_distress
# from smart_allocator import smart_allocate
# import pandas as pd

# def job():
#     print("\n🔄 Running Disaster Response Agent...\n")

#     # 🌦 Fetch weather for a fixed city (Mumbai in this example)
#     lat, lon = 19.07, 72.87
#     weather = get_current_weather(lat, lon)

#     if weather and "weather" in weather:
#         print(f"🌦 Weather: {weather['weather'][0]['description'].capitalize()}, Temp: {weather['main']['temp']}°C")
#     else:
#         print("⚠️ Could not fetch weather data.")

#     # 💬 Analyze tweets for distress
#     try:
#         df = pd.read_csv("data.csv")

#         if "message" not in df.columns:
#             print("⚠️ No 'message' column found in data.csv.")
#             return

#         distress_data = df["message"].tolist()

#         # Count distress messages
#         distress_count = sum(1 for msg in distress_data if is_distress(msg))
#         print(f"🚨 Distress Messages Detected: {distress_count}")

#         # 🧠 Smart Resource Allocation (AI)
#         smart_allocate(city="Mumbai", lat=lat, lon=lon, distress_data=distress_data, population=20000000)

#     except Exception as e:
#         print(f"❌ Error analyzing tweets or allocating resources: {e}")

#     print("✅ Task completed. Waiting for next cycle...\n")


# # ⏰ Schedule the task to run automatically every 10 minutes
# schedule.every(10).minutes.do(job)

# if __name__ == "__main__":
#     print("🚀 Disaster Response Agent Started...")
#     job()  # Run once immediately

#     while True:
#         schedule.run_pending()
#         time.sleep(60)
# import time
# import schedule
# import time
# from logger import log_risk

# from collector import get_current_weather, collect_tweets
# from nlp import analyze_tweets
# from smart_allocator import allocate_resources

# # ----------------------------------------
# # 🌍 City Coordinates + Populations
# # ----------------------------------------
# CITIES = {
#     "Mumbai": {"lat": 19.07, "lon": 72.87, "population": 3100000},
#     "Pune": {"lat": 18.52, "lon": 73.85, "population": 1800000},
#     "Delhi": {"lat": 28.61, "lon": 77.21, "population": 3200000},
#     "Chennai": {"lat": 13.08, "lon": 80.27, "population": 2500000},
# }


# # ----------------------------------------
# # 🚀 MAIN AGENT LOGIC
# # ----------------------------------------
# def job():
#     print("\n🔄 Running Disaster Response Agent for Multiple Cities...\n")

#     # Step 1️⃣: Analyze distress tweets
#     try:
#         tweets, help_tweets = collect_tweets()
#         analyzed = analyze_tweets()

#         distress_count = len([t for t in analyzed if t['distress']])
#         print(f"💬 Total distress reports detected: {distress_count}")
#     except Exception as e:
#         print(f"⚠️ Error analyzing tweets: {e}")
#         distress_count = 0

#     # Step 2️⃣: Loop through all cities
#     for city, info in CITIES.items():
#         lat, lon = info["lat"], info["lon"]
#         population = info["population"]

#         print(f"\n📍 Processing city: {city}...")

#         # Get weather
#         try:
#             weather = get_current_weather(lat, lon)
#             humidity = weather["main"]["humidity"]
#             desc = weather["weather"][0]["description"].capitalize()
#             temp = weather["main"]["temp"]
#             print(f"🌦 Weather: {desc}, Temp: {temp}°C, Humidity: {humidity}%")
#         except Exception as e:
#             print(f"⚠️ Could not fetch weather for {city}: {e}")
#             humidity = 50  # fallback value

#         # Step 3️⃣: Smart resource allocation
#         try:
#             result = allocate_resources(city, distress_count, humidity, population)

#             print(f"✅ Allocation Summary for {city}:")
#             print(f"   • Risk Score: {result['risk_score']}")
#             print(f"   • Risk Level: {result['risk_level'].upper()}")
#             print(f"   • Resources: {result['resources']}")
#         except Exception as e:
#             print(f"⚠️ Allocation failed for {city}: {e}")

#         print("-" * 50)

#     print("\n⏳ Waiting for next 10-min cycle...\n")
#     print("=" * 60)


# # ----------------------------------------
# # ⏰ SCHEDULER
# # ----------------------------------------
# schedule.every(10).minutes.do(job)

# if __name__ == "__main__":
#     print("🚀 Multi-City Disaster Response Agent Started...\n")
#     job()  # Run once immediately

#     while True:
#         schedule.run_pending()
#         time.sleep(1)
# logger.py
# -------------------------------------------------------------
# 🌍 Disaster Response Coordination Agent
# -------------------------------------------------------------
from collector import get_current_weather, collect_tweets
from nlp import analyze_tweets
from smart_allocator import allocate_resources
from logger import log_risk
import time

# -------------------------------------------------------------
# 🧠 Main Agent Function
# -------------------------------------------------------------
def job():
    print("\n🔄 Running Disaster Response Agent...\n")

    # Cities and their coordinates (lat, lon)
    cities = {
    "Mumbai": (19.07, 72.87),
    "Pune": (18.52, 73.85),
    "Delhi": (28.61, 77.21),
    "Chennai": (13.08, 80.27),

    # 🆕 Added local cities
    "Phaltan, Maharashtra": (17.9915, 74.4317),
    "Kalamboli, Navi Mumbai, Maharashtra": (19.025770, 73.101570)
}


    for city, (lat, lon) in cities.items():
        print(f"\n📍 City: {city}")

        # 🌦 Get weather data
        weather = get_current_weather(lat, lon)
        if not weather or "weather" not in weather:
            print("⚠️ Could not fetch weather data for this city.")
            continue

        # 💬 Analyze distress tweets for the city
        distress_count = analyze_tweets(city)

        # ⚙️ Allocate resources based on weather + distress
        allocation, risk_score, risk_level = allocate_resources(city, weather, distress_count)

        # 🧾 Print current city summary
        print(f"🚨 Risk Level: {risk_level.upper()} ({risk_score})")
        print(f"🚑 Resources: {allocation}")

        # 📝 Log to CSV
        print(f"📝 Logging data for {city}...")
        log_risk(city, weather, risk_score, risk_level, allocation)

        print("-" * 40)

    print("\n✅ Cycle complete. Waiting for next run...\n")


# -------------------------------------------------------------
# 🚀 Run Agent Continuously (Manual or Automated)
# -------------------------------------------------------------
if __name__ == "__main__":
    while True:
        job()
        print("⏳ Sleeping for 2 minutes before next cycle...\n")
        time.sleep(120)  # Run every 2 minutes (adjust as needed)
