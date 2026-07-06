import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

# Page config and Title
st.set_page_config(page_title="Stock Boost - Institutional Scanner", layout="wide")
st.title("🚀 STOCK BOOST – Advanced Institutional Flow & Volume Scanner")
st.write("Live Market Smooth Structure & Volume Analytics (3-Minute Auto-Refresh Sequence)")

# 200+ FULL METRIC WATCHLIST
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

# COMPLETE SECTOR MAPPING
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

def analyze_market_batch():
    bullish_stocks = []
    bearish_stocks = []
    volume_gainers = []
    sector_performance = {}

    try:
        data_intraday = yf.download(WATCHLIST, period="2d", interval="15m", group_by='ticker', progress=False)
        data_daily = yf.download(WATCHLIST, period="6d", interval="1d", group_by='ticker', progress=False)
        
        for ticker in WATCHLIST:
            try:
                if ticker not in data_daily.columns.levels[0] or ticker not in data_intraday.columns.levels[0]:
                    continue
                
                t_daily = data_daily[ticker].dropna()
                t_intra = data_intraday[ticker].dropna()

                if len(t_daily) < 2 or len(t_intra) < 6:
                    continue

                prev_day_close = float(t_daily['Close'].iloc[-2])
                avg_hist_vol = float(t_daily['Volume'].iloc[-5:-1].mean())
                current_day_vol = float(t_daily['Volume'].iloc[-1])
                vol_multiplier = current_day_vol / avg_hist_vol if avg_hist_vol > 0 else 1.0

                prices = t_intra['Close'].values.flatten()
                highs = t_intra['High'].values.flatten()
                lows = t_intra['Low'].values.flatten()
                latest_price = float(prices[-1])
                p_change = ((latest_price - prev_day_close) / prev_day_close) * 100

                # --- 1. STRICT CANDLE UNIFORMITY FILTER (ANTI-SPIKE) ---
                candle_bodies = np.abs(t_intra['Close'].values.flatten() - t_intra['Open'].values.flatten())
                avg_body = np.mean(candle_bodies)
                max_body = np.max(candle_bodies[-4:])
                if max_body > (avg_body * 2.2):
                    continue

                # --- 2. ULTRA-STRICT DEEP PULLBACK FILTER ---
                # Checks if the price breaks structural boundaries by dropping too deep from recent high/low peaks
                if latest_price > prev_day_close:  # Potential Bullish Setup
                    highest_recent = np.max(highs[-4:])
                    pullback_depth = ((highest_recent - latest_price) / highest_recent) * 100
                    if pullback_depth > 0.40:  # Strict 0.4% maximum boundary drop limit
                        continue
                else:  # Potential Bearish Setup
                    lowest_recent = np.min(lows[-4:])
                    pullback_depth = ((latest_price - lowest_recent) / lowest_recent) * 100
                    if pullback_depth > 0.40:
                        continue

                # --- 3. DYNAMIC SIDEWAYS SCANNER (2-5 CANDLES LIMIT) ---
                recent_closes = prices[-6:]
                is_stagnant = False
                for i in range(len(recent_closes) - 4):
                    window = recent_closes[i:i+4]
                    window_range = (np.max(window) - np.min(window)) / np.min(window) * 100
                    if window_range < 0.08:  # Strict dead flat noise wall ceiling
                        is_stagnant = True
                        break
                if is_stagnant:
                    continue

                # Calculate EMAs: 9, 15, and 50
                t_intra['EMA_9'] = t_intra['Close'].ewm(span=9, adjust=False).mean()
                t_intra['EMA_15'] = t_intra['Close'].ewm(span=15, adjust=False).mean()
                t_intra['EMA_50'] = t_intra['Close'].ewm(span=50, adjust=False).mean()

                ema9 = float(t_intra['EMA_9'].iloc[-1])
                ema15 = float(t_intra['EMA_15'].iloc[-1])
                ema50 = float(t_intra['EMA_50'].iloc[-1])

                # RSI Calculation
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

                # --- 4. EMA RIBBON ALIGNMENT ---
                if latest_price > ema9 and ema9 > ema15 and ema15 > ema50:
                    bullish_stocks.append(stock_data)
                elif latest_price < ema9 and ema9 < ema15 and ema15 < ema50:
                    bearish_stocks.append(stock_data)

                if vol_multiplier >= 1.5:
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

# Fire Engine Streams
with st.spinner("Connecting to High-Speed Institutional Ribbon Streams..."):
    bullish, bearish, vol_gainers, sectors = analyze_market_batch()

# Layout Build
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🟢 TOP 10 UP SIDE MOVES (Smooth Dynamic Accumulation - Above 50 EMA)")
    if bullish:
        st.dataframe(pd.DataFrame(bullish).sort_values(by="Change %", ascending=False).head(10), use_container_width=True)
    else:
        st.info("Scanning steady trending charts...")

    st.subheader("🔴 TOP 10 DOWN SIDE MOVES (Smooth Dynamic Distribution - Below 50 EMA)")
    if bearish:
        st.dataframe(pd.DataFrame(bearish).sort_values(by="Change %", ascending=True).head(10), use_container_width=True)
    else:
        st.info("Scanning steady trending charts...")

    st.subheader("📊 VOLUME GAINERS (High Volume Activity >= 1.5x Multiplier)")
    if vol_gainers:
        st.dataframe(pd.DataFrame(vol_gainers).sort_values(by="Volume Multiplier", ascending=False), use_container_width=True)
    else:
        st.info("Monitoring liquid arrays for surge patterns...")

with col2:
    st.subheader("🔥 Institutional Sector Heat")
    sector_summary = []
    for sec, changes in sectors.items():
        if changes:
            sector_summary.append({"Sector": sec, "Avg Gain %": round(np.mean(changes), 2)})
    
    if sector_summary:
        st.dataframe(pd.DataFrame(sector_summary).sort_values(by="Avg Gain %", ascending=False), use_container_width=True)
    else:
        st.info("Awaiting structural data loops...")

# 3-Minute Refresh Sequence
time.sleep(180)
st.rerun()
