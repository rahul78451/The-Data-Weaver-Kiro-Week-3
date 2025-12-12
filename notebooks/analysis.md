# Analysis Notebook

This notebook documents exploratory analysis and experiments.

1. Load `data/sample_orders.csv` and `src/data_loader.fetch_weather` results.
2. Aggregate orders per day.
3. Plot correlations and compute Pearson r.

Example code snippet:

```python
import pandas as pd
from src.data_loader import load_or_generate_data, fetch_weather
orders = load_or_generate_data('data/sample_orders.csv', '2025-11-01', '2025-11-30')
weather = fetch_weather(28.6139,77.2090,'2025-11-01','2025-11-30')