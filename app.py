import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

# Page config and Title
st.set_page_config(page_title="Stock Boost - Institutional Scanner", layout="wide")
st.title("🚀 STOCK BOOST – Advanced Institutional Flow & Volume Scanner")
st.write("Live Market Smooth Structure & Volume Analytics (Persistent Off-Market Display)")

# 1. COMPLETE F&O WATCHLIST
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
    "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "BATAINDIA.NS",
    "BHARATFORG.NS", "BIOCON.NS", "BOSCHLTD.NS", "BSOFT.NS", "CANBK.NS", "CANFINHOME.NS",
    "CHAMBLFERT.NS", "COFORGE.NS", "CONCOR.NS", "COROMANDEL.NS", "CROMPTON.NS", "CUB.NS",
    "CUMMINSIND.NS", "CYIENT.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DELHIVERY.NS",
    "EXIDEIND.NS", "FEDERALBNK.NS", "FORTIS.NS", "GLENMARK.NS", "GMRINFRA.NS", "GODREJCP.NS",
    "GRANULES.NS", "GUJGASLTD.NS", "GNFC.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HUDCO.NS",
    "IDBI.NS", "IDEA.NS", "IDFC.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", "INDIGO.NS",
    "INDUSTOWER.NS", "IPCALAB.NS", "IRB.NS", "IRCTC.NS", "IRFC.NS", "JKCEMENT.NS",
    "JSWENERGY.NS", "JUBLFOOD.NS", "KALYANKJIL.NS", "LICHSGFIN.NS", "LUPIN.NS", "MANAPPURAM.NS",
    "MRF.NS", "MGL.NS", "MOTHERSON.NS", "MPHASIS.NS", "MRPL.NS", "MUTHOOTFIN.NS",
    "NATIONALUM.NS", "NAVINFLUOR.NS", "NAUKRI.NS", "OBEROIRLTY.NS", "OFSS.NS", "OIL.NS",
    "PAGEIND.NS", "PEL.NS", "PERSISTENT.NS", "PETRONET.NS", "PNB.NS", "PVRINOX.NS",
    "RAMCOCEM.NS", "RBLBANK.NS", "RECLTD.NS", "RVNL.NS", "SHREECEM.NS", "SIEMENS.NS",
    "SRF.NS", "SUPREMEIND.NS", "SUNTV.NS", "SYNGENE.NS", "TATACOMM.NS", "TATACHEM.NS",
    "TATAELXSI.NS", "TATAPOWER.NS", "TATACONSUM.NS", "TORNTPOWER.NS", "TRENT.NS",
    "TRIDENT.NS", "TVSMOTOR.NS", "UBL.NS", "UCOBANK.NS", "UPL.NS", "UNIONBANK.NS", "ZEEL.NS",
    "ZOMATO.NS", "ZYDUSLIFE.NS", "JINDALSTEL.NS", "SJVN.NS", "NHPC.NS", "MAHABANK.NS",
    "CENTRALBK.NS", "IOB.NS", "SUZLON.NS", "IREDA.NS", "GICRE.NS", "NIACL.NS", "LIC.NS", "HINDZINC.NS"
]

SECTOR_MAP = {
    "RELIANCE.NS": "Energy", "ONGC.NS": "Energy", "BPCL.NS": "Energy", "IOC.NS": "Energy", "POWERGRID.NS": "Utilities", "NTPC.NS": "Utilities",
    "TCS.NS": "IT", "INFY.NS": "IT", "WIPRO.NS": "IT", "TECHM.NS": "IT", "HCLTECH.NS": "IT", "LTIM.NS": "IT", "COFORGE.NS": "IT", "PERSISTENT.NS": "IT",
    "HDFCBANK.NS": "Banking", "ICICIBANK.NS": "Banking", "AXISBANK.NS": "Banking", "KOTAKBANK.NS": "Banking", "SBIN.NS": "Banking", "INDUSINDBK.NS": "Banking", "PNB.NS": "Banking", "BANKBARODA.NS": "Banking",
    "BAJFINANCE.NS": "Financial Services", "BAJAJFINSV.NS": "Financial Services", "CHOLAFIN.NS": "Financial Services", "SHRIRAMFIN.NS": "Financial Services", "PFC.NS": "Financial Services", "RECLTD.NS": "Financial Services",
    "MARUTI.NS": "Auto", "TATAMOTORS.NS": "Auto", "M&M.NS": "Auto", "EICHERMOT.NS": "Auto", "HEROMOTOCO.NS": "Auto", "BAJAJ-AUTO.NS": "Auto", "TVSMOTOR.NS": "Auto",
    "TATASTEEL.NS": "Metals", "HINDALCO.NS": "Metals", "JSWSTEEL.NS": "Metals", "SAIL.NS": "Metals", "NMDC.NS": "Metals", "JINDALSTEL.NS": "Metals",
    "SUNPHARMA.NS": "Pharma", "CIPLA.NS": "Pharma", "DRREDDY.NS": "Pharma", "DIVISLAB.NS": "Pharma", "APOLLOHOSP.NS": "Pharma", "ZYDUSLIFE.NS": "Pharma",
    "ITC.NS": "FMCG", "HINDUNILVR.NS": "FMCG", "BRITANNIA.NS": "FMCG", "NESTLEIND.NS": "FMCG", "VBL.NS": "FMCG", "COLPAL.NS": "FMCG", "DABUR.NS": "FMCG"
}

