

# import streamlit as st
# import pandas as pd
# import os
# import json
# import plotly.express as px
# import requests
# from streamlit_autorefresh import st_autorefresh
# from streamlit_lottie import st_lottie
# from streamlit_option_menu import option_menu
# from streamlit_extras.let_it_rain import rain

# # ------------------------------
# # ⚙️ CONFIG
# # ------------------------------
# st.set_page_config(page_title="🌍 Disaster Response Dashboard", layout="wide")

# DATA_FILE = "risk_log.csv"
# ALERT_FILE = "alerts_status.json"
# REFRESH_INTERVAL = 30  # seconds
# st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="data_refresh")

# # ------------------------------
# # 🌍 HEADER WITH ANIMATION
# # ------------------------------
# def load_lottie(url):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_weather = load_lottie("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")

# col1, col2 = st.columns([1, 4])
# with col1:
#     st_lottie(lottie_weather, height=100)
# with col2:
#     st.title("🌍 Disaster Response Coordination Dashboard")
#     st.markdown("### Real-time monitoring of risk, weather, and response allocation.")
# st.caption(f"⏱ Auto-refresh every {REFRESH_INTERVAL} seconds.")

# # ------------------------------
# # 🧭 SIDEBAR MENU
# # ------------------------------
# with st.sidebar:
#     selected = option_menu(
#         "📊 Dashboard Menu",
#         ["Overview", "Risk Trends", "Resources", "Alerts"],
#         icons=["map", "graph-up", "truck", "exclamation-triangle"],
#         menu_icon="cast",
#         default_index=0
#     )

# # ------------------------------
# # 📊 LOAD DATA
# # ------------------------------
# if not os.path.exists(DATA_FILE):
#     st.error("❌ No risk_log.csv found. Run the agent first.")
#     st.stop()

# df = pd.read_csv(DATA_FILE)
# df.columns = df.columns.str.strip().str.title().str.replace("_", " ")

# if df.empty:
#     st.warning("⚠️ Risk log file is empty. Wait for the agent to generate data.")
#     st.stop()

# if "Timestamp" in df.columns:
#     df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce", infer_datetime_format=True)

# # Ensure essential columns
# for col in ["City", "Weather", "Humidity", "Risk Score", "Risk Level"]:
#     if col not in df.columns:
#         df[col] = None
# for col in ["Boats", "Medical Units", "Ndrf Teams"]:
#     if col not in df.columns:
#         df[col] = 0

# # ------------------------------
# # 🚨 ALERTS (GLOBAL)
# # ------------------------------
# alerts = []
# if os.path.exists(ALERT_FILE):
#     with open(ALERT_FILE, "r") as f:
#         alerts = json.load(f)

# if alerts:
#     st.markdown(
#         f"""
#         <div style='background-color:#ffcccc;padding:12px;border-radius:10px;animation: blinker 1s linear infinite;'>
#             <b>🚨 ACTIVE ALERTS DETECTED!</b><br>
#             {"<br>".join([f"🌆 {a['city']} — {a['risk_level'].upper()} risk ({a['weather']})" for a in alerts])}
#         </div>
#         <style>@keyframes blinker {{ 50% {{ opacity: 0; }} }}</style>
#         """,
#         unsafe_allow_html=True
#     )
#     # If critical alerts exist → add animation
#     if any(a["risk_level"].lower() == "critical" for a in alerts):
#         rain(emoji="🚨", font_size=54, falling_speed=5, animation_length=1)

# # ------------------------------
# # 🌍 OVERVIEW (MAP)
# # ------------------------------
# if selected == "Overview":
#     st.subheader("🗺️ Latest Risk Updates — Interactive Map")

#     latest_entries = (
#         df.sort_values("Timestamp", na_position="last")
#         .groupby("City", as_index=False)
#         .last()
#     )

#     # Coordinates for map
#     city_coords = {
#         "Mumbai": (19.0760, 72.8777),
#         "Pune": (18.5204, 73.8567),
#         "Delhi": (28.6139, 77.2090),
#         "Chennai": (13.0827, 80.2707),
#     }
#     latest_entries["Latitude"] = latest_entries["City"].map(lambda c: city_coords.get(c, (None, None))[0])
#     latest_entries["Longitude"] = latest_entries["City"].map(lambda c: city_coords.get(c, (None, None))[1])
#     latest_entries = latest_entries.dropna(subset=["Latitude", "Longitude"])

#     color_map = {"Low": "green", "Medium": "yellow", "High": "orange", "Critical": "red"}
#     latest_entries["Color"] = latest_entries["Risk Level"].str.title().map(color_map).fillna("gray")
#     latest_entries["Risk Score"] = pd.to_numeric(latest_entries["Risk Score"], errors="coerce").fillna(0)

#     if latest_entries.empty:
#         st.info("No data to display on map yet.")
#     else:
#         fig = px.scatter_mapbox(
#             latest_entries,
#             lat="Latitude",
#             lon="Longitude",
#             size="Risk Score",
#             color="Risk Level",
#             color_discrete_map=color_map,
#             hover_name="City",
#             hover_data={
#                 "Risk Score": True,
#                 "Weather": True,
#                 "Humidity": True,
#                 "Boats": True,
#                 "Medical Units": True,
#                 "Ndrf Teams": True,
#                 "Latitude": False,
#                 "Longitude": False
#             },
#             size_max=50,
#             zoom=4,
#             height=500
#         )
#         fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
#         st.plotly_chart(fig, use_container_width=True)

#     st.subheader("📋 Latest Data Summary")
#     st.dataframe(latest_entries, use_container_width=True)

# # ------------------------------
# # 📈 RISK TRENDS
# # ------------------------------
# elif selected == "Risk Trends":
#     st.subheader("📈 Risk Score Over Time")
#     if "Timestamp" in df.columns and "City" in df.columns:
#         trend_data = df.pivot_table(values="Risk Score", index="Timestamp", columns="City", aggfunc="last")
#         if trend_data.empty:
#             st.info("Not enough historical data yet.")
#         else:
#             st.line_chart(trend_data)
#     else:
#         st.warning("Missing Timestamp or City columns.")

# # ------------------------------
# # 🧭 RESOURCES
# # ------------------------------
# elif selected == "Resources":
#     st.subheader("🚑 Resource Allocation Overview")
#     st.dataframe(df[["City", "Boats", "Medical Units", "Ndrf Teams", "Risk Level", "Timestamp"]], use_container_width=True)

# # ------------------------------
# # 🚨 ALERTS
# # ------------------------------
# elif selected == "Alerts":
#     st.subheader("🚨 Current Alert Summary")
#     if alerts:
#         st.dataframe(pd.DataFrame(alerts))
#     else:
#         st.success("✅ No active alerts detected.")
# import streamlit as st
# import pandas as pd
# import os
# import json
# import plotly.express as px
# import requests
# from streamlit_autorefresh import st_autorefresh
# from streamlit_lottie import st_lottie
# from streamlit_option_menu import option_menu
# from streamlit_extras.let_it_rain import rain

# # ------------------------------
# # ⚙️ CONFIG
# # ------------------------------
# st.set_page_config(page_title="🌍 Disaster Response Dashboard", layout="wide")

# DATA_FILE = "risk_log.csv"
# ALERT_FILE = "alerts_status.json"
# REFRESH_INTERVAL = 30  # seconds
# st_autorefresh(interval=REFRESH_INTERVAL * 1000, key="data_refresh")

# # ------------------------------
# # 🌍 HEADER WITH ANIMATION
# # ------------------------------
# def load_lottie(url):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_weather = load_lottie("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")

# col1, col2 = st.columns([1, 4])
# with col1:
#     st_lottie(lottie_weather, height=100)
# with col2:
#     st.title("🌍 Disaster Response Coordination Dashboard")
#     st.markdown("### Real-time monitoring of risk, weather, and response allocation.")
# st.caption(f"⏱ Auto-refresh every {REFRESH_INTERVAL} seconds.")

# # ------------------------------
# # 🧭 SIDEBAR MENU
# # ------------------------------
# with st.sidebar:
#     selected = option_menu(
#         "📊 Dashboard Menu",
#         ["Overview", "Risk Trends", "Resources", "Alerts"],
#         icons=["map", "graph-up", "truck", "exclamation-triangle"],
#         menu_icon="cast",
#         default_index=0
#     )

# # ------------------------------
# # 📊 LOAD DATA
# # ------------------------------
# if not os.path.exists(DATA_FILE):
#     st.error("❌ No risk_log.csv found. Run the agent first.")
#     st.stop()

# df = pd.read_csv(DATA_FILE)
# df.columns = df.columns.str.strip().str.title().str.replace("_", " ")

# if df.empty:
#     st.warning("⚠️ Risk log file is empty. Wait for the agent to generate data.")
#     st.stop()

# if "Timestamp" in df.columns:
#     df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce", infer_datetime_format=True)

# # Ensure essential columns
# for col in ["City", "Weather", "Humidity", "Risk Score", "Risk Level"]:
#     if col not in df.columns:
#         df[col] = None
# for col in ["Boats", "Medical Units", "Ndrf Teams"]:
#     if col not in df.columns:
#         df[col] = 0

# # ------------------------------
# # 🚨 ALERTS (GLOBAL)
# # ------------------------------
# alerts = []
# if os.path.exists(ALERT_FILE):
#     with open(ALERT_FILE, "r") as f:
#         alerts = json.load(f)

# if alerts:
#     st.markdown(
#         f"""
#         <div style='background-color:#ffcccc;padding:12px;border-radius:10px;animation: blinker 1s linear infinite;'>
#             <b>🚨 ACTIVE ALERTS DETECTED!</b><br>
#             {"<br>".join([f"🌆 {a['city']} — {a['risk_level'].upper()} risk ({a['weather']})" for a in alerts])}
#         </div>
#         <style>@keyframes blinker {{ 50% {{ opacity: 0; }} }}</style>
#         """,
#         unsafe_allow_html=True
#     )
#     if any(a["risk_level"].lower() == "critical" for a in alerts):
#         rain(emoji="🚨", font_size=54, falling_speed=5, animation_length=1)

# # ------------------------------
# # 🌍 OVERVIEW (MAP)
# # ------------------------------
# if selected == "Overview":
#     st.subheader("🗺️ Latest Risk Updates — Interactive Map")

#     latest_entries = (
#         df.sort_values("Timestamp", na_position="last")
#         .groupby("City", as_index=False)
#         .last()
#     )

#     # ✅ Coordinates for all cities
#     city_coords = {
#         "Mumbai": (19.0760, 72.8777),
#         "Pune": (18.5204, 73.8567),
#         "Delhi": (28.6139, 77.2090),
#         "Chennai": (13.0827, 80.2707),
#         "Phaltan": (17.9915, 74.4317),
#         "Kalamboli": (19.0323, 73.0965)
#     }

#     latest_entries["Latitude"] = latest_entries["City"].map(lambda c: city_coords.get(c, (None, None))[0])
#     latest_entries["Longitude"] = latest_entries["City"].map(lambda c: city_coords.get(c, (None, None))[1])
#     latest_entries = latest_entries.dropna(subset=["Latitude", "Longitude"])

#     color_map = {"Low": "green", "Medium": "yellow", "High": "orange", "Critical": "red"}
#     latest_entries["Color"] = latest_entries["Risk Level"].str.title().map(color_map).fillna("gray")
#     latest_entries["Risk Score"] = pd.to_numeric(latest_entries["Risk Score"], errors="coerce").fillna(0)

#     if latest_entries.empty:
#         st.info("No data to display on map yet.")
#     else:
#         fig = px.scatter_mapbox(
#             latest_entries,
#             lat="Latitude",
#             lon="Longitude",
#             size="Risk Score",
#             color="Risk Level",
#             color_discrete_map=color_map,
#             hover_name="City",
#             hover_data={
#                 "Risk Score": True,
#                 "Weather": True,
#                 "Humidity": True,
#                 "Boats": True,
#                 "Medical Units": True,
#                 "Ndrf Teams": True,
#                 "Latitude": False,
#                 "Longitude": False
#             },
#             size_max=50,
#             zoom=4.8,
#             height=520
#         )
#         fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
#         st.plotly_chart(fig, use_container_width=True)

#     st.subheader("📋 Latest Data Summary")
#     st.dataframe(latest_entries, use_container_width=True)

# # ------------------------------
# # 📈 RISK TRENDS
# # ------------------------------
# elif selected == "Risk Trends":
#     st.subheader("📈 Risk Score Over Time")
#     if "Timestamp" in df.columns and "City" in df.columns:
#         trend_data = df.pivot_table(values="Risk Score", index="Timestamp", columns="City", aggfunc="last")
#         if trend_data.empty:
#             st.info("Not enough historical data yet.")
#         else:
#             st.line_chart(trend_data)
#     else:
#         st.warning("Missing Timestamp or City columns.")

# # ------------------------------
# # 🧭 RESOURCES
# # ------------------------------
# elif selected == "Resources":
#     st.subheader("🚑 Resource Allocation Overview")
#     st.dataframe(df[["City", "Boats", "Medical Units", "Ndrf Teams", "Risk Level", "Timestamp"]], use_container_width=True)

# # ------------------------------
# # 🚨 ALERTS
# # ------------------------------
# elif selected == "Alerts":
#     st.subheader("🚨 Current Alert Summary")
#     if alerts:
#         st.dataframe(pd.DataFrame(alerts))
#     else:
#         st.success("✅ No active alerts detected.")
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit_extras.let_it_rain import rain

st.set_page_config(page_title="🌍 Disaster Response Dashboard", layout="wide")

# ------------------------------------------------------------
# 🌍 Load Lottie Animation
# ------------------------------------------------------------
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_weather = load_lottie("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")

# ------------------------------------------------------------
# 🎨 Header
# ------------------------------------------------------------
col1, col2 = st.columns([1, 4])
with col1:
    st_lottie(lottie_weather, height=100)
with col2:
    st.title("🌍 Disaster Response Coordination Dashboard")
    st.markdown("Real-time monitoring of risk, weather, and AI-based forecasting.")

# ------------------------------------------------------------
# 🗂️ Sidebar Menu
# ------------------------------------------------------------
with st.sidebar:
    selected = option_menu(
        "📊 Dashboard Menu",
        ["Overview", "Risk Trends", "Resources", "Alerts", "AI Predictor"],
        icons=["map", "graph-up", "truck", "exclamation-triangle", "cpu"],
        menu_icon="cast",
        default_index=0
    )

    # ------------------------------
    # ⚙️ Agent Control
    # ------------------------------
    st.markdown("---")
    st.subheader("🧠 Agent Control")

    if st.button("🚀 Start Agent"):
        import subprocess
        subprocess.Popen(["python", "agent.py"])
        st.success("✅ Agent started successfully in background.")

    if st.button("🛑 Stop Agent"):
        with open("stop_agent.flag", "w") as f:
            f.write("stop")
        st.warning("🛑 Stop signal sent. The agent will shut down after current cycle.")

# ------------------------------------------------------------
# 🧾 Load and Clean Data
# ------------------------------------------------------------
@st.cache_data(ttl=30)
def load_data(path):
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.title()
    rename_map = {
        "Ndrf Teams": "NDRF Teams",
        "Ndrf_Teams": "NDRF Teams",
        "Ndrfteams": "NDRF Teams",
        "Medical_Units": "Medical Units"
    }
    df.rename(columns=rename_map, inplace=True)
    for col in ["Timestamp", "City", "Weather", "Humidity", "Risk Score", "Risk Level", "Boats", "Medical Units", "NDRF Teams"]:
        if col not in df.columns:
            df[col] = None
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df[df["City"].astype(str).str.len() > 2]
    return df

data_file = "risk_log.csv"
df = load_data(data_file)
if df is None or df.empty:
    st.warning("⚠️ No data found. Please run the agent first.")
    st.stop()

# ------------------------------------------------------------
# 🗺️ City Coordinates
# ------------------------------------------------------------
city_coords = {
    "mumbai": (19.0760, 72.8777),
    "pune": (18.5204, 73.8567),
    "delhi": (28.6139, 77.2090),
    "chennai": (13.0827, 80.2707),
    "phaltan": (17.9915, 74.4317),
    "kalamboli": (19.025770, 73.101570),
}

def find_coords_for_city(city_name):
    if pd.isna(city_name):
        return (None, None)
    city_lower = str(city_name).lower().strip()
    for key in city_coords.keys():
        if key in city_lower:
            return city_coords[key]
    return (None, None)

latest_entries = df.sort_values("Timestamp").drop_duplicates("City", keep="last")
latest_entries["Latitude"], latest_entries["Longitude"] = zip(*latest_entries["City"].map(find_coords_for_city))
map_df = latest_entries.dropna(subset=["Latitude", "Longitude"]).copy()

