# import pandas as pd
# import time
# import os
# import json
# from colorama import Fore, Style, init
# from plyer import notification

# # Initialize colorama
# init(autoreset=True)

# DATA_FILE = "risk_log.csv"
# ALERT_FILE = "alerts_status.json"
# CHECK_INTERVAL = 30  # seconds
# RISK_ALERT_LEVELS = ["high", "critical"]

# def send_alert(city, risk_level, risk_score, weather):
#     """Display console + desktop alerts"""
#     alert_msg = f"🚨 ALERT: {city} | Risk: {risk_level.upper()} | Score: {risk_score} | Weather: {weather}"
    
#     color = Fore.RED if risk_level.lower() == "critical" else Fore.YELLOW
#     print(color + alert_msg + Style.RESET_ALL)

#     # Desktop notification
#     notification.notify(
#         title=f"⚠️ {city} Risk Alert!",
#         message=f"Risk Level: {risk_level.upper()} | Score: {risk_score}\nWeather: {weather}",
#         app_name="Disaster Response Agent",
#         timeout=8
#     )


# def check_for_alerts():
#     """Read latest risk data and trigger alerts"""
#     if not os.path.exists(DATA_FILE):
#         print(Fore.RED + f"[ERROR] No {DATA_FILE} found. Run the agent first." + Style.RESET_ALL)
#         return []

#     df = pd.read_csv(DATA_FILE)
#     if df.empty:
#         print(Fore.YELLOW + "[INFO] Risk log is empty, waiting for data..." + Style.RESET_ALL)
#         return []

#     df.columns = df.columns.str.strip().str.title().str.replace("_", " ")
#     if "Timestamp" in df.columns:
#         df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

#     latest_entries = df.sort_values("Timestamp").groupby("City").tail(1)

#     active_alerts = []

#     for _, row in latest_entries.iterrows():
#         risk_level = str(row.get("Risk Level", "")).lower()
#         if risk_level in RISK_ALERT_LEVELS:
#             send_alert(
#                 city=row.get("City", "Unknown"),
#                 risk_level=risk_level,
#                 risk_score=row.get("Risk Score", "?"),
#                 weather=row.get("Weather", "Unknown"),
#             )
#             active_alerts.append({
#                 "city": row.get("City", "Unknown"),
#                 "risk_level": risk_level,
#                 "risk_score": row.get("Risk Score", "?"),
#                 "weather": row.get("Weather", "Unknown")
#             })

#     # Save current alerts to file for dashboard
#     with open(ALERT_FILE, "w") as f:
#         json.dump(active_alerts, f, indent=4)

#     return active_alerts


# def main():
#     print(Fore.CYAN + "🛰️ Starting Real-Time Alert Monitor...\n" + Style.RESET_ALL)
#     while True:
#         alerts = check_for_alerts()
#         if not alerts:
#             print(Fore.GREEN + "✅ No high/critical alerts at the moment." + Style.RESET_ALL)
#         time.sleep(CHECK_INTERVAL)


# if __name__ == "__main__":
#     main()
import pandas as pd
import time
import os
import json
from colorama import Fore, Style, init
from plyer import notification

# Initialize colorama
init(autoreset=True)

DATA_FILE = "risk_log.csv"
ALERT_FILE = "alerts_status.json"
CHECK_INTERVAL = 30  # seconds
RISK_ALERT_LEVELS = ["high", "critical"]

def send_alert(city, risk_level, risk_score, weather):
    """Display console + desktop alerts"""
    alert_msg = f"🚨 ALERT: {city} | Risk: {risk_level.upper()} | Score: {risk_score} | Weather: {weather}"
    
    color = Fore.RED if risk_level.lower() == "critical" else Fore.YELLOW
    print(color + alert_msg + Style.RESET_ALL)

    # Desktop notification
    try:
        notification.notify(
            title=f"⚠️ {city} Risk Alert!",
            message=f"Risk Level: {risk_level.upper()} | Score: {risk_score}\nWeather: {weather}",
            app_name="Disaster Response Agent",
            timeout=8
        )
    except Exception as e:
        print(Fore.RED + f"[WARN] Desktop notification failed: {e}" + Style.RESET_ALL)


def check_for_alerts():
    """Read latest risk data and trigger alerts"""
    if not os.path.exists(DATA_FILE):
        print(Fore.RED + f"[ERROR] No {DATA_FILE} found. Run the agent first." + Style.RESET_ALL)
        return []

    try:
        df = pd.read_csv(DATA_FILE)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to read {DATA_FILE}: {e}" + Style.RESET_ALL)
        return []

    if df.empty:
        print(Fore.YELLOW + "[INFO] Risk log is empty, waiting for data..." + Style.RESET_ALL)
        return []

    df.columns = df.columns.str.strip().str.title().str.replace("_", " ", regex=False)

    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    
    # Ensure required columns exist
    if "City" not in df.columns:
        print(Fore.RED + "[ERROR] 'City' column not found in risk log." + Style.RESET_ALL)
        return []

    if "Timestamp" in df.columns:
        latest_entries = df.sort_values("Timestamp").groupby("City").tail(1)
    else:
        latest_entries = df.groupby("City").tail(1)

    active_alerts = []

    for _, row in latest_entries.iterrows():
        risk_level = str(row.get("Risk Level", "")).lower()
        if risk_level in RISK_ALERT_LEVELS:
            send_alert(
                city=row.get("City", "Unknown"),
                risk_level=risk_level,
                risk_score=row.get("Risk Score", "?"),
                weather=row.get("Weather", "Unknown"),
            )
            active_alerts.append({
                "city": row.get("City", "Unknown"),
                "risk_level": risk_level,
                "risk_score": row.get("Risk Score", "?"),
                "weather": row.get("Weather", "Unknown")
            })

    # Save current alerts to file for dashboard
    try:
        with open(ALERT_FILE, "w") as f:
            json.dump(active_alerts, f, indent=4, default=str)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to save alerts: {e}" + Style.RESET_ALL)

    return active_alerts


def main():
    print(Fore.CYAN + "🛰️ Starting Real-Time Alert Monitor...\n" + Style.RESET_ALL)
    while True:
        alerts = check_for_alerts()
        if not alerts:
            print(Fore.GREEN + "✅ No high/critical alerts at the moment." + Style.RESET_ALL)
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()