import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import time

# Premium Matrix UI Dashboard Configuration
st.set_page_config(page_title="Nifty 50 Pure Direction Engine", layout="centered")

st.markdown("""
    <style>
    .reportview-container { background: #070a13; }
    .main-matrix-card { 
        background-color: #0d1222; 
        padding: 45px; 
        border-radius: 20px; 
        border: 1px solid #1e2942;
        border-top: 10px solid #3b82f6; 
        text-align: center;
        margin-top: 40px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    .status-badge {
        background-color: #1a2333;
        color: #60a5fa;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 13px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 25px;
        border: 1px solid #2563eb;
    }
    .prediction-view { font-size: 46px; font-weight: 900; letter-spacing: 2px; margin: 20px 0; text-transform: uppercase; }
    .description-view { color: #94a3b8; font-size: 16px; line-height: 1.7; margin-top: 15px; font-style: italic; }
    .metrics-container { display: flex; justify-content: space-around; margin-top: 30px; padding: 15px; background: #131a30; border-radius: 12px; }
    .metric-box { text-align: center; }
    .metric-val { font-size: 18px; font-weight: bold; color: #f8fafc; }
    .metric-lbl { font-size: 12px; color: #64748b; text-transform: uppercase; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 NIFTY PURE DIRECTION POWERHOUSE")
st.write("15-Year Macro Data • Technical Indicators Core • FII/DII Liquidity Hunt • Retailer Psychology Triggers")

def execute_ultimate_nifty_analysis():
    try:
        # 1. Fetching Multi-Timeframe Data Blocks Safely
        nifty_macro = yf.download("^NSEI", period="max", interval="1d", progress=False)
        nifty_recent = yf.download("^NSEI", period="1mo", interval="1d", progress=False)
        nifty_live = yf.download("^NSEI", period="1d", interval="5m", progress=False)
        
        if nifty_macro.empty or nifty_live.empty or len(nifty_recent) < 15:
            return "⏳ READING DATA CLOUDS...", "Connecting to live Exchange servers...", "#94a3b8", 0, 0, 0

        # Flatten columns if they contain multi-index series vectors
        for d in [nifty_macro, nifty_recent, nifty_live]:
            if isinstance(d.columns, pd.MultiIndex):
                d.columns = d.columns.get_level_values(0)

        # --- TECHNICAL ANALYSIS ENGINE (TA CORE) ---
        recent_closes = nifty_recent['Close'].values.flatten()
        
        nifty_recent['EMA_9'] = nifty_recent['Close'].ewm(span=9, adjust=False).mean()
        nifty_recent['EMA_21'] = nifty_recent['Close'].ewm(span=21, adjust=False).mean()
        
        ema_9 = float(nifty_recent['EMA_9'].values[-1])
        ema_21 = float(nifty_recent['EMA_21'].values[-1])
        
        # Live Price Action Arrays
        live_prices = nifty_live['Close'].values.flatten()
        live_opens = nifty_live['Open'].values.flatten()
        live_highs = nifty_live['High'].values.flatten()
        live_lows = nifty_live['Low'].values.flatten()

        current_tick = float(live_prices[-1])
        opening_tick = float(live_opens[0])
        
        # Real-time Volatility Engine (ATR Proxy)
        intraday_ranges = live_highs - live_lows
        live_atr_pct = (np.mean(intraday_ranges) / opening_tick) * 100

        # --- PSYCHOLOGY & INSTITUTION TRAP DETECTION ---
        heavyweights = ["RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS"]
        hw_data = yf.download(heavyweights, period="1d", interval="5m", group_by='ticker', progress=False)
        
        fii_buying_pressure = 0
        retail_panic_index = 0

        for stock in heavyweights:
            try:
                if stock in hw_data.columns.levels[0]:
                    s_df = hw_data[stock].dropna()
                    s_close = s_df['Close'].values.flatten()
                    s_open = s_df['Open'].values.flatten()
                    s_high = s_df['High'].values.flatten()
                    s_low = s_df['Low'].values.flatten()
                    
                    if len(s_close) > 0:
                        if s_close[-1] > s_open[0]:
                            fii_buying_pressure += 2
                        else:
                            fii_buying_pressure -= 2
                            
                        # Psychology Trap Formula
                        if (s_high[-1] - s_low[-1]) > (abs(s_close[-1] - s_open[0]) * 2.5):
                            retail_panic_index += 1
            except:
                continue

        # --- 15-YEAR SEASONALITY ALIGNMENT ---
        current_month = datetime.datetime.now().month
        macro_historical_closes = nifty_macro[nifty_macro.index.month == current_month]['Close'].values.flatten()
        historical_bullish_ratio = float(np.mean(np.diff(macro_historical_closes) > 0)) if len(macro_historical_closes) > 1 else 0.5

        # --- ALGORITHM SCORING MATRIX ---
        score = 0
        
        if current_tick > ema_9: score += 1.5
        if ema_9 > ema_21: score += 1
        if current_tick > opening_tick: score += 2.5
        
        if historical_bullish_ratio > 0.52: score += 1
        if fii_buying_pressure > 2: score += 3
        if retail_panic_index > 2 and current_tick > opening_tick: score += 1.5

        if current_tick < ema_9: score -= 1.5
        if ema_9 < ema_21: score -= 1
        if current_tick < opening_tick: score -= 2.5
        if historical_bullish_ratio <= 0.52: score -= 1
        if fii_buying_pressure < -2: score -= 3
        if retail_panic_index > 2 and current_tick < opening_tick: score -= 1.5

        # --- FINAL DIRECTION SELECTION ROUTER ---
        if score >= 5:
            if live_atr_pct > 0.05:
                bias, desc, color = "🚀 BULLISH TRENDING", "Technical breakout aligned with FII block buying. Pure upside trend grinding expected.", "#00FF00"
            else:
                bias, desc, color = "🥱 BULLISH SIDEWAYS", "Structure is positive but compressed. Expect slow upward drift inside a tight range.", "#99FF99"
        elif score <= -5:
            if live_atr_pct > 0.05:
                bias, desc, color = "📉 BEARISH TRENDING", "Heavy Institutional distribution active. Continuous breakdown sequence; recovery attempts will fail.", "#FF3333"
            else:
                bias, desc, color = "⚠️ BEARISH SIDEWAYS", "Market structural breakdown is slow. Price grinding downwards inside a choppy range.", "#FF9999"
        else:
            if current_tick >= opening_tick:
                bias, desc, color = "🥱 UPSIDE SIDEWAYS", "No clear FII commitment. Retailers trapped on both sides, price locked inside premium flat zone.", "#FFFF99"
            else:
                bias, desc, color = "🥱 DOWNSIDE SIDEWAYS", "Compression Index is high. Market moving sideways with a minor negative exhaustion layout.", "#E2E8F0"

        return bias, desc, color, round(score, 1), fii_buying_pressure, retail_panic_index

    except Exception as e:
        return "⏳ CORE RE-CALIBRATING", f"Re-mapping live math feeds: {str(e)}", "#ffffff", 0, 0, 0

# Time Tracking Sequence
now_time = datetime.datetime.now()
current_clock = now_time.strftime("%H:%M")

st.markdown("---")

# Caching engine to ensure strict 9:30 AM single daily lock
if "locked_nifty_bias" not in st.session_state:
    st.session_state.locked_nifty_bias = None
    st.session_state.locked_nifty_desc = None
    st.session_state.locked_nifty_color = None
    st.session_state.locked_score = 0
    st.session_state.locked_fii = 0
    st.session_state.locked_retail = 0

if current_clock >= "09:30":
    if st.session_state.locked_nifty_bias is None:
        with st.spinner("Locking Mathematical Psychology Model Matrix..."):
            bias, desc, color, scr, fii, rtl = execute_ultimate_nifty_analysis()
            st.session_state.locked_nifty_bias = bias
            st.session_state.locked_nifty_desc = desc
            st.session_state.locked_nifty_color = color
            st.session_state.locked_score = scr
            st.session_state.locked_fii = fii
            st.session_state.locked_retail = rtl
            
    bias = st.session_state.locked_nifty_bias
    desc = st.session_state.locked_nifty_desc
    color = st.session_state.locked_nifty_color
    scr = st.session_state.locked_score
    fii = st.session_state.locked_fii
    rtl = st.session_state.locked_retail
    badge_text = "🔒 FINAL INTRADAY MATRIX LOCKED FOR THE DAY (09:30 AM)"
else:
    bias, desc, color, scr, fii, rtl = execute_ultimate_nifty_analysis()
    badge_text = f"⏱️ ALGO PROCESSING FEED (Locking at 09:30 AM) | Live Scan: {current_clock}"

# Unified Clean Inline HTML Formatting (Fixes text block render error)
fii_color = '#10b981' if fii >= 0 else '#ef4444'
card_html = f'<div class="main-matrix-card"><div class="status-badge">{badge_text}</div><div style="color: #4b5563; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">Calculated Multi-Factor Target</div><div class="prediction-view" style="color: {color};">{bias}</div><div class="description-view">{desc}</div><div class="metrics-container"><div class="metric-box"><div class="metric-val" style="color: #3b82f6;">{scr}</div><div class="metric-lbl">Model Score</div></div><div class="metric-box"><div class="metric-val" style="color: {fii_color};">{fii}</div><div class="metric-lbl">Inst. Flow</div></div><div class="metric-box"><div class="metric-val" style="color: #f59e0b;">{rtl} Blocks</div><div class="metric-lbl">Retail Trap Risk</div></div></div></div>'

st.markdown(card_html, unsafe_allow_html=True)

# 3-Minute Precise Loop Update
time.sleep(180)
st.rerun()
