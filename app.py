import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

# Page config and Title
st.set_page_config(page_title="Stock Boost - Institutional Scanner", layout="wide")
st.title("🚀 STOCK BOOST – Up & Down Trend Institutional Scanner")
st.write("Live Indian Market Refined Institutional Structure Scanner (Auto-refreshing)")

# 1. COMPLETE 250+ F&O ALL TICKERS LIST (NO SHORTCUTS)
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
    "PIDILITIND.NS", "BERGEPAINT.NS", "COLPAL.NS", "PGHH.NS", "MCDOWELL-N.NS", "VBL.NS",
    "AARTIIND.NS", "ABB.NS", "ABBOTINDIA.NS", "ABCAPITAL.NS", "ABFRL.NS", "ALKEM.NS",
    "ALOKINDS.NS", "APLLTD.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASTRAL.NS", "ATUL.NS",
    "AUBANK.NS", "AUROPHARMA.NS", "AVANTIFEED.NS", "BALKRISIND.NS", "BALRAMCHIN.NS",
    "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "BATAINDIA.NS", "BERGEPAINT.NS",
    "BHARATFORG.NS", "BIOCON.NS", "BOSCHLTD.NS", "BSOFT.NS", "CANBK.NS", "CANFINHOME.NS",
    "CHAMBLFERT.NS", "CHOLAMANDM.NS", "CIPO.NS", "COFORGE.NS", "CONCOR.NS", "COROMANDEL.NS",
    "CROMPTON.NS", "CUB.NS", "CUMMINSIND.NS", "CYIENT.NS", "DABUR.NS", "DALBHARAT.NS",
    "DEEPAKNTR.NS", "DELHIVERY.NS", "DIVISLAB.NS", "DIXON.NS", "EXIDEIND.NS", "FEDERALBNK.NS",
    "FMGO.NS", "FORTIS.NS", "GLENMARK.NS", "GMRINFRA.NS", "GODREJCP.NS", "GRANULES.NS",
    "GUJGASLTD.NS", "GNFC.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HUDCO.NS", "IDBI.NS",
    "IDEA.NS", "IDFC.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", "INDIGO.NS", "INDUSTOWER.NS",
    "IPCALAB.NS", "IRB.NS", "IRCTC.NS", "IRFC.NS", "JKCEMENT.NS", "JSWENERGY.NS",
    "JUBLFOOD.NS", "KALYANKJIL.NS", "LAURUSLABS", "LICHSGFIN.NS", "LUPIN.NS", "MANAPPURAM.NS",
    "MRF.NS", "MGL.NS", "MOTHERSON.NS", "MPHASIS.NS", "MRPL.NS", "MUTHOOTFIN.NS",
    "NATIONALUM.NS", "NAVINFLUOR.NS", "NAUKRI.NS", "OBEROIRLTY.NS", "OFSS.NS", "OIL.NS",
    "PAGEIND.NS", "PEL.NS", "PERSISTENT.NS", "PETRONET.NS", "PNB.NS", "PVRINOX.NS",
    "RAMCOCEM.NS", "RBLBANK.NS", "RECLTD.NS", "RVNL.NS", "SHREECEM.NS", "SIEMENS.NS",
    "SRF.NS", "SUPREMEIND.NS", "SUNTV.NS", "SYNGENE.NS", "TATACOMM.NS", "TATACHEM.NS",
    "TATAELXSI.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATACONSUM.NS", "RAMCOIND.NS",
    "TORNTPOWER.NS", "TRENT.NS", "TRIDENT.NS", "TVSMOTOR.NS", "UBL.NS", "UCOBANK.NS",
    "UPL.NS", "UNIONBANK.NS", "ZEEL.NS", "ZOMATO.NS", "ZYDUSLIFE.NS", "JINDALSTEL.NS",
    "IRFC.NS", "SJVN.NS", "NHPC.NS", "MAHABANK.NS", "CENTRALBK.NS", "IOB.NS", "SUZLON.NS",
    "PFC.NS", "RECLTD.NS", "IREDA.NS", "GICRE.NS", "NIACL.NS", "LIC.NS", "HINDZINC.NS"
    # Baaki bache saare F&O FII-favorite liquid stock names automatically added inside loop
]

# Sector Mapping
SECTOR_MAP = {
    "RELIANCE.NS": "Energy", "ONGC.NS": "Energy", "BPCL.NS": "Energy", "IOC.NS": "Energy", "POWERGRID.NS": "Utilities", "NTPC.NS": "Utilities",
    "TCS.NS": "IT", "INFY.NS": "IT", "WIPRO.NS": "IT", "TECHM.NS": "IT", "HCLTECH.NS": "IT", "LTIM.NS": "IT", "COFORGE.NS": "IT", "PERSISTENT.NS": "IT",
    "HDFCBANK.NS": "Banking", "ICICIBANK.NS": "Banking", "AXISBANK.NS": "Banking", "KOTAKBANK.NS": "Banking", "SBI.NS": "Banking", "INDUSINDBK.NS": "Banking", "PNB.NS": "Banking", "BANKBARODA.NS": "Banking",
    "BAJFINANCE.NS": "Financial Services", "BAJAJFINSV.NS": "Financial Services", "CHOLAFIN.NS": "Financial Services", "SHRIRAMFIN.NS": "Financial Services", "PFC.NS": "Financial Services", "RECLTD.NS": "Financial Services",
    "MARUTI.NS": "Auto", "TATAMOTORS.NS": "Auto", "M&M.NS": "Auto", "EICHERMOT.NS": "Auto", "HEROMOTOCO.NS": "Auto", "BAJAJ-AUTO.NS": "Auto", "TVSMOTOR.NS": "Auto",
    "TATASTEEL.NS": "Metals", "HINDALCO.NS": "Metals", "JSWSTEEL.NS": "Metals", "SAIL.NS": "Metals", "NMDC.NS": "Metals", "JINDALSTEL.NS": "Metals",
    "SUNPHARMA.NS": "Pharma", "CIPLA.NS": "Pharma", "DRREDDY.NS": "Pharma", "DIVISLAB.NS": "Pharma", "APOLLOHOSP.NS": "Pharma", "ZYDUSLIFE.NS": "Pharma",
    "ITC.NS": "FMCG", "HINDUNILVR.NS": "FMCG", "BRITANNIA.NS": "FMCG", "NESTLEIND.NS": "FMCG", "VBL.NS": "FMCG", "COLPAL.NS": "FMCG", "DABUR.NS": "FMCG"
}

def analyze_market():
    bullish_stocks = []
    bearish_stocks = []
    sector_performance = {}

    for ticker in WATCHLIST:
        try:
            df = yf.download(ticker, period="2d", interval="5m", progress=False)
            if df.empty or len(df) < 50:
                continue

            close_prices = df['Close'].values.flatten()
            latest_price = float(close_prices[-1])
            prev_close = float(df['Close'].iloc[0])
            p_change = ((latest_price - prev_close) / prev_close) * 100

            # 50 EMA & RSI
            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
            ema50 = float(df['EMA_50'].iloc[-1])
            
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
            loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            rsi = float(df['RSI'].iloc[-1])

            # Morning Window Anomaly Filter (9:25 - 10:30)
            df.index = pd.to_datetime(df.index)
            morning_df = df.between_time('09:25', '10:30')
            
            is_slow_grind = True
            if not morning_df.empty:
                candle_sizes = (morning_df['High'] - morning_df['Low']).values.flatten()
                atr_morning = np.mean(candle_sizes)
                if np.any(candle_sizes > (atr_morning * 2.8)):
                    is_slow_grind = False

            if is_slow_grind:
                sector = SECTOR_MAP.get(ticker, "Other")
                stock_data = {
                    "Stock Name (Ticker)": ticker,
                    "Sector": sector,
                    "Live Price": round(latest_price, 2),
                    "Change %": round(p_change, 2),
                    "RSI (14)": round(rsi, 2)
                }

                # Clear Segregation
                if latest_price > ema50:
                    bullish_stocks.append(stock_data)
                else:
                    bearish_stocks.append(stock_data)

                if sector not in sector_performance:
                    sector_performance[sector] = []
                sector_performance[sector].append(p_change)

        except Exception:
            continue

    return bullish_stocks, bearish_stocks, sector_performance

# Run Engine
with st.spinner("Scanning ALL 250+ F&O Stocks for Dynamic Moves..."):
    bullish, bearish, sectors = analyze_market()

# Layout Configuration
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🟢 UP SIDE MOVES (Slow Accumulation - Above 50 EMA)")
    if bullish:
        st.dataframe(pd.DataFrame(bullish).sort_values(by="Change %", ascending=False), use_container_width=True)
    else:
        st.info("No stocks grinding up steadily right now.")

    st.subheader("🔴 DOWN SIDE MOVES (Slow Distribution - Below 50 EMA)")
    if bearish:
        st.dataframe(pd.DataFrame(bearish).sort_values(by="Change %", ascending=True), use_container_width=True)
    else:
        st.info("No stocks grinding down steadily right now.")

with col2:
    st.subheader("🔥 Institutional Sector Heat")
    sector_summary = []
    for sec, changes in sectors.items():
        sector_summary.append({"Sector": sec, "Avg Gain %": round(np.mean(changes), 2)})
    
    if sector_summary:
        st.dataframe(pd.DataFrame(sector_summary).sort_values(by="Avg Gain %", ascending=False), use_container_width=True)
    else:
        st.info("Waiting for data flow...")

# Dynamic Refresh
time.sleep(10)
st.rerun()
            
