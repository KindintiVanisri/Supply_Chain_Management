from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import random

# === Load and Clean Data ===
df = pd.read_csv("cleaned_supply_chain_data.csv")
df.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace infs with NaN
df.fillna(0, inplace=True)  # Replace NaNs with 0

# === Initialize FastAPI App ===
app = FastAPI()

# Enable CORS so Streamlit frontend can access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# === Endpoint 1: All Data ===
@app.get("/all_data")
def get_all_data():
    return df.to_dict(orient="records")

# === Endpoint 2: Forecast (Simulated for now) ===
@app.get("/forecast/{product_id}")
def forecast(product_id: str):
    # Simulate a 30-day forecast with random values
    forecast_dates = pd.date_range(start="2025-08-08", periods=30, freq='D')
    forecast = [{"ds": str(date), "yhat": round(random.uniform(50, 150), 2)} for date in forecast_dates]
    return forecast

# === Endpoint 3: Inventory Optimization ===
@app.get("/inventory_optimize/{product_id}")
def optimize_inventory(product_id: str):
    product_data = df[df['Product ID'] == product_id]

    if product_data.empty:
        return {"error": "Product not found"}

    stock = product_data['Stock levels'].mean() or 100
    order = product_data['Order quantities'].mean() or 80
    safety_stock = int(stock * 0.2)
    reorder_point = int(stock * 0.5)

    return {
        "product_id": product_id,
        "reorder_point": reorder_point,
        "safety_stock": safety_stock,
        "recommended_order_quantity": int(order)
    }

# === Endpoint 4: Market Sentiment (Dummy for now) ===
@app.post("/market_analysis")
def analyze_market(text: str):
    sentiment = "Positive" if "good" in text.lower() or "increase" in text.lower() else "Negative"
    return {
        "sentiment": sentiment,
        "confidence": round(random.uniform(0.7, 0.99), 2),
        "suggested_action": "Increase inventory" if sentiment == "Positive" else "Review supply sources"
    }