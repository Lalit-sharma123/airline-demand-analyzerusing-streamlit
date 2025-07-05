import requests
import pandas as pd

def fetch_opensky_data():
    try:
        url = "https://opensky-network.org/api/states/all"
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data["states"], columns=[
            "icao24", "callsign", "origin_country", "time_position", "last_contact",
            "longitude", "latitude", "baro_altitude", "on_ground", "velocity", "heading",
            "vertical_rate", "sensors", "geo_altitude", "squawk", "spi", "position_source"
        ])
        return df
    except Exception as e:
        print("Error fetching OpenSky data:", e)
        return pd.DataFrame()