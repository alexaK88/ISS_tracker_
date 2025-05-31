import streamlit as st
import json
import pandas as pd
import pydeck as pdk
from urllib.request import urlopen
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every N seconds
interval_sec = st.slider("Refresh interval (seconds)", 5, 60, 10)
st_autorefresh(interval=interval_sec * 1000, key="iss_refresh")

st.title("🛰️ ISS Live Tracker")


# Get current ISS position
def get_iss_position():
    try:
        response = urlopen("http://api.open-notify.org/iss-now.json")
        data = json.loads(response.read())
        lat = float(data["iss_position"]["latitude"])
        lon = float(data["iss_position"]["longitude"])
        return lat, lon
    except Exception as e:
        st.error(f"Could not fetch ISS data: {e}")
        return None, None


lat, lon = get_iss_position()
if lat and lon:
    df = pd.DataFrame([[lat, lon]], columns=["lat", "lon"])

    # Map using pydeck
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v11',
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=1,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[255, 0, 0, 160]',
                get_radius=100000,
            ),
        ],
    ))
    st.write(f"📍 Current ISS Coordinates:\n- **Latitude**: `{lat}`\n- **Longitude**: `{lon}`")
