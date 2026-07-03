import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import linregress

st.set_page_config(page_title="Stock Boost Live", layout="wide")
st.title("🚀 STOCK BOOST – Advanced Slow & Steady Trend Scanner")
st.write("Live Indian Market Refined Screener for Institutional Slow Grind Moves")

WATCHLIST = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "SBIN.NS", "BHARTSHIP.NS", 
    "ICICIBANK.NS", "HDFCBANK.NS", "AXISBANK.NS", "ITC.NS", "LT.NS",
    "TATAMOTORS.NS", "M&M.NS", "SUNPHARMA.NS"
]

def analyze_stock(ticker):
    try:
        df = yf.Ticker(ticker).history(period="2d", interval="5m")
        if len(df) < 30:
            return None
        
        recent = df.tail(15).copy()
        
        df['Range'] = df['High'] - df['Low']
        avg_range = df['Range'].rolling(window=20).mean().iloc[-1]
        max_allowed_range = avg_range * 1.4
        
        if recent['Range'].max() > max_allowed_range:
            return None
            
        y = recent['Close'].values
        x = np.arange(len(y))
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        
        is_trending_smoothly = (r_value**2) > 0.60
        
        df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
        recent_ema = df.tail(15)
        
        above_count = (recent_ema['Close'] > recent_ema['EMA_9']).sum()
        below_count = (recent_ema['Close'] < recent_ema['EMA_9']).sum()

        if is_trending_smoothly and slope > 0 and above_count >= 11:
            return "UP"
        elif is_trending_smoothly and slope < 0 and below_count >= 11:
            return "DOWN"
            
        return None
    except:
        return None

if st.button("🔄 Scan Market Structures Live"):
    up_boost = []
    down_boost = []
    
    with st.spinner("Analyzing structures, slopes and volatility channels..."):
        for stock in WATCHLIST:
            result = analyze_stock(stock)
            symbol_name = stock.replace(".NS", "")
            if result == "UP":
                up_boost.append(symbol_name)
            elif result == "DOWN":
                down_boost.append(symbol_name)
                
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🟢 UP SIDE BOOST (Slow Grind Up)")
        if up_boost:
            for s in up_boost:
                st.info(f"📈 **{s}** → Steady Bullish Accumulation")
        else:
            st.write("No stocks matching steady up-trend right now.")
            
    with col2:
        st.markdown("### 🔴 DOWN SIDE BOOST (Slow Grind Down)")
        if down_boost:
            for s in down_boost:
                st.error(f"📉 **{s}** → Steady Bearish Distribution")
        else:
            st.write("No stocks matching steady down-trend right now.")
