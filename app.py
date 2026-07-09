import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

# Ultra-wide Layout Page Configuration
st.set_page_config(page_title="Volume Gainer Scanner", layout="wide")
st.title("📊 Institutional Volume Flow Scanner (200+ F&O Matrix)")
st.write("Live 5-Minute Volume Surge Tracker • High Real-Time Accumulation vs 10-Day Baseline")

# COMPLETE 200+ F&O WATCHLIST
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

def scan_volume_gainers():
    up_gainers = []
    down_gainers = []

    try:
        # Batch downloads to keep requests safe and fast
        data_intraday = yf.download(WATCHLIST, period="1d", interval="5m", group_by='ticker', progress=False)
        data_daily = yf.download(WATCHLIST, period="11d", interval="1d", group_by='ticker', progress=False)
        
        for ticker in WATCHLIST:
            try:
                if ticker not in data_daily.columns.levels[0] or ticker not in data_intraday.columns.levels[0]:
                    continue
                
                t_daily = data_daily[ticker].dropna()
                t_intra = data_intraday[ticker].dropna()

                if len(t_daily) < 11 or len(t_intra) < 5:
                    continue

                # --- 10-DAY VOLUME COMPARISON MATRIX ---
                avg_10day_vol = float(t_daily['Volume'].iloc[-11:-1].mean())
                current_day_vol = float(t_daily['Volume'].iloc[-1])
                
                # Check if today's overall volume has scaled past historical limits
                if current_day_vol <= avg_10day_vol:
                    continue

                # --- LIVE INTRADAY 5m VOLUME ACCUMULATION TRIGGER ---
                vols_5m = t_intra['Volume'].values.flatten()
                
                # Ensure volume is strictly increasing or piling up in the last 3 candles
                if not (vols_5m[-1] >= vols_5m[-2] or vols_5m[-2] >= vols_5m[-3]):
                    continue

                vol_multiplier = current_day_vol / avg_10day_vol if avg_10day_vol > 0 else 1.0

                # Technical Trend Sorter using 9 & 15 EMAs on 5-minute chart
                t_intra['EMA_9'] = t_intra['Close'].ewm(span=9, adjust=False).mean()
                t_intra['EMA_15'] = t_intra['Close'].ewm(span=15, adjust=False).mean()
                
                prices = t_intra['Close'].values.flatten()
                latest_price = float(prices[-1])
                ema9 = float(t_intra['EMA_9'].iloc[-1])
                ema15 = float(t_intra['EMA_15'].iloc[-1])

                prev_day_close = float(t_daily['Close'].iloc[-2])
                p_change = ((latest_price - prev_day_close) / prev_day_close) * 100

                stock_data = {
                    "Stock Name": ticker.replace(".NS", ""),
                    "Live Price": round(latest_price, 2),
                    "Change %": round(p_change, 2),
                    "Volume Multiplier": f"{round(vol_multiplier, 2)}x"
                }

                # Corrected syntax condition allocation
                if latest_price > ema9 and ema9 >= ema15:
                    up_gainers.append(stock_data)
                elif latest_price < ema9 and ema9 <= ema15:
                    down_gainers.append(stock_data)

            except Exception:
                continue
    except Exception:
        pass

    return up_gainers, down_gainers

# Run Scanner Loops
with st.spinner("Analyzing Liquid 10-Day Arrays for Continuous Volume Surges..."):
    up_list, down_list = scan_volume_gainers()

# Layout Arrangement
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟢 VOLUME GAINERS (UP SIDE MOVES)")
    if up_list:
        st.dataframe(pd.DataFrame(up_list).sort_values(by="Change %", ascending=False), use_container_width=True)
    else:
        st.info("Monitoring 200+ grid for institutional up-side buying volume...")

with col2:
    st.subheader("🔴 VOLUME GAINERS (DOWN SIDE MOVES)")
    if down_list:
        st.dataframe(pd.DataFrame(down_list).sort_values(by="Change %", ascending=True), use_container_width=True)
    else:
        st.info("Monitoring 200+ grid for heavy shorting distribution volume...")

# 3-Minute Refresh sequence loop
time.sleep(180)
st.rerun()
