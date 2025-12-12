# src/data_loader.py
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import requests


def load_or_generate_data(path: str, start, end):
    """If CSV exists, load. Otherwise generate simulated orders between start and end."""
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Ensure order_datetime column exists
        if 'order_datetime' not in df.columns:
            raise ValueError('sample_orders.csv missing order_datetime column')
        return df

    # Generate synthetic orders data
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    rng = pd.date_range(start, end, freq='D')
    rows = []
    for day in rng:
        # simulate base order volume
        base = np.random.poisson(lam=200)
        # simulate hourly distribution
        hours = np.random.poisson(lam=base/12, size=24)
        for h, cnt in enumerate(hours):
            for i in range(cnt):
                ts = day + pd.to_timedelta(h, unit='h') + pd.to_timedelta(np.random.randint(0,60), unit='m')
                rows.append({'order_datetime': ts.isoformat(), 'order_value': round(np.random.uniform(80,700),2)})
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return df


def fetch_weather(lat, lon, start_date, end_date):
    """Fetch daily weather summary from Open-Meteo (no API key required).
    Returns DataFrame with columns: date, temperature_2m_mean, precipitation_sum
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}&daily=temperature_2m_mean,precipitation_sum&timezone=UTC"
    )
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    daily = data.get('daily', {})
    df = pd.DataFrame({
        'date': daily.get('time', []),
        'temperature_2m_mean': daily.get('temperature_2m_mean', []),
        'precipitation_sum': daily.get('precipitation_sum', [])
    })
    return df