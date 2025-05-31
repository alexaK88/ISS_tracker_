# iss_tracker_app.py
import streamlit as st
import json
import matplotlib.pyplot as plt
from urllib.request import urlopen
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import time

def get_iss_location():
    try:
        response = urlopen("http://api.open-notify.org/iss-now.json")
        data = json.loads(response.read())
        lat = float(data['iss_position']['latitude'])
        lon = float(data['iss_position']['longitude'])
        timestamp = data['timestamp']
        return lat, lon, timestamp
    except Exception as e:
        st.error(f"Error fetching ISS data: {e}")
        return None, None, None

def plot_iss_location(lat, lon):
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.plot(lon, lat, marker='o', color='red', markersize=8, transform=ccrs.PlateCarree())
    ax.set_title('Live ISS Position')
    return fig

# --- Streamlit App ---
st.set_page_config(page_title="ISS Tracker", layout="centered")
st.title("🛰️ International Space Station Live Tracker")
st.write("This app shows the live position of the ISS, updating every few seconds.")

# Refresh interval input
interval = st.slider("Update interval (seconds)", min_value=5, max_value=60, value=10)

# Start button
if st.button("Start Tracking"):
    placeholder = st.empty()
    while True:
        lat, lon, timestamp = get_iss_location()
        if lat is not None and lon is not None:
            with placeholder.container():
                st.markdown(f"**Last updated**: {time.ctime(timestamp)}")
                st.markdown(f"**Latitude**: `{lat}`  |  **Longitude**: `{lon}`")
                fig = plot_iss_location(lat, lon)
                st.pyplot(fig)
        time.sleep(interval)
        # required to break loop with rerun (e.g., manual stop or refresh)
        if st.session_state.get("stop", False):
            break
