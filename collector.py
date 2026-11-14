# import requests
# import os
# import pandas as pd
# from dotenv import load_dotenv

# load_dotenv()
# OWM_KEY = os.getenv("OPENWEATHER_KEY")

# # 🌦 WEATHER DATA COLLECTOR
# def get_current_weather(lat, lon):
#     """Fetch current weather data for given coordinates."""
#     url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_KEY}&units=metric"
#     r = requests.get(url).json()
#     return r

# # 💬 TWEET DATA COLLECTOR
# def collect_tweets():
#     """Read simulated tweets from CSV file."""
#     tweets = pd.read_csv("data/sim_tweets.csv")
#     help_tweets = tweets[tweets['status'] == 'help']
#     return tweets, help_tweets
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from nlp import is_distress, extract_numbers, extract_location  # 👈 add this import

# -----------------------------
# 🌦 WEATHER DATA COLLECTOR
# -----------------------------
load_dotenv()
OWM_KEY = os.getenv("OPENWEATHER_KEY")

def get_current_weather(lat, lon):
    """Fetch current weather data for given coordinates."""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_KEY}&units=metric"
    r = requests.get(url).json()
    return r


# -----------------------------
# 💬 TWEET DATA COLLECTOR
# -----------------------------
def collect_tweets():
    """Read simulated tweets from CSV file."""
    tweets = pd.read_csv("data.csv")
    help_tweets = tweets[tweets['status'] == 'help']
    return tweets, help_tweets


# -----------------------------
# 🚨 NLP + WEATHER ANALYZER
# -----------------------------
def analyze_tweets():
    """Analyze tweets for distress and print key info."""
    tweets, help_tweets = collect_tweets()

    print("\n🔍 Analyzing Tweets for Distress Signals...\n")

    for _, row in help_tweets.iterrows():
        text = str(row['text'])
        lat, lon = row.get('lat', None), row.get('lon', None)

        if is_distress(text):
            people = extract_numbers(text)
            location = extract_location(text)
            print(f"🚨 Distress detected: {text}")
            print(f"   → People: {people}")
            print(f"   → Location (text): {location}")
            print(f"   → Coordinates: ({lat}, {lon})")

            # Optional: Weather info
            if pd.notna(lat) and pd.notna(lon):
                weather = get_current_weather(lat, lon)
                if 'weather' in weather:
                    print(f"   → Weather: {weather['weather'][0]['description']}")
            print()
        else:
            print(f"✅ No distress: {text}\n")


# -----------------------------
# ▶️ MAIN TEST
# -----------------------------
if __name__ == "__main__":
    analyze_tweets()




