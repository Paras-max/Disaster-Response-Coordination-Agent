# # smart_allocator.py
# import pandas as pd
# from collector import get_current_weather
# from nlp import is_distress
# import math

# # --------------------------------------
# # 🚨 SMART RESOURCE ALLOCATION (AI-like)
# # --------------------------------------

# def calculate_risk_score(city, rainfall, distress_reports, population):
#     """
#     Combine multiple real factors to compute a dynamic risk score.
#     """
#     # Normalize each factor (rough scaling)
#     rain_factor = rainfall / 50       # more rain → higher risk
#     distress_factor = distress_reports / 5
#     population_factor = population / 1_000_000

#     # Weighted formula (you can tweak)
#     risk_score = (0.5 * rain_factor) + (0.3 * distress_factor) + (0.2 * population_factor)
#     return round(risk_score, 2)


# def classify_risk(score):
#     """Convert numeric score → risk category."""
#     if score >= 8:
#         return "critical"
#     elif score >= 5:
#         return "high"
#     elif score >= 3:
#         return "medium"
#     else:
#         return "low"


# def allocate_resources(city, risk):
#     """
#     Decide how many resources to send.
#     """
#     allocation = {
#         "low": {"boats": 0, "medical_units": 0, "ndrf_teams": 0},
#         "medium": {"boats": 1, "medical_units": 1, "ndrf_teams": 1},
#         "high": {"boats": 2, "medical_units": 1, "ndrf_teams": 2},
#         "critical": {"boats": 3, "medical_units": 2, "ndrf_teams": 3},
#     }

#     return {"city": city, "risk": risk, "resources": allocation.get(risk, {})}


# # --------------------------------------
# # 🧩 MAIN INTEGRATION FUNCTION
# # --------------------------------------

# def smart_allocate(city, lat, lon, distress_data, population=1000000):
#     """
#     Use live weather + distress tweets + population to allocate resources intelligently.
#     """
#     # 🌦 Get live weather
#     weather = get_current_weather(lat, lon)
#     if not weather or "weather" not in weather:
#         print(f"⚠️ Could not fetch weather for {city}")
#         return None

#     rainfall = weather["main"].get("humidity", 0)  # humidity as proxy for rainfall intensity

#     # 💬 Count distress tweets
#     distress_reports = 0
#     for text in distress_data:
#         if is_distress(text):
#             distress_reports += 1

#     # 🔢 Compute risk score
#     score = calculate_risk_score(city, rainfall, distress_reports, population)
#     risk = classify_risk(score)

#     result = allocate_resources(city, risk)

#     # 🧾 Display results
#     print(f"\n📍 City: {city}")
#     print(f"🌧 Rainfall proxy (humidity): {rainfall}%")
#     print(f"💬 Distress Reports: {distress_reports}")
#     print(f"👥 Population: {population}")
#     print(f"⚠️ Risk Score: {score} → {risk.upper()}")
#     print(f"🚑 Allocated Resources: {result['resources']}")

#     return result


# # --------------------------------------
# # ▶️ MAIN TEST
# # --------------------------------------
# if __name__ == "__main__":
#     # Example simulated data
#     df = pd.read_csv("data.csv")

#     # Assume your data.csv has a column 'message'
#     distress_data = df["message"].tolist() if "message" in df.columns else []

#     # Pune example (you can change)
#     smart_allocate(city="Pune", lat=18.52, lon=73.85, distress_data=distress_data, population=3100000)
# allocator.py
"""
# Smart Resource Allocator for Disaster Response Agent

# Uses distress data (from tweets), weather (humidity/rain),
# and population to compute a dynamic risk score and allocate
# response teams intelligently.
# """

# # ----------------------------------------
# # 🔹 Risk Classification Logic
# # ----------------------------------------
# def classify_risk(score: float) -> str:
#     """Classify numeric risk score into category."""
#     if score >= 8:
#         return "critical"
#     elif score >= 5:
#         return "high"
#     elif score >= 3:
#         return "medium"
#     else:
#         return "low"


# # ----------------------------------------
# # 🔹 Resource Mapping
# # ----------------------------------------
# def resource_mapping():
#     """Returns a mapping of risk → resource allocation."""
#     return {
#         "low": {
#             "boats": 0,
#             "medical_units": 0,
#             "ndrf_teams": 0
#         },
#         "medium": {
#             "boats": 1,
#             "medical_units": 1,
#             "ndrf_teams": 1
#         },
#         "high": {
#             "boats": 2,
#             "medical_units": 2,
#             "ndrf_teams": 2
#         },
#         "critical": {
#             "boats": 3,
#             "medical_units": 3,
#             "ndrf_teams": 3
#         }
#     }


# # ----------------------------------------
# # 🔹 Main Allocation Function
# # ----------------------------------------
# def allocate_resources(city, distress_count, humidity, population=1000000):
#     """
#     Allocate resources based on distress reports, humidity (rain proxy), and population.

#     Parameters:
#         city (str): City name
#         distress_count (int): Number of distress reports detected
#         humidity (float): Humidity from weather data
#         population (int): Population (default = 1,000,000)

#     Returns:
#         dict: {
#             'city': str,
#             'risk_score': float,
#             'risk_level': str,
#             'resources': dict
#         }
#     """

#     # Compute individual weighted factors
#     rain_factor = humidity / 20.0          # 0–5 range
#     distress_factor = distress_count * 1.5 # more distress = higher risk
#     pop_factor = population / 1_000_000.0  # 1 per million

#     # Weighted risk score
#     score = (0.5 * rain_factor) + (0.4 * distress_factor) + (0.1 * pop_factor)

#     # Classify risk
#     risk_level = classify_risk(score)