def analyze_market():
    bullish_stocks = []
    bearish_stocks = []
    volume_gainers = []
    sector_performance = {}

    for ticker in WATCHLIST:
        try:
            # Persistent fetching: get 5m data. If market closed, yfinance automatically returns last available session data.
            df = yf.download(ticker, period="5d", interval="5m", progress=False)
            daily_df = yf.download(ticker, period="6d", interval="1d", progress=False)
            
            if df.empty or len(df) < 10 or daily_df.empty or len(daily_df) < 2:
                continue

            # Calculate Historical Daily Vol Average for Volume Gainer feature (last 5 days)
            avg_hist_vol = float(daily_df['Volume'].iloc[-6:-1].mean())
            current_day_vol = float(daily_df['Volume'].iloc[-1])
            vol_multiplier = current_day_vol / avg_hist_vol if avg_hist_vol > 0 else 1.0

            # Last Close of Previous Day
            prev_day_close = float(daily_df['Close'].iloc[-2])

            # Group intraday by day to extract today's timestamps clearly
            df['DateOnly'] = df.index.date
            unique_days = sorted(df['DateOnly'].unique())
            latest_day_df = df[df['DateOnly'] == unique_days[-1]]

            if latest_day_df.empty:
                continue

            first_candle_open = float(latest_day_df['Open'].iloc[0])
            first_candle_high = float(latest_day_df['High'].iloc[0])
            first_candle_low = float(latest_day_df['Low'].iloc[0])
            latest_price = float(latest_day_df['Close'].iloc[-1])
            p_change = ((latest_price - prev_day_close) / prev_day_close) * 100

            # Strict 1.5% Gap and Opening Candle Bracket Filters
            gap_pct = abs((first_candle_open - prev_day_close) / prev_day_close) * 100
            first_candle_high_dev = abs((first_candle_high - prev_day_close) / prev_day_close) * 100
            first_candle_low_dev = abs((first_candle_low - prev_day_close) / prev_day_close) * 100

            if gap_pct > 1.5 or first_candle_high_dev > 1.5 or first_candle_low_dev > 1.5:
                continue  # REJECT stock if it violates the 1.5% shock barrier

            # Calculate 50 EMA and 14 RSI on Full Intraday Array
            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            ema50 = float(df['EMA_50'].iloc[-1])
            
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
            loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            rsi = float(df['RSI'].iloc[-1])

            # Morning Window Slow Grind Filter (09:25 - 10:30)
            latest_day_df.index = pd.to_datetime(latest_day_df.index)
            morning_df = latest_day_df.between_time('09:25', '10:30')
            
            is_slow_grind = True
            if not morning_df.empty and len(morning_df) > 2:
                candle_sizes = (morning_df['High'] - morning_df['Low']).values.flatten()
                atr_morning = np.mean(candle_sizes)
                if np.any(candle_sizes > (atr_morning * 2.8)):
                    is_slow_grind = False

            if is_slow_grind:
                sector = SECTOR_MAP.get(ticker, "Other")
                stock_data = {
                    "Stock Name": ticker.replace(".NS", ""),
                    "Sector": sector,
                    "Live Price": round(latest_price, 2),
                    "Change %": round(p_change, 2),
                    "RSI (14)": round(rsi, 2)
                }

                # Segregate to Bullish or Bearish Tables
                if latest_price > ema50:
                    bullish_stocks.append(stock_data)
                else:
                    bearish_stocks.append(stock_data)

                # Append to Volume Gainer Table if Volume Multiplier > 1.5x
                if vol_multiplier >= 1.5:
                    vol_data = stock_data.copy()
                    vol_data["Volume Multiplier"] = f"{round(vol_multiplier, 2)}x"
                    volume_gainers.append(vol_data)

                if sector not in sector_performance:
                    sector_performance[sector] = []
                sector_performance[sector].append(p_change)

        except Exception:
            continue

    return bullish_stocks, bearish_stocks, volume_gainers, sector_performance

# Run Analytical Engine
with st.spinner("Processing Persistent Structural Matrix & Volume Clouds..."):
    bullish, bearish, vol_gainers, sectors = analyze_market()

# Layout Arrangement
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🟢 UP SIDE MOVES (Slow Accumulation - Above 50 EMA & <1.5% Opening Bracket)")
    if bullish:
        st.dataframe(pd.DataFrame(bullish).sort_values(by="Change %", ascending=False), use_container_width=True)
    else:
        st.info("No stocks fitting the smooth institutional accumulation bracket.")

    st.subheader("🔴 DOWN SIDE MOVES (Slow Distribution - Below 50 EMA & <1.5% Opening Bracket)")
    if bearish:
        st.dataframe(pd.DataFrame(bearish).sort_values(by="Change %", ascending=True), use_container_width=True)
    else:
        st.info("No stocks fitting the smooth institutional distribution bracket.")

    st.subheader("📊 VOLUME GAINERS (High Institutional Volume Activity >= 1.5x Multiplier)")
    if vol_gainers:
        st.dataframe(pd.DataFrame(vol_gainers).sort_values(by="Live Price", ascending=False), use_container_width=True)
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
        st.info("Waiting for data flow loop...")

# Automatic loop sequence refresh
time.sleep(10)
st.rerun()
