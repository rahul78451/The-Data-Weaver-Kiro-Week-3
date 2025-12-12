# src/utils.py
from datetime import datetime


def parse_iso(dt_str):
    return datetime.fromisoformat(dt_str)