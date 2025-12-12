# src/visuals.py
import plotly.express as px
import pandas as pd


def plot_time_series(df, x, y, title=None):
    fig = px.line(df, x=x, y=y, title=title)
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig


def plot_scatter(df, x, y, title=None):
    fig = px.scatter(df, x=x, y=y, trendline='ols', title=title)
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return fig