import streamlit as st
from scraper import fetch_opensky_data
from processor import analyze_trends
import pandas as pd

st.set_page_config(page_title="Airline Booking Demand Dashboard", layout="wide")
st.title("✈️ Airline Booking Demand Dashboard")

with st.spinner("Fetching live flight data..."):
    df = fetch_opensky_data()

if df.empty:
    st.error("Failed to fetch data. Please try again later.")
else:
    st.success("Data loaded successfully!")

    # Sidebar filters
    st.sidebar.header("🔍 Filter Options")
    all_countries = df['origin_country'].dropna().unique().tolist()
    selected_countries = st.sidebar.multiselect("Select Country", sorted(all_countries), default=all_countries[:5])
    on_ground_filter = st.sidebar.radio("Flight Status", options=["All", "On Ground", "In Air"])

    # Apply filters
    if selected_countries:
        df = df[df['origin_country'].isin(selected_countries)]
    if on_ground_filter == "On Ground":
        df = df[df['on_ground'] == True]
    elif on_ground_filter == "In Air":
        df = df[df['on_ground'] == False]

    st.subheader("Filtered Flight Data")
    st.dataframe(df.head(20), use_container_width=True)

    # Export to Excel
    @st.cache_data
    def convert_df_to_excel(dataframe):
        return dataframe.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_excel(df)
    st.download_button("⬇️ Download as CSV", csv, "filtered_flight_data.csv", "text/csv")

    st.subheader("Trend Analysis")
    if not df.empty:
        analysis = analyze_trends(df)
        st.write("### Top 5 Countries by Flight Origin")
        st.bar_chart(pd.Series(analysis["top_countries"]))

        st.write("### Flights On Ground vs In Air")
        st.bar_chart(pd.Series(analysis["on_ground_ratio"]))
    else:
        st.warning("No data to analyze after applying filters.")