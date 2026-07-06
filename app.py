import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

# Page config and Title
st.set_page_config(page_title="Stock Boost - Institutional Scanner", layout="wide")
st.title("🚀 STOCK BOOST – One-Way Institutional Direction Scanner")
st.write("Live 5-Minute Pure Grinding Trends (Strict 9/15 EMA Support & Micro Sideways Filter)")

# 200+ COMPREHENSIVE WATCHLIST
WATCHLIST = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS", "HDFCBANK.NS", "BHARTIARTL.NS",
    "SBIN.NS", "LTIM.NS", "LT.NS", "ITC.NS", "AXISBANK.NS", "KOTAKBANK.NS", "HINDUNILVR.NS",
    "BAJFINANCE.NS", "MARUTI.NS", "M&M.NS", "TATASTEEL.NS", "TATAMOTORS.NS", "POWERGRID.NS",
    "NTPC.NS", "ADANIENT.NS", "ADANIPORTS.NS", "COALINDIA.NS", "SUNPHARMA.NS", "CIPLA.NS",
    "JIOFIN.NS", "GRASIM.NS", "ULTRACEMCO.NS", "INDUSINDBK.NS", "BPCL.NS", "IOC.NS",
    "HINDALCO.NS", "BAJAJFINSV.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "BRITANNIA.NS",
    "NESTLEIND.NS", "WIPRO.NS", "TECHM.NS", "HCLTECH.NS", "ONGC.NS", "APOLLOHOSP.NS",
    "DRREDDY.NS", "DIVISLAB.NS", "SBILIFE.NS", "HDFCLIFE.NS", "BAJAJ-AUTO.NS", "TITAN.NS",
    "ASIANPAINT.NS", "JSWSTEEL.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "DLF.NS", "GODREJPROP.NS",
    "BEL.NS", "HAL.NS", "BHEL.NS", "REC.NS", "PFC.NS", "GAIL.NS", "SAIL.NS", "NMDC.NS",
    "VOLTAS.NS", "DIXON.NS", "POLYCAB.NS", "KEI.NS", "HAVELLS.NS", "AMBUJACEM.NS", "ACC.NS",
    "PIDILITIND.NS", "BERGEPAINT.NS", "COLPAL.NS", "PGHH.NS", "MCDOWELL-N.NS", "VBL.NS",
    "AARTIIND.NS", "ABB.NS", "ABBOTINDIA.NS", "ABCAPITAL.NS", "ABFRL.NS", "ALKEM.NS",
    "ALOKINDS.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASTRAL.NS", "ATUL.NS",
    "AUBANK.NS", "AUROPHARMA.NS", "BALKRISIND.NS", "BALRAMCHIN.NS",
    "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "BATAINDIA.NS", "BHARATFORG.NS",
    "BIOCON.NS", "BOSCHLTD.NS", "BSOFT.NS", "CANBK.NS", "CANFINHOME.NS", "CHAMBLFERT.NS",
    "COFORGE.NS", "CONCOR.NS", "COROMANDEL.NS", "CROMPTON.NS", "CUB.NS", "CUMMINSIND.NS",
    "CYIENT.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DELHIVERY.NS", "EXIDEIND.NS",
    "FEDERALBNK.NS", "FORTIS.NS", "GLENMARK.NS", "GMRINFRA.NS", "GODREJCP.NS", "GRANULES.NS",
    "GUJGASLTD.NS", "GNFC.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HUDCO.NS", "IDBI.NS",
    "IDEA.NS", "IDFC.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", "INDIGO.NS", "INDUSTOWER.NS",
    "IPCALAB.NS", "IRB.NS", "IRCTC.NS", "IRFC.NS", "JKCEMENT.NS", "JSWENERGY.NS", "JUBLFOOD.NS",
    "KALYANKJIL.NS", "LICHSGFIN.NS", "LUPIN.NS", "MANAPPURAM.NS", "MRF.NS", "MGL.NS",
    "MOTHERSON.NS", "MPHASIS.NS", "MRPL.NS", "MUTHOOTFIN.NS", "NATIONALUM.NS", "NAVINFLUOR.NS",
    "NAUKRI.NS", "OBEROIRLTY.NS", "OFSS.NS", "OIL.NS", "PAGEIND.NS", "PEL.NS", "PERSISTENT.NS",
    "PETRONET.NS", "PNB.NS", "PVRINOX.NS", "RAMCOCEM.NS", "RBLBANK.NS", "RECLTD.NS",
    "RVNL.NS", "SHREECEM.NS", "SIEMENS.NS", "SRF.NS", "SUPREMEIND.NS", "SUNTV.NS",
    "SYNGENE.NS", "TATACOMM.NS", "TATACHEM.NS", "TATAELXSI.NS", "TATAPOWER.NS", "TATACONSUM.NS",
    "TORNTPOWER.NS", "TRENT.NS", "TRIDENT.NS", "TVSMOTOR.NS", "UBL.NS", "UCOBANK.NS",
    "UPL.NS", "UNIONBANK.NS", "ZEEL.NS", "ZOMATO.NS", "ZYDUSLIFE.NS", "JINDALSTEL.NS",
    "SJVN.NS", "NHPC.NS", "MAHABANK.NS", "CENTRALBK.NS", "IOB.NS", "SUZLON.NS", "IREDA.NS",
    "GICRE.NS", "NIACL.NS", "LIC.NS", "HINDZINC.NS"
]

SECTOR_MAP = {
    "RELIANCE.NS": "Energy", "ONGC.NS": "Energy", "BPCL.NS": "Energy", "IOC.NS": "Energy", "HPCL.NS": "Energy", "HINDPETRO.NS": "Energy", "OIL.NS": "Energy", "MRPL.NS": "Energy",
    "POWERGRID.NS": "Utilities", "NTPC.NS": "Utilities", "JSWENERGY.NS": "Utilities", "TATAPOWER.NS": "Utilities", "SJVN.NS": "Utilities", "NHPC.NS": "Utilities", "SUZLON.NS": "Utilities", "GAIL.NS": "Utilities", "IGL.NS": "Utilities", "MGL.NS": "Utilities", "GUJGASLTD.NS": "Utilities", "TORNTPOWER.NS": "Utilities",
    "TCS.NS": "IT", "INFY.NS": "IT", "WIPRO.NS": "IT", "TECHM.NS": "IT", "HCLTECH.NS": "IT", "LTIM.NS": "IT", "COFORGE.NS": "IT", "PERSISTENT.NS": "IT", "MPHASIS.NS": "IT", "BSOFT.NS": "IT", "OFSS.NS": "IT", "CYIENT.NS": "IT",
    "HDFCBANK.NS": "Banking", "ICICIBANK.NS": "Banking", "AXISBANK.NS": "Banking", "KOTAKBANK.NS": "Banking", "SBIN.NS": "Banking", "INDUSINDBK.NS": "Banking", "PNB.NS": "Banking", "BANKBARODA.NS": "Banking", "FEDERALBNK.NS": "Banking", "BANDHANBNK.NS": "Banking", "RBLBANK.NS": "Banking", "IDFCFIRSTB.NS": "Banking", "AUBANK.NS": "Banking", "BANKINDIA.NS": "Banking", "MAHABANK.NS": "Banking", "CENTRALBK.NS": "Banking", "IOB.NS": "Banking", "IDBI.NS": "Banking", "UCOBANK.NS": "Banking", "UNIONBANK.NS": "Banking",
    "BAJFINANCE.NS": "Financial Services", "BAJAJFINSV.NS": "Financial Services", "CHOLAFIN.NS": "Financial Services", "SHRIRAMFIN.NS": "Financial Services", "PFC.NS": "Financial Services", "RECLTD.NS": "Financial Services", "MUTHOOTFIN.NS": "Financial Services", "MANAPPURAM.NS": "Financial Services", "LICHSGFIN.NS": "Financial Services", "ABCAPITAL.NS": "Financial Services", "PEL.NS": "Financial Services", "SBILIFE.NS": "Financial Services", "HDFCLIFE.NS": "Financial Services", "LIC.NS": "Financial Services", "GICRE.NS": "Financial Services", "NIACL.NS": "Financial Services", "IREDA.NS": "Financial Services", "HUDCO.NS": "Financial Services", "IDFC.NS": "Financial Services",
    "MARUTI.NS": "Auto", "TATAMOTORS.NS": "Auto", "M&M.NS": "Auto", "EICHERMOT.NS": "Auto", "HEROMOTOCO.NS": "Auto", "BAJAJ-AUTO.NS": "Auto", "TVSMOTOR.NS": "Auto", "ASHOKLEY.NS": "Auto", "BHARATFORG.NS": "Auto", "BALKRISIND.NS": "Auto", "APOLLOTYRE.NS": "Auto", "EXIDEIND.NS": "Auto", "MOTHERSON.NS": "Auto", "BOSCHLTD.NS": "Auto",
    "TATASTEEL.NS": "Metals", "HINDALCO.NS": "Metals", "JSWSTEEL.NS": "Metals", "SAIL.NS": "Metals", "NMDC.NS": "Metals", "JINDALSTEL.NS": "Metals", "NATIONALUM.NS": "Metals", "HINDCOPPER.NS": "Metals", "HINDZINC.NS": "Metals",
    "SUNPHARMA.NS": "Pharma", "CIPLA.NS": "Pharma", "DRREDDY.NS": "Pharma", "DIVISLAB.NS": "Pharma", "APOLLOHOSP.NS": "Pharma", "ZYDUSLIFE.NS": "Pharma", "LUPIN.NS": "Pharma", "AUROPHARMA.NS": "Pharma", "ALKEM.NS": "Pharma", "BIOCON.NS": "Pharma", "FORTIS.NS": "Pharma", "GLENMARK.NS": "Pharma", "IPCALAB.NS": "Pharma", "GRANULES.NS": "Pharma", "SYNGENE.NS": "Pharma", "ABBOTINDIA.NS": "Pharma",
    "ITC.NS": "FMCG", "HINDUNILVR.NS": "FMCG", "BRITANNIA.NS": "FMCG", "NESTLEIND.NS": "FMCG", "VBL.NS": "FMCG", "COLPAL.NS": "FMCG", "DABUR.NS": "FMCG", "TATACONSUM.NS": "FMCG", "MCDOWELL-N.NS": "FMCG", "UBL.NS": "FMCG", "PGHH.NS": "FMCG", "BALRAMCHIN.NS": "FMCG",
    "DLF.NS": "Real Estate", "GODREJPROP.NS": "Real Estate", "OBEROIRLTY.NS": "Real Estate",
    "LT.NS": "Capital Goods", "BEL.NS": "Capital Goods", "HAL.NS": "Capital Goods", "BHEL.NS": "Capital Goods", "ABB.NS": "Capital Goods", "SIEMENS.NS": "Capital Goods", "VOLTAS.NS": "Capital Goods", "CUMMINSIND.NS": "Capital Goods",
    "DIXON.NS": "Consumer Durables", "POLYCAB.NS": "Consumer Durables", "KEI.NS": "Consumer Durables", "HAVELLS.NS": "Consumer Durables", "TITAN.NS": "Consumer Durables", "ASTRAL.NS": "Consumer Durables", "KALYANKJIL.NS": "Consumer Durables", "CROMPTON.NS": "Consumer Durables", "BATAINDIA.NS": "Consumer Durables",
    "GRASIM.NS": "Materials", "ULTRACEMCO.NS": "Materials", "AMBUJACEM.NS": "Materials", "ACC.NS": "Materials", "PIDILITIND.NS": "Materials", "BERGEPAINT.NS": "Materials", "ASIANPAINT.NS": "Materials", "SHREECEM.NS": "Materials", "JKCEMENT.NS": "Materials", "RAMCOCEM.NS": "Materials", "DEEPAKNTR.NS": "Materials", "AARTIIND.NS": "Materials", "ATUL.NS": "Materials", "SRF.NS": "Materials", "NAVINFLUOR.NS": "Materials", "CHAMBLFERT.NS": "Materials", "GNFC.NS": "Materials", "SUPREMEIND.NS": "Materials", "TATACHEM.NS": "Materials",
    "BHARTIARTL.NS": "Telecom", "INDUSTOWER.NS": "Telecom", "TATACOMM.NS": "Telecom",
    "ADANIENT.NS": "Conglomerates", "JIOFIN.NS": "Financial Services",
    "ADANIPORTS.NS": "Services", "CONCOR.NS": "Services", "DELHIVERY.NS": "Services", "INDIGO.NS": "Services", "IRCTC.NS": "Services", "RVNL.NS": "Services", "ZOMATO.NS": "Services", "JUBLFOOD.NS": "Services", "PVRINOX.NS": "Services", "SUNTV.NS": "Services", "ZEEL.NS": "Services", "NAUKRI.NS": "Services", "TRENT.NS": "Services", "IRB.NS": "Services", "TRIDENT.NS": "Services"
}

def predict_nifty_bias():
    try:
        nifty_daily = yf.download("^NSEI", period="6d", interval="1d", progress=False)
        nifty_intra = yf.download("^NSEI", period="1d", interval="5m", progress=False)
        if nifty_daily.empty or len(nifty_daily) < 5 or nifty_intra.empty:
            return "⏳ Awaiting Trend Matrix Data", "gray"
        closes = nifty_daily['Close'].values.flatten()
        nifty_daily['EMA_5'] = nifty_daily['Close'].ewm(span=5, adjust=False).mean()
        latest_ema = float(nifty_daily['EMA_5'].iloc[-1])
        intra_prices = nifty_intra['Close'].values.flatten()
        current_live_price = float(intra_prices[-1])
        consecutive_ups = sum(1 for i in range(-4, 0) if closes[i] > closes[i-1])
        daily_returns = np.abs(np.diff(closes[-5:]) / closes[-5:-1]) * 100
        avg_volatility = np.mean(daily_returns)

        if current_live_price >= latest_ema and consecutive_ups >= 2:
            if avg_volatility > 0.45:
                return "🚀 BULLISH TRENDING (Strong Up Side Flow)", "#00FF00"
            else:
                return "🥱 BULLISH SIDEWAYS (Slow Creeping Up Side)", "#99FF99"
        elif current_live_price < latest_ema and consecutive_ups <= 2:
            if avg_volatility > 0.45:
                return "📉 BEARISH TRENDING (Strong Down Side Pressure)", "#FF3333"
            else:
                return "⚠️ BEARISH SIDEWAYS (Slow Structural Drop)", "#FF9999"
        else:
            return "🥱 COMPLETELY SIDEWAYS (Dead Rangebound Floor)", "#FFFF99"
    except Exception:
        return "⏳ Syncing Nifty Pulse Clouds...", "white"

def analyze_market_batch():
    bullish_stocks = []
    bearish_stocks = []
    volume_gainers = []
    sector_performance = {}

    try:
        data_intraday = yf.download(WATCHLIST, period="1d", interval="5m", group_by='ticker', progress=False)
        data_daily = yf.download(WATCHLIST, period="5d", interval="1d", group_by='ticker', progress=False)
        
        for ticker in WATCHLIST:
            try:
                if ticker not in data_daily.columns.levels[0] or ticker not in data_intraday.columns.levels[0]:
                    continue
                
                t_daily = data_daily[ticker].dropna()
                t_intra = data_intraday[ticker].dropna()

                if len(t_daily) < 2 or len(t_intra) < 15:
                    continue

                prev_day_close = float(t_daily['Close'].iloc[-2])
                
                # --- PRESENT TIME VOLUME ENGINE VS MULTI-DAY AVERAGE ---
                avg_hist_vol = float(t_daily['Volume'].iloc[-4:].mean())
                recent_intra_vol = float(t_intra['Volume'].iloc[-4:].mean()) * 75  # Normalized volume pulse
                vol_multiplier = recent_intra_vol / avg_hist_vol if avg_hist_vol > 0 else 1.0

                prices = t_intra['Close'].values.flatten()
                highs = t_intra['High'].values.flatten()
                lows = t_intra['Low'].values.flatten()
                latest_price = float(prices[-1])
                p_change = ((latest_price - prev_day_close) / prev_day_close) * 100

                # --- 1. STALWART CANDLE SIZE CONSTRAINT (SMALL CANDLES ONLY) ---
                candle_bodies = np.abs(t_intra['Close'].values.flatten() - t_intra['Open'].values.flatten())
                avg_body = np.mean(candle_bodies)
                max_recent_body = np.max(candle_bodies[-3:])
                if max_recent_body > (avg_body * 1.8):  # Rejects massive volatile spikes
                    continue

                # --- 2. ULTRA-STRICT PULLBACK ENGINE (MAX 0.18% REVERSION BOUNDARY) ---
                if latest_price > prev_day_close:
                    highest_peak = np.max(highs[-4:])
                    pullback = ((highest_peak - latest_price) / highest_peak) * 100
                    if pullback > 0.18:  # Instant termination for sudden deep drops
                        continue
                else:
                    lowest_peak = np.min(lows[-4:])
                    pullback = ((latest_price - lowest_peak) / lowest_peak) * 100
                    if pullback > 0.18:
                        continue

                # --- 3. DYNAMIC SIDEWAYS DECAY FILTER (MAX 3-4 CANDLES CEILING) ---
                # Rejects if more than 4 candles freeze in a dead tight corridor
                recent_closes = prices[-8:]
                is_extensively_sideways = False
                for i in range(len(recent_closes) - 5):
                    window = recent_closes[i:i+5]  # 5 candles check window
                    w_range = (np.max(window) - np.min(window)) / np.min(window) * 100
                    if w_range < 0.10:  # Dead horizontal channel cap
                        is_extensively_sideways = True
                        break
                if is_extensively_sideways:
                    continue

                # --- 4. 9 & 15 EMA ONE-WAY RIDING LOGIC ---
                t_intra['EMA_9'] = t_intra['Close'].ewm(span=9, adjust=False).mean()
                t_intra['EMA_15'] = t_intra['Close'].ewm(span=15, adjust=False).mean()

                ema9_arr = t_intra['EMA_9'].values
                ema15_arr = t_intra['EMA_15'].values
                
                # Check if lines are smoothly tilted and consecutive support is respected
                is_bullish_ride = (prices[-1] > ema9_arr[-1] > ema15_arr[-1]) and (ema9_arr[-1] > ema9_arr[-2] > ema9_arr[-3])
                is_bearish_ride = (prices[-1] < ema9_arr[-1] < ema15_arr[-1]) and (ema9_arr[-1] < ema9_arr[-2] < ema9_arr[-3])

                # RSI (14) Engine
                delta = t_intra['Close'].diff()
                gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
                loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs.iloc[-1])) if not np.isnan(rs.iloc[-1]) else 50.0

                sector = SECTOR_MAP.get(ticker, "Other Tickers Block")
                stock_data = {
                    "Stock Name": ticker.replace(".NS", ""),
                    "Sector": sector,
                    "Live Price": round(latest_price, 2),
                    "Change %": round(p_change, 2),
                    "RSI (14)": round(rsi, 2)
                }

                if is_bullish_ride:
                    bullish_stocks.append(stock_data)
                elif is_bearish_ride:
                    bearish_stocks.append(stock_data)

                # Present time volume surge verification
                if vol_multiplier >= 1.5 and (is_bullish_ride or is_bearish_ride):
                    vol_data = stock_data.copy()
                    vol_data["Volume Multiplier"] = f"{round(vol_multiplier, 2)}x"
                    volume_gainers.append(vol_data)

                if sector not in sector_performance:
                    sector_performance[sector] = []
                sector_performance[sector].append(p_change)

            except Exception:
                continue
    except Exception:
        pass

    return bullish_stocks, bearish_stocks, volume_gainers, sector_performance

# Cloud Core Processing Stream
with st.spinner("Filtering Pure One-Way 5m Grinding Structural Channels..."):
    bullish, bearish, vol_gainers, sectors = analyze_market_batch()

# Layout Design Setup
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🟢 ONE-WAY UP SIDE MOVES (Riding 9 & 15 EMA smoothly with Small Candles)")
    if bullish:
        st.dataframe(pd.DataFrame(bullish).sort_values(by="Change %", ascending=False).head(10), use_container_width=True)
    else:
        st.info("Scanning for clean micro-grinding bullish trajectories...")

    st.subheader("🔴 ONE-WAY DOWN SIDE MOVES (Dropping below 9 & 15 EMA with Small Candles)")
    if bearish:
        st.dataframe(pd.DataFrame(bearish).sort_values(by="Change %", ascending=True).head(10), use_container_width=True)
    else:
        st.info("Scanning for clean micro-grinding bearish trajectories...")

    st.subheader("📊 TRENDING VOLUME GAINERS (High Live Active Volume + One-Way Rider Active)")
    if vol_gainers:
        st.dataframe(pd.DataFrame(vol_gainers).sort_values(by="Volume Multiplier", ascending=False), use_container_width=True)
    else:
        st.info("Monitoring immediate volume blocks on active trends...")

with col2:
    st.subheader("🔥 Institutional Sector Heat")
    sector_summary = []
    for sec, changes in sectors.items():
        if changes:
            sector_summary.append({"Sector": sec, "Avg Gain %": round(np.mean(changes), 2)})
    
    if sector_summary:
        st.dataframe(pd.DataFrame(sector_summary).sort_values(by="Avg Gain %", ascending=False), use_container_width=True)
    else:
        st.info("Awaiting macro loop tracks...")

    # --- NIFTY HYPER LOGIC DIRECTION BOX ---
    st.markdown("---")
    st.subheader("🎯 Today's Nifty Direction Bias")
    bias_text, color_code = predict_nifty_bias()
    st.markdown(f"""
        <div style="background-color:#11151c; padding:20px; border-radius:10px; border-left: 8px solid {color_code};">
            <h4 style="margin:0; color:white; font-size:16px;">Calculated Multi-Day Momentum Trend Matrix:</h4>
            <p style="margin:10px 0 0 0; color:{color_code}; font-size:20px; font-weight:bold;">{bias_text}</p>
        </div>
    """, unsafe_allow_html=True)

# 5-Minute Auto Refresh Loop
time.sleep(300)
st.rerun()
