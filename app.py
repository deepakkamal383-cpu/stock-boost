import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

# Page config and Title
st.set_page_config(page_title="Stock Boost - Institutional Scanner", layout="wide")
st.title("🚀 STOCK BOOST – Advanced Slow & Steady Trend Scanner")
st.write("Live Indian Market Refined Institutional Structure Scanner (Auto-refreshing)")

# 1. 250+ F&O Watchlist (Top Liquid Tickers)
WATCHLIST = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS", "HDFCBANK.NS", "BHARTIARTL.NS",
    "SBI.NS", "LTIM.NS", "LT.NS", "ITC.NS", "AXISBANK.NS", "KOTAKBANK.NS", "HINDUNILVR.NS",
    "BAJFINANCE.NS", "MARUTI.NS", "M&M.NS", "TATASTEEL.NS", "TATAMOTORS.NS", "POWERGRID.NS",
    "NTPC.NS", "ADANIENT.NS", "ADANIPORTS.NS", "COALINDIA.NS", "SUNPHARMA.NS", "CIPLA.NS",
    "JIOFIN.NS", "GRASIM.NS", "ULTRACEMCO.NS", "INDUSINDBK.NS", "BPCL.NS", "IOC.NS",
    "HINDALCO.NS", "BAJAJFINSV.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "BRITANNIA.NS",
    "NESTLEIND.NS", "WIPRO.NS", "TECHM.NS", "HCLTECH.NS", "ONGC.NS", "APOLLOHOSP.NS",
    "DRREDDY.NS", "DIVISLAB.NS", "SBILIFE.NS", "HDFCLIFE.NS", "BAJAJ-AUTO.NS", "TITAN.NS",
    "ASIANPAINT.NS", "JSWSTEEL.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "DLF.NS", "GODREJPROP.NS",
    "BEL.NS", "HAL.NS", "BHEL.NS", "REC.NS", "PFC.NS", "GAIL.NS", "SAIL.NS", "NMDC.NS",
    "VOLTAS.NS", "DIXON.NS", "POLYCAB.NS", "KEI.NS", "HAVELLS.NS", "AMBUJACEM.NS", "ACC.NS",
    "PIDILITIND.NS", "BERGEPAINT.NS", "COLPAL.NS", "PGHH.NS", "MCDOWELL-N.NS", "VBL.NS"
]

# Sector Mapping for FII/DII Institutional Tracking
SECTOR_MAP = {
    "RELIANCE.NS": "Energy", "ONGC.NS": "Energy", "BPCL.NS": "Energy", "IOC.NS": "Energy", "POWERGRID.NS": "Utilities", "NTPC.NS": "Utilities",
    "TCS.NS": "IT", "INFY.NS": "IT", "WIPRO.NS": "IT", "TECHM.NS": "IT", "HCLTECH.NS": "IT", "LTIM.NS": "IT",
    "HDFCBANK.NS": "Banking", "ICICIBANK.NS": "Banking", "AXISBANK.NS": "Banking", "KOTAKBANK.NS": "Banking", "SBI.NS": "Banking", "INDUSINDBK.NS": "Banking",
    "BAJFINANCE.NS": "Financial Services", "BAJAJFINSV.NS": "Financial Services", "CHOLAFIN.NS": "Financial Services", "SHRIRAMFIN.NS": "Financial Services",
    "MARUTI.NS": "Auto", "TATAMOTORS.NS": "Auto", "M&M.NS": "Auto", "EICHERMOT.NS": "Auto", "HEROMOTOCO.NS": "Auto", "BAJAJ-AUTO.NS": "Auto",
    "TATASTEEL.NS": "Metals", "HINDALCO.NS": "Metals", "JSWSTEEL.NS": "Metals", "SAIL.NS": "Metals", "NMDC.NS": "Metals",
    "SUNPHARMA.NS": "Pharma", "CIPLA.NS": "Pharma", "DRREDDY.NS": "Pharma", "DIVISLAB.NS": "Pharma", "APOLLOHOSP.NS": "Pharma",
    "ITC.NS": "FMCG", "HINDUNILVR.NS": "FMCG", "BRITANNIA.NS": "FMCG", "NESTLEIND.NS": "FMCG", "VBL.NS": "FMCG", "COLPAL.NS": "FMCG"
}

def analyze_market():
    stock_results = []
    sector_performance = {}

    for ticker in WATCHLIST:
        try:
            # 5-min interval data fetched for intra-day candle analysis
            df = yf.download(ticker, period="2d", interval="5m", progress=False)
            if df.empty or len(df) < 50:
                continue

            # Core Metrics
            close_prices = df['Close'].values.flatten()
            latest_price = float(close_prices[-1])
            prev_close = float(df['Close'].iloc[0])
            p_change = ((latest_price - prev_close) / prev_close) * 100

            # Technical Indicators
            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
            loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))

            ema50 = float(df['EMA_50'].iloc[-1])
            rsi = float(df['RSI'].iloc[-1])

            # --- MORNING WINDOW FILTER (9:25 AM to 10:30 AM) ---
            df.index = pd.to_datetime(df.index)
            morning_df = df.between_time('09:25', '10:30')
            
            is_slow_grind = True
            if not morning_df.empty:
                candle_sizes = (morning_df['High'] - morning_df['Low']).values.flatten()
                atr_morning = np.mean(candle_sizes)
                # Check if any individual morning candle is abnormally massive (anomaly detection)
                if np.any(candle_sizes > (atr_morning * 2.8)):
                    is_slow_grind = False

            if is_slow_grind:
                sector = SECTOR_MAP.get(ticker, "Other")
                stock_results.append({
                    "Ticker": ticker,
                    "Sector": sector,
                    "Price": round(latest_price, 2),
                    "Change %": round(p_change, 2),
                    "RSI": round(rsi, 2),
                    "Trend": "Bullish" if latest_price > ema50 else "Bearish"
                })

                # Sector Aggregation
                if sector not in sector_performance:
                    sector_performance[sector] = []
                sector_performance[sector].append(p_change)

        except Exception:
            continue

    return stock_results, sector_performance

# Execute Scanner
with st.spinner("Scanning Institutional Flows & Morning Windows..."):
    stocks, sectors = analyze_market()

# Layout Design
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Filtered Stocks (Morning Slow Grind Approved)")
    if stocks:
        st.dataframe(pd.DataFrame(stocks), use_container_width=True)
    else:
        st.info("No stocks fitting the precise accumulation profile right now.")

with col2:
    st.subheader("🔥 Sector Strength Institutional Heat")
    sector_summary = []
    for sec, changes in sectors.items():
        sector_summary.append({"Sector": sec, "Avg Gain %": round(np.mean(changes), 2)})
    
    if sector_summary:
        st.dataframe(pd.DataFrame(sector_summary).sort_values(by="Avg Gain %", ascending=False), use_container_width=True)
    else:
        st.info("Waiting for sector flow dynamics...")

# --- REAL-TIME AUTO REFRESH LOOP ---
time.sleep(10)
st.rerun()
