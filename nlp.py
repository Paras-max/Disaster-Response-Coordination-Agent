# src/nlp.py

# import pandas as pd
# import re

# # -------------------------------------
# # 🚨 DISTRESS DETECTION KEYWORDS
# # -------------------------------------
# # Common distress words in English + Hindi
# keywords = [
#     "help", "fas gaye", "phasa", "rescue", "save us",
#     "trapped", "help us", "bachao", "need help",
#     "stuck", "emergency", "sos", "जान बचाओ", "फंसे हैं",
#     "flood", "flooded", "rain", "barish", "paani", "भारी बारिश", "जलमग्न"
# ]

# def is_distress(text):
#     """Check if the message/tweet is a distress call."""
#     if not isinstance(text, str):
#         return False
#     t = text.lower()
#     return any(k in t for k in keywords)

# # -------------------------------------
# # 👥 EXTRACT NUMBER OF PEOPLE
# # -------------------------------------
# def extract_numbers(text):
#     """Extracts number of people from text, e.g. '10 people trapped'."""
#     if not isinstance(text, str):
#         return None
#     m = re.search(r'(\d+)\s*(people|log|persons|members)?', text)
#     return int(m.group(1)) if m else None

# # -------------------------------------
# # 📍 EXTRACT LOCATION
# # -------------------------------------
# def extract_location(text):
#     """Extracts simple location names using 'in <Location>' pattern."""
#     if not isinstance(text, str):
#         return None
#     m = re.search(r'in\s+([A-Z][a-zA-Z]+)', text)
#     return m.group(1) if m else None

# # -------------------------------------
# # 🧩 ANALYZE TWEETS
# # -------------------------------------
# import pandas as pd

# def analyze_tweets():
#     print("\n🔍 Analyzing Tweets for Distress Signals...\n")
#     df = pd.read_csv("data.csv")

#     for _, row in df.iterrows():
#         text = str(row.get("text", ""))
#         if is_distress(text):
#             print(f"🚨 Distress Detected: {text}")
#             print(f"📍 Location: {extract_location(text)}")
#             print(f"👥 People: {extract_numbers(text)}")
#             print("-" * 40)
#         else:
#             print(f"✅ No distress: {text}")
#     print("\n✅ Analysis Complete.\n")

# if __name__ == "__main__":
#     analyze_tweets()

# import re
# import pandas as pd

# keywords = [
#     "help", "fas gaye", "phasa", "rescue", "save us",
#     "trapped", "help us", "bachao", "need help",
#     "stuck", "emergency", "sos", "जान बचाओ", "फंसे हैं",
#     "flood", "flooded", "rain", "barish", "paani", "भारी बारिश", "जलमग्न"
# ]

# def is_distress(text):
#     if not isinstance(text, str):
#         return False
#     t = text.lower()
#     return any(k in t for k in keywords)

# def extract_numbers(text):
#     if not isinstance(text, str):
#         return None
#     m = re.search(r'(\d+)\s*(people|log|persons|members)?', text)
#     return int(m.group(1)) if m else None

# def extract_location(text):
#     if not isinstance(text, str):
#         return None
#     m = re.search(r'in\s+([A-Z][a-zA-Z]+)', text)
#     return m.group(1) if m else None

# # ✅ UPDATED FUNCTION
# def analyze_tweets(df):
#     """Analyze a given dataframe of tweets/messages."""
#     df["is_distress"] = df["message"].apply(is_distress)
#     df["num_people"] = df["message"].apply(extract_numbers)
#     df["location"] = df["message"].apply(extract_location)
#     return df
import pandas as pd
import re

# -------------------------------------
# 🚨 DISTRESS DETECTION KEYWORDS
# -------------------------------------
keywords = [
    "help", "fas gaye", "phasa", "rescue", "save us",
    "trapped", "help us", "bachao", "need help",
    "stuck", "emergency", "sos", "जान बचाओ", "फंसे हैं",
    "flood", "flooded", "rain", "barish", "paani", "भारी बारिश", "जलमग्न"
]

def is_distress(text):
    if not isinstance(text, str):
        return False
    t = text.lower()
    return any(k in t for k in keywords)

def extract_numbers(text):
    if not isinstance(text, str):
        return None
    m = re.search(r'(\d+)\s*(people|log|persons|members)?', text)
    return int(m.group(1)) if m else None

def extract_location(text):
    if not isinstance(text, str):
        return None
    m = re.search(r'in\s+([A-Z][a-zA-Z]+)', text)
    return m.group(1) if m else None

# -------------------------------------
# 🧠 MAIN FUNCTION
# -------------------------------------
def analyze_tweets(city_name):
    """Reads data.csv, filters for a specific city, and detects distress."""
    try:
        df = pd.read_csv("data.csv")  # load your dataset
    except FileNotFoundError:
        print("⚠️ data.csv not found!")
        return 0

    if "message" not in df.columns or "city" not in df.columns:
        print("⚠️ Missing required columns in data.csv (need 'message' and 'city').")
        return 0

    # Filter only rows for this city
    city_df = df[df["city"].str.lower() == city_name.lower()]

    if city_df.empty:
        print(f"ℹ️ No data for {city_name}.")
        return 0

    # Check which are distress
    city_df["is_distress"] = city_df["message"].apply(is_distress)

    distress_count = city_df["is_distress"].sum()
    print(f"💬 {city_name}: {distress_count} distress messages found.")

    return int(distress_count)