#     # Pick resources based on risk
#     mapping = resource_mapping()
#     resources = mapping.get(risk_level, {})

#     # Prepare result
#     result = {
#         "city": city,
#         "risk_score": round(score, 2),
#         "risk_level": risk_level,
#         "resources": resources
#     }

#     # Print summary for debugging/logging
#     print(f"📍 City: {city}")
#     print(f"🌧 Humidity: {humidity}% | 💬 Distress Reports: {distress_count}")
#     print(f"⚠️ Risk Score: {result['risk_score']} → {risk_level.upper()}")
#     print(f"🚑 Resources: {resources}")
#     print("—" * 40)

#     return result
"""
Smart Resource Allocator for Disaster Response Agent

Uses distress data (from tweets), weather (humidity/rain),
and population to compute a dynamic risk score and allocate
response teams intelligently.
"""

# # ----------------------------------------
# # 🔹 Risk Classification Logic
# # ----------------------------------------
# def classify_risk(score: float) -> str:
#     """Classify numeric risk score into category."""
#     if score >= 8:
#         return "critical"
#     elif score >= 5:
#         return "high"
#     elif score >= 3:
#         return "medium"
#     else:
#         return "low"


# # ----------------------------------------
# # 🔹 Resource Mapping
# # ----------------------------------------
# def resource_mapping():
#     """Returns a mapping of risk → resource allocation."""
#     return {
#         "low": {
#             "boats": 0,
#             "medical_units": 0,
#             "ndrf_teams": 0
#         },
#         "medium": {
#             "boats": 1,
#             "medical_units": 1,
#             "ndrf_teams": 1
#         },
#         "high": {
#             "boats": 2,
#             "medical_units": 2,
#             "ndrf_teams": 2
#         },
#         "critical": {
#             "boats": 3,
#             "medical_units": 3,
#             "ndrf_teams": 3
#         }
#     }


# # ----------------------------------------
# # 🔹 Main Allocation Function
# # ----------------------------------------
# def allocate_resources(city, weather, distress_count, population=1000000):
#     """
#     Allocate resources based on distress reports, weather data, and population.

#     Parameters:
#         city (str): City name
#         weather (dict): Weather data from API
#         distress_count (int): Number of distress reports detected
#         population (int): Default = 1,000,000

#     Returns:
#         tuple: (resources, risk_score, risk_level)
#     """

#     # 🌦 Extract humidity (acts as rain proxy)
#     humidity = weather.get("main", {}).get("humidity", 0)

#     # Compute factors
#     rain_factor = humidity / 20.0           # 0–5 range
#     distress_factor = distress_count * 1.5  # distress impact
#     pop_factor = population / 1_000_000.0   # scaled population

#     # Weighted risk score
#     score = (0.5 * rain_factor) + (0.4 * distress_factor) + (0.1 * pop_factor)

#     # Classify risk
#     risk_level = classify_risk(score)

#     # Pick resources based on risk
#     mapping = resource_mapping()
#     resources = mapping.get(risk_level, {})

#     # 🧾 Print for live monitoring
#     print(f"📍 City: {city}")
#     print(f"🌧 Humidity: {humidity}% | 💬 Distress Reports: {distress_count}")
#     print(f"⚠️ Risk Score: {round(score,2)} → {risk_level.upper()}")
#     print(f"🚑 Resources: {resources}")
#     print("—" * 40)

#     # Return as tuple for agent + logger
#     return resources, round(score, 2), risk_level

# ----------------------------------------
# 🔹 Risk Classification Logic
# ----------------------------------------
def classify_risk(score: float) -> str:
    """Classify numeric risk score into category."""
    if score >= 8:
        return "critical"
    elif score >= 5:
        return "high"
    elif score >= 3:
        return "medium"
    else:
        return "low"


# ----------------------------------------
# 🔹 Resource Mapping
# ----------------------------------------
def resource_mapping():
    """Returns a mapping of risk → resource allocation."""
    return {
        "low": {
            "Boats": 0,
            "Medical Units": 0,
            "NDRF Teams": 0
        },
        "medium": {
            "Boats": 1,
            "Medical Units": 1,
            "NDRF Teams": 1
        },
        "high": {
            "Boats": 2,
            "Medical Units": 2,
            "NDRF Teams": 2
        },
        "critical": {
            "Boats": 3,
            "Medical Units": 3,
            "NDRF Teams": 3
        }
    }


# ----------------------------------------
# 🔹 Main Allocation Function
# ----------------------------------------
def allocate_resources(city, weather, distress_count, population=1000000):
    """
    Allocate resources based on distress reports, weather data, and population.

    Returns:
        tuple: (resources, risk_score, risk_level)
    """

    # 🌦 Extract humidity (acts as rain proxy)
    humidity = weather.get("main", {}).get("humidity", 0)

    # Compute factors
    rain_factor = humidity / 20.0           # 0–5 range
    distress_factor = distress_count * 1.5  # distress impact
    pop_factor = population / 1_000_000.0   # scaled population

    # Weighted risk score
    score = (0.5 * rain_factor) + (0.4 * distress_factor) + (0.1 * pop_factor)

    # Classify risk
    risk_level = classify_risk(score)

    # Pick resources based on risk
    mapping = resource_mapping()
    resources = mapping.get(risk_level, {})

    # 🧾 Print for live monitoring
    print(f"📍 City: {city}")
    print(f"🌧 Humidity: {humidity}% | 💬 Distress Reports: {distress_count}")
    print(f"⚠️ Risk Score: {round(score,2)} → {risk_level.upper()}")
    print(f"🚑 Resources: {resources}")
    print("—" * 40)

    # Return as tuple for agent + logger
    return resources, round(score, 2), risk_level
