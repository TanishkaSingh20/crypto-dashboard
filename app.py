import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Crypto Dashboard", layout="wide")

st.title("📊 Cryptocurrency Dashboard")

# -----------------------------
# Load CSV correctly
# -----------------------------
def load_crypto_data(path):

    # Skip first 3 rows
    df = pd.read_csv(path, skiprows=3)

    # Set proper column names
    df.columns = ["date","close","high","low","open","volume"]

    # Convert types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_cols = ["close","high","low","open","volume"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["close"])

    return df


# -----------------------------
# Load CSV files
# -----------------------------
data_folder = "crypto_data"

files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

coin = st.sidebar.selectbox("Select Coin", files)

file_path = os.path.join(data_folder, coin)

data = load_crypto_data(file_path)

st.write("Rows loaded:", len(data))

if len(data) == 0:
    st.error("Dataset empty. Check CSV format.")
    st.stop()

# -----------------------------
# Show dataset
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(data.head())

# -----------------------------
# Price Trend
# -----------------------------
st.subheader("Price Trend")

fig = px.line(data, x="date", y="close", title="Price Over Time")

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Moving Average
# -----------------------------
st.subheader("Moving Average")

data["MA50"] = data["close"].rolling(50).mean()
data["MA200"] = data["close"].rolling(200).mean()

fig2 = px.line(data, x="date", y=["close","MA50","MA200"])

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Volatility
# -----------------------------
st.subheader("Volatility")

data["returns"] = data["close"].pct_change()

fig3 = px.histogram(data, x="returns")

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Simple Prediction
# -----------------------------
st.subheader("Prediction")

last_price = data["close"].iloc[-1]

prediction = last_price * 1.02

st.metric("Predicted Next Price", round(prediction,4))