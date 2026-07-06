import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

# Page config and Title
st.set_page_config(page_title="Stock Boost - Institutional Scanner", layout="wide")
st.title("🚀 STOCK BOOST – Advanced Institutional Flow & Volume Scanner")
st.write("Live Market Smooth Structure & Volume Analytics (All 200+ F&O Stocks Active)")

# COMPLETE 200+ F&O WATCHLIST (NO FILTERS BEFORE SCAN)
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
    "RELIANCE.NS": "Energy", "ONGC.NS": "Energy", "BPCL.NS": "Energy", "IOC.NS": "Energy", "POWERGRID.NS": "Utilities", "NTPC.NS": "Utilities",
    "TCS.NS": "IT", "INFY.NS": "IT", "WIPRO.NS": "IT", "TECHM.NS": "IT", "HCLTECH.NS": "IT", "LTIM.NS": "IT", "COFORGE.NS": "IT", "PERSISTENT.NS": "IT",
    "HDFCBANK.NS": "Banking", "ICICIBANK.NS": "Banking", "AXISBANK.NS": "Banking", "KOTAKBANK.NS": "Banking", "SBIN.NS": "Banking", "INDUSINDBK.NS": "Banking", "PNB.NS": "Banking", "BANKBARODA.NS": "Banking",
    "BAJFINANCE.NS": "Financial Services", "BAJAJFINSV.NS": "Financial Services", "CHOLAFIN.NS": "Financial Services", "SHRIRAMFIN.NS": "Financial Services", "PFC.NS": "Financial Services", "RECLTD.NS": "Financial Services",
    "MARUTI.NS": "Auto", "TATAMOTORS.NS": "Auto", "M&M.NS": "Auto", "EICHERMOT.NS": "Auto", "HEROMOTOCO.NS": "Auto", "BAJAJ-AUTO.NS": "Auto", "TVSMOTOR.NS": "Auto",
    "TATASTEEL.NS": "Metals", "HINDALCO.NS": "Metals", "JSWSTEEL.NS": "Metals", "SAIL.NS": "Metals", "NMDC.NS": "Metals", "JINDALSTEL.NS": "Metals",
    "SUNPHARMA.NS": "Pharma", "CIPLA.NS": "Pharma", "DRREDDY.NS": "Pharma", "DIVISLAB.NS": "Pharma", "APOLLOHOSP.NS": "Pharma", "ZYDUSLIFE.NS": "Pharma",
    "ITC.NS": "FMCG", "HINDUNILVR.NS": "FMCG", "BRITANNIA.NS": "FMCG", "NESTLEIND.NS": "FMCG", "VBL.NS": "FMCG", "COLPAL.NS": "FMCG", "DABUR.NS": "FMCG"
}

def analyze_market_batch():
    bullish_stocks = []
    bearish_stocks = []
    volume_gainers = []
    sector_performance = {}

    try:
        # High Speed Batch Fetching
        data_intraday = yf.download(WATCHLIST, period="2d", interval="15m", group_by='ticker', progress=False)
        data_daily = yf.download(WATCHLIST, period="6d", interval="1d", group_by='ticker', progress=False)
        
        for ticker in WATCHLIST:
            try:
                if ticker not in data_daily.columns.levels[0] or ticker not in data_intraday.columns.levels[0]:
                    continue
                
                t_daily = data_daily[ticker].dropna()
                t_intra = data_intraday[ticker].dropna()

                if len(t_daily) < 2 or len(t_intra) < 3:
                    continue

                prev_day_close = float(t_daily['Close'].iloc[-2])
                avg_hist_vol = float(t_daily['Volume'].iloc[-5:-1].mean())
                current_day_vol = float(t_daily['Volume'].iloc[-1])
                vol_multiplier = current_day_vol / avg_hist_vol if avg_hist_vol > 0 else 1.0

                latest_price = float(t_intra['Close'].iloc[-1])
                p_change = ((latest_price - prev_day_close) / prev_day_close) * 100

                # 50 EMA & RSI Calculations
                t_intra['EMA_50'] = t_intra['Close'].ewm(span=50, adjust=False).mean()
                ema50 = float(t_intra['EMA_50'].iloc[-1])

                delta = t_intra['Close'].diff()
                gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
                loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs.iloc[-1])) if not np.isnan(rs.iloc[-1]) else 50.0

                # Morning Window Anomaly Filter (09:25 - 10:30) - Controlled Size Check
                t_intra.index = pd.to_datetime(t_intra.index)
                morning_df = t_intra.between_time('09:25', '10:30')
                
                is_slow_grind = True
                if not morning_df.empty and len(morning_df) > 1:
                    candle_sizes = (morning_df['High'] - morning_df['Low']).values.flatten()
                    atr_morning = np.mean(candle_sizes)
                    if np.any(candle_sizes > (atr_morning * 3.5)):
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

                    # Trend Alignment (Above vs Below 50 EMA)
                    if latest_price > ema50:
                        bullish_stocks.append(stock_data)
                    else:
                        bearish_stocks.append(stock_data)

                    # Volume Surge Accumulation Filter
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

# Fire Engine
with st.spinner("Connecting to High-Speed Institutional 200+ Streams..."):
    bullish, bearish, vol_gainers, sectors = analyze_market_batch()

# Layout Build
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🟢 UP SIDE MOVES (Slow Accumulation - Above 50 EMA)")
    if bullish:
        st.dataframe(pd.DataFrame(bullish).sort_values(by="Change %", ascending=False), use_container_width=True)
    else:
        st.info("Scanning smooth institutional accumulation brackets...")

    st.subheader("🔴 DOWN SIDE MOVES (Slow Distribution - Below 50 EMA)")
    if bearish:
        st.dataframe(pd.DataFrame(bearish).sort_values(by="Change %", ascending=True), use_container_width=True)
    else:
        st.info("Scanning smooth institutional distribution brackets...")

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

# Loop Sync
time.sleep(15)
st.rerun()
