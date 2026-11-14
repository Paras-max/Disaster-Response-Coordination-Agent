# import csv
# from datetime import datetime
# import os

# LOG_FILE = "risk_log.csv"

# # ✅ Ensure log file has headers
# if not os.path.exists(LOG_FILE):
#     with open(LOG_FILE, mode="w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["timestamp", "city", "weather", "humidity", "risk_score", "risk_level", "boats", "medical_units", "ndrf_teams"])

# def log_risk(city, weather, risk_score, risk_level, allocation):
#     """Append each city's risk data to CSV for tracking over time."""
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     humidity = weather.get("main", {}).get("humidity", "N/A")
#     desc = weather.get("weather", [{}])[0].get("description", "Unknown")

#     with open(LOG_FILE, mode="a", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow([
#             timestamp,
#             city,
#             desc,
#             humidity,
#             risk_score,
#             risk_level,
#             allocation["boats"],
#             allocation["medical_units"],
#             allocation["ndrf_teams"]
#         ])
# import csv
# import os
# from datetime import datetime

# # ------------------------------
# # 📁 CSV FILE CONFIGURATION
# # ------------------------------
# LOG_FILE = "risk_log.csv"

# # If the CSV doesn't exist, create it with proper headers
# if not os.path.exists(LOG_FILE):
#     with open(LOG_FILE, mode="w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow([
#             "Timestamp",
#             "City",
#             "Weather",
#             "Risk Score",
#             "Risk Level",
#             "Boats",
#             "Medical Units",
#             "NDRF Teams"
#         ])

# # ------------------------------
# # 📝 LOG FUNCTION
# # ------------------------------
# def log_risk(city, weather, risk_score, risk_level, allocation):
#     """
#     Logs disaster response data to CSV.
#     Each row includes timestamp, city, weather info, risk score/level, and allocated resources.
#     """

#     # Extract resource values safely
#     boats = allocation.get("Boats", 0)
#     medical_units = allocation.get("Medical Units", 0)
#     ndrf_teams = allocation.get("NDRF Teams", 0)

#     # Extract weather info safely
#     if isinstance(weather, dict):
#         weather_desc = weather.get("description", "N/A")
#     else:
#         weather_desc = str(weather)

#     # Write to CSV file
#     with open(LOG_FILE, mode="a", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow([
#             datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             city,
#             weather_desc,
#             round(float(risk_score), 2),
#             risk_level,
#             boats,
#             medical_units,
#             ndrf_teams
#         ])

#     # Console confirmation
#     print(
#         f"📝 Logged data for {city}: "
#         f"Risk={risk_level} ({risk_score:.2f}), "
#         f"Resources → Boats={boats}, Medical Units={medical_units}, NDRF Teams={ndrf_teams}"
#     )
# -------------------------------------------------------------
# 🌍 Disaster Response Coordination Agent
# -------------------------------------------------------------
# import csv
# from datetime import datetime
# import os

# LOG_FILE = "risk_log.csv"

# def log_risk(city, weather, risk_score, risk_level, allocation):
#     """
#     Logs risk, weather, and resource allocation data into a CSV file.
#     """
#     file_exists = os.path.isfile(LOG_FILE)
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Extract weather safely
#     weather_desc = weather.get("weather", [{}])[0].get("description", "unknown")
#     humidity = weather.get("main", {}).get("humidity", "N/A")

#     # Extract resources safely
#     boats = allocation.get("boats", 0)
#     medical_units = allocation.get("medical_units", 0)
#     ndrf_teams = allocation.get("ndrf_teams", 0)

#     # ✅ Dashboard-matching headers
#     headers = [
#         "Timestamp", "City", "Weather", "Humidity",
#         "Risk Score", "Risk Level", "Boats", "Medical Units", "NDRF Teams"
#     ]

#     # ✅ Write data
#     with open(LOG_FILE, "a", newline="") as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             writer.writerow(headers)
#         writer.writerow([
#             timestamp, city, weather_desc, humidity, risk_score, risk_level,
#             boats, medical_units, ndrf_teams
#         ])
import csv
from datetime import datetime
import os

LOG_FILE = "risk_log.csv"

def log_risk(city, weather, risk_score, risk_level, allocation):
    """
    Logs risk, weather, and resource allocation data into a CSV file.
    Automatically adds timestamps and ensures all columns exist.
    """

    # Ensure log file exists
    file_exists = os.path.isfile(LOG_FILE)

    # Always add a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extract weather safely
    weather_desc = weather.get("weather", [{}])[0].get("description", "unknown")
    humidity = weather.get("main", {}).get("humidity", "N/A")

    # Extract resources safely
    boats = allocation.get("boats", 0)
    medical_units = allocation.get("medical_units", 0)
    ndrf_teams = allocation.get("ndrf_teams", 0)

    # Define the correct headers
    headers = [
        "Timestamp", "City", "Weather", "Humidity",
        "Risk Score", "Risk Level",
        "Boats", "Medical Units", "NDRF Teams"
    ]

    # Write data to CSV
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)

        # Write header if new file or empty
        if not file_exists or os.path.getsize(LOG_FILE) == 0:
            writer.writeheader()

        # Write the current row
        writer.writerow({
            "Timestamp": timestamp,
            "City": city,
            "Weather": weather_desc,
            "Humidity": humidity,
            "Risk Score": risk_score,
            "Risk Level": risk_level,
            "Boats": boats,
            "Medical Units": medical_units,
            "NDRF Teams": ndrf_teams
        })

    print(f"✅ Logged: {city} | {risk_level} | {timestamp}")
