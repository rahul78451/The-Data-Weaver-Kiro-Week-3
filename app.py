import streamlit as st
from src.data_loader import load_or_generate_data, fetch_weather
from src.visuals import plot_time_series, plot_scatter
import pandas as pd

st.set_page_config(page_title="The Data Weaver", layout="wide")

st.title("The Data Weaver — Weather vs Food Orders")
st.markdown("Mashup dashboard demo: weather (Open-Meteo) vs simulated food orders")

# Sidebar
st.sidebar.header("Settings")
city = st.sidebar.text_input("City (for weather)", value="Delhi")
latitude = st.sidebar.text_input("Latitude", value="28.6139")
longitude = st.sidebar.text_input("Longitude", value="77.2090")
start_date = st.sidebar.date_input("Start date", value=pd.to_datetime('2025-11-01'))
end_date = st.sidebar.date_input("End date", value=pd.to_datetime('2025-11-30'))

# Load order data (auto-generate if missing)
orders = load_or_generate_data(path="data/sample_orders.csv", start=start_date, end=end_date)

# Fetch weather
weather = fetch_weather(float(latitude), float(longitude), start_date.isoformat(), end_date.isoformat())

st.sidebar.markdown(f"Orders: {orders.shape[0]} rows")
st.sidebar.markdown(f"Weather days: {weather.shape[0]} rows")

# Main layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Orders over time")
    st.plotly_chart(plot_time_series(orders, 'order_datetime', 'order_value', title='Orders over time'))


with col2:
    st.subheader("Temperature over time")
    st.plotly_chart(plot_time_series(weather, 'date', 'temperature_2m_mean', title='Daily Mean Temperature'))

st.subheader("Merge & Correlate")
# Prepare merged dataset: aggregate orders per day and merge with weather
orders_daily = orders.copy()
orders_daily['date'] = pd.to_datetime(orders_daily['order_datetime']).dt.date
orders_agg = orders_daily.groupby('date').size().reset_index(name='orders_count')
orders_agg['date'] = pd.to_datetime(orders_agg['date'])

weather['date'] = pd.to_datetime(weather['date']).dt.date
weather_agg = weather.groupby('date').agg({
    'temperature_2m_mean': 'mean',
    'precipitation_sum': 'sum'
}).reset_index()
weather_agg['date'] = pd.to_datetime(weather_agg['date'])

merged = pd.merge(orders_agg, weather_agg, on='date', how='inner')

st.write(f"Merged rows: {merged.shape[0]}")

st.plotly_chart(plot_scatter(merged, x='temperature_2m_mean', y='orders_count', title='Orders vs Temperature'))

st.plotly_chart(plot_scatter(merged, x='precipitation_sum', y='orders_count', title='Orders vs Precipitation'))

st.markdown("---")

st.subheader("Download merged CSV")
@st.cache_data
def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = to_csv(merged)
st.download_button("Download merged CSV", data=csv, file_name='merged_weather_orders.csv', mime='text/csv')

st.info("Swap datasets by replacing `data/sample_orders.csv` and updating the loader if needed.")