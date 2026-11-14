# # predictor.py
# import pandas as pd
# from sklearn.linear_model import LinearRegression
# import numpy as np
# from collector import get_current_weather
# from nlp import is_distress
# import os
# import random

# MODEL_FILE = "risk_model.pkl"

# # ----------------------------------------
# # ⚙️ SIMPLE RULE-BASED FLOOD RISK FUNCTION
# # ----------------------------------------
# def predict_flood_risk(city_name, distress_count=0):
#     """
#     Predicts flood risk using weather + distress data.
#     If ML model available, uses it to forecast next-hour risk score.
#     """
#     print(f"\n🌧 Checking flood risk for {city_name}...")

#     coords = {
#         "mumbai": (19.07, 72.87),
#         "pune": (18.52, 73.86),
#         "thane": (19.21, 72.97),
#         "delhi": (28.61, 77.23),
#     }

#     lat, lon = coords.get(city_name.lower(), (19.07, 72.87))
#     weather = get_current_weather(lat, lon)

#     if "main" not in weather:
#         print("⚠️ Could not fetch weather data.")
#         return None

#     rain = weather.get("rain", {}).get("1h", 0)
#     humidity = weather["main"]["humidity"]
#     wind = weather["wind"]["speed"]

#     # ---------------------------
#     # Rule-based scoring (current risk)
#     # ---------------------------
#     score = 0
#     if rain > 10: score += 3
#     elif rain > 5: score += 2
#     elif rain > 2: score += 1

#     if humidity > 85: score += 1
#     if wind > 8: score += 1
#     if distress_count > 3: score += 2
#     elif distress_count > 1: score += 1

#     # Convert to risk level
#     if score >= 6:
#         risk = "🔴 HIGH"
#     elif score >= 3:
#         risk = "🟠 MEDIUM"
#     else:
#         risk = "🟢 LOW"

#     # ---------------------------
#     # AI Forecasting (Next-hour prediction)
#     # ---------------------------
#     forecast_score = forecast_future_risk(rain, humidity, wind, distress_count)
#     forecast_label = interpret_forecast(forecast_score)

#     print(f"🌦 Rain: {rain}mm | 💨 Wind: {wind}m/s | 💧 Humidity: {humidity}%")
#     print(f"📊 Distress Count: {distress_count}")
#     print(f"🚨 Current Risk: {risk}")
#     print(f"⚡ Forecasted Next-Hour Risk: {forecast_label}")

#     return {
#         "current_risk": risk,
#         "forecast_risk": forecast_label,
#         "forecast_score": forecast_score
#     }


# # ----------------------------------------
# # 🤖 ML MODEL TRAINING (Simulated)
# # ----------------------------------------
# def train_model():
#     """Train a simple regression model using dummy past weather-risk data."""
#     X = np.array([
#         [2, 80, 5, 0],
#         [5, 85, 6, 1],
#         [10, 90, 7, 2],
#         [15, 95, 9, 3],
#         [20, 97, 10, 4],
#     ])
#     y = np.array([2, 3, 5, 7, 9])  # risk scores

#     model = LinearRegression()
#     model.fit(X, y)
#     return model


# def forecast_future_risk(rain, humidity, wind, distress):
#     """Use regression to predict future risk score."""
#     model = train_model()
#     future_score = model.predict([[rain, humidity, wind, distress]])[0]
#     return round(float(future_score), 2)


# def interpret_forecast(score):
#     """Convert numeric forecast score to risk label."""
#     if score >= 7:
#         return "🔴 HIGH"
#     elif score >= 4:
#         return "🟠 MEDIUM"
#     else:
#         return "🟢 LOW"


# # ----------------------------------------
# # ▶️ MAIN TEST
# # ----------------------------------------
# if __name__ == "__main__":
#     result = predict_flood_risk("Mumbai", distress_count=4)
#     print(result)
# predictor.py
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import os

# ---------------------------------------------
# 🧠 Forecast Function for All Cities
# ---------------------------------------------
def run_forecast_for_all():
    """
    Trains a lightweight model on existing risk data and
    predicts future risk scores for each city.
    Returns a DataFrame with predicted risk levels.
    """

    # Load dataset
    file_path = "risk_log.csv"
    if not os.path.exists(file_path):
        print("⚠️ risk_log.csv not found! Please run agent first.")
        return pd.DataFrame()

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.title()

    # Basic cleaning
    df = df.dropna(subset=["Risk Score", "City"])
    df["Risk Score"] = pd.to_numeric(df["Risk Score"], errors="coerce")
    df = df.dropna(subset=["Risk Score"])
    df["Humidity"] = pd.to_numeric(df["Humidity"], errors="coerce").fillna(df["Humidity"].mean())

    # Prepare training data
    city_forecasts = []
    for city in df["City"].unique():
        city_data = df[df["City"] == city].copy()

        if len(city_data) < 3:
            # Not enough data points for prediction
            continue

        # Feature Engineering
        city_data["Humidity"] = city_data["Humidity"].fillna(city_data["Humidity"].mean())
        X = np.arange(len(city_data)).reshape(-1, 1)
        y = city_data["Risk Score"].values

        # Train a simple regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict next time-step
        next_index = np.array([[len(city_data)]])
        next_risk = model.predict(next_index)[0]
        next_risk = float(max(0, round(next_risk, 2)))  # Ensure non-negative

        # Assign risk level
        if next_risk >= 8:
            level = " HIGH"
        elif next_risk >= 5:
            level = " MEDIUM"
        else:
            level = " LOW"

        # Append forecast
        city_forecasts.append({
            "City": city,
            "Predicted Risk Score": next_risk,
            "Forecast Risk Level": level,
            "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    forecast_df = pd.DataFrame(city_forecasts)

    # Save results for dashboard
    if not forecast_df.empty:
        forecast_df.to_csv("forecast_log.csv", index=False)
        print("✅ Forecast saved to forecast_log.csv")

    return forecast_df


# ---------------------------------------------
# ▶️ Test Mode (if run directly)
# ---------------------------------------------
if __name__ == "__main__":
    print("Running AI Flood Risk Predictor...\n")
    result = run_forecast_for_all()
    if result.empty:
        print("⚠️ No forecast generated (insufficient data).")
    else:
        print(result)