critical_count = (latest_entries["Risk Level"].str.lower() == "critical").sum()
avg_risk = pd.to_numeric(latest_entries["Risk Score"], errors="coerce").dropna().mean()
last_updated = df["Timestamp"].max()
total_cities = latest_entries["City"].nunique()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Cities Monitored", int(total_cities))
c2.metric("Critical Alerts", int(critical_count))
c3.metric("Avg Risk Score", round(avg_risk if not pd.isna(avg_risk) else 0, 2))
c4.metric("Last Updated", str(last_updated) if pd.notna(last_updated) else "N/A")

# ------------------------------------------------------------
# 🌐 OVERVIEW TAB
# ------------------------------------------------------------
if selected == "Overview":
    st.subheader("🌐 Real-time Risk Overview")
    selected_cities = st.multiselect("Filter Cities", sorted(latest_entries["City"].unique()))
    color_map = {"Low": "green", "Medium": "orange", "High": "red", "Critical": "darkred"}
    filtered_map_df = map_df if len(selected_cities) == 0 else map_df[map_df["City"].isin(selected_cities)]
    filtered_latest = latest_entries if len(selected_cities) == 0 else latest_entries[latest_entries["City"].isin(selected_cities)]
    if not filtered_map_df.empty:
        fig = px.scatter_mapbox(
            filtered_map_df,
            lat="Latitude",
            lon="Longitude",
            size="Risk Score",
            color="Risk Level",
            color_discrete_map=color_map,
            hover_name="City",
            hover_data={
                "Weather": True,
                "Humidity": True,
                "Boats": True,
                "Medical Units": True,
                "NDRF Teams": True,
            },
            zoom=4,
            height=500,
        )
        fig.update_layout(mapbox_style="carto-positron")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No valid coordinates found for cities.")

    st.markdown("### 🧾 Latest Risk Summary")
    st.dataframe(
        filtered_latest[["City", "Risk Level", "Risk Score", "Boats", "Medical Units", "NDRF Teams", "Timestamp"]],
        use_container_width=True
    )

# ------------------------------------------------------------
# 📈 RISK TRENDS TAB
# ------------------------------------------------------------
elif selected == "Risk Trends":
    st.subheader("📈 Historical Risk Trends")

    selected_city = st.selectbox("Select City", df["City"].unique())
    city_data = df[df["City"] == selected_city]

    if not city_data.empty:
        fig = px.line(
            city_data,
            x="Timestamp", y="Risk Score",
            title=f"Risk Trend — {selected_city}",
            markers=True, color_discrete_sequence=["#ff4b4b"]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for this city.")

# ------------------------------------------------------------
# 🚑 RESOURCES TAB
# ------------------------------------------------------------
elif selected == "Resources":
    st.subheader("🚑 Resource Allocation Summary")
    st.dataframe(
        latest_entries[["City", "Boats", "Medical Units", "NDRF Teams", "Risk Level", "Timestamp"]],
        use_container_width=True
    )

# ------------------------------------------------------------
# 🚨 ALERTS TAB
# ------------------------------------------------------------
elif selected == "Alerts":
    st.subheader("🚨 Active Alerts")

    critical_alerts = latest_entries[latest_entries["Risk Level"].str.lower() == "critical"]

    if not critical_alerts.empty:
        rain(emoji="🚨", font_size=54, falling_speed=5, animation_length=1)
        st.error("🚨 CRITICAL ALERT — Immediate Action Needed!")
        st.dataframe(critical_alerts, use_container_width=True)
    else:
        st.success("✅ No critical alerts at the moment.")

# ------------------------------------------------------------
# 🤖 AI PREDICTOR TAB
# ------------------------------------------------------------
elif selected == "AI Predictor":
    st.subheader("🧠 AI Flood Risk Predictor")

    from predictor import run_forecast_for_all

    if st.button("🚀 Run AI Forecast"):
        with st.spinner("Running AI model... please wait..."):
            forecast_df = run_forecast_for_all()
            st.success("✅ Forecast completed!")
            st.dataframe(forecast_df, use_container_width=True)
            forecast_df.to_csv("forecast_log.csv", index=False)
            st.caption("💾 Results saved to forecast_log.csv")
    else:
        st.info("Click 'Run AI Forecast' to start prediction.")
