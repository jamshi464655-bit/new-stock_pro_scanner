import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import time
from datetime import datetime

st.set_page_config(page_title="EasyCharts Pro - Nifty 500 Scanner", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 10px 0;
    }
    .category-header {
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        color: white;
        font-weight: bold;
        margin: 15px 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        padding: 15px;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def play_alert():
    audio_html = """
    <audio autoplay>
        <source src="https://www.soundjay.com/buttons/beep-07a.mp3" type="audio/mpeg">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

@st.cache_data(ttl=300)  # 5 minutes cache
def load_stock_symbols():
    """Load Nifty 500 stocks"""
    symbols = [
        # Nifty 50
        "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "HINDUNILVR", "ITC", "SBIN", 
        "BHARTIARTL", "KOTAKBANK", "LT", "AXISBANK", "ASIANPAINT", "MARUTI", "TITAN",
        "SUNPHARMA", "ULTRACEMCO", "BAJFINANCE", "NESTLEIND", "HCLTECH", "WIPRO", "POWERGRID",
        "NTPC", "TATAMOTORS", "BAJAJFINSV", "M&M", "TECHM", "ADANIPORTS", "ONGC", "TATASTEEL",
        "COALINDIA", "HINDALCO", "INDUSINDBK", "JSWSTEEL", "GRASIM", "DIVISLAB", "DRREDDY",
        "CIPLA", "APOLLOHOSP", "BRITANNIA", "EICHERMOT", "HEROMOTOCO", "BAJAJ-AUTO", 
        "TATACONSUM", "SBILIFE", "HDFCLIFE", "ADANIENT", "ADANIGREEN", "TATAPOWER", "PIDILITIND",
        
        # Nifty Next 50
        "ADANIENSOL", "SIEMENS", "HAVELLS", "DLF", "DMART", "INDIGO", "VEDL", "GODREJCP",
        "GAIL", "BOSCHLTD", "CHOLAFIN", "MUTHOOTFIN", "PNB", "CANBK", "RECLTD", "NMDC",
        "ICICIGI", "SRF", "TORNTPHARM", "DABUR", "MARICO", "PEL", "BANKBARODA", "MOTHERSON",
        "SHREECEM", "AMBUJACEM", "TRENT", "INDUSTOWER", "BERGEPAINT", "COLPAL", "LTIM",
        "HINDPETRO", "BPCL", "IOCL", "SAIL", "LUPIN", "BIOCON", "NAUKRI", "ZOMATO", "PAYTM",
        "DIXON", "POLYCAB", "CROMPTON", "VOLTAS", "TVSMOTOR", "ASHOKLEY", "ESCORTS", "MRF",
        "CONCOR", "GMRINFRA",
        
        # Mid Cap 150
        "PERSISTENT", "COFORGE", "LTTS", "MPHASIS", "OFSS", "SBICARD", "ABCAPITAL",
        "AUBANK", "BANDHANBNK", "FEDERALBNK", "IDFCFIRSTB", "IDFC", "IDEA", "JINDALSTEL",
        "TATACHEM", "UPL", "ADANIPOWER", "APLAPOLLO", "ASTRAL", "CUMMINSIND",
        "DEEPAKNTR", "GODREJPROP", "HDFCAMC", "ICICIPRULI", "IRCTC", "JUBLFOOD", "LAURUSLABS",
        "LICI", "MAX", "METROPOLIS", "NYKAA", "OBEROIRLTY", "PAGEIND", "PIIND", "POLICYBZR",
        "SYNGENE", "TATACOMM", "TIINDIA", "UBL", "WHIRLPOOL",
        
        # Small Cap
        "AAVAS", "AEGISCHEM", "AFFLE", "ANGELONE", "APTUS", "ASAHIINDIA", "ATUL",
        "AUROPHARMA", "AXISCADES", "BAJAJCON", "BALRAMCHIN", "BATAINDIA", "BEL", "BHARATFORG",
        "BIRLACORPN", "BSE", "CAMPUS", "CARBORUNIV", "CENTRALBK", "CESC", "CHAMBLFERT", "CLEAN",
        "CRAFTSMAN", "CREDITACC", "CUB", "CYIENT", "DATAPATTNS", "DEEPAKFERT", "DELTACORP",
        "DEVYANI", "DHANUKA", "ELECON", "EMAMILTD",
        
        # Sectoral
        "SONATSOFTW", "MASTEK", "INTELLECT", "KPITTECH", "ZENSAR", "TATAELXSI", "HAPPSTMNDS",
        "RBLBANK", "YESBANK", "UNIONBANK", "INDIANB", "IOB", "MAHABANK", "CDSL", "CAMS",
        "ALKEM", "ABBOTINDIA", "IPCALAB", "LALPATHLAB", "THYROCARE", "GRANULES", "NATCOPHARMA",
        "AJANTPHARM", "GLAXO", "PFIZER", "BALKRISIND", "APOLLOTYRE", "CEAT", "EXIDEIND",
        "PRESTIGE", "BRIGADE", "SOBHA", "IRCON", "RVNL", "NCC", "KNR", "PNC", "GPIL",
        "RADICO", "JYOTHYLAB", "VBL", "CCL", "GILLETTE", "HONASA", "RELAXO", "ABFRL",
        "SHOPERSTOP", "WESTLIFE", "SAPPHIRE", "RAYMOND", "SIYARAM", "ZEEL", "SAREGAMA",
        "NAZARA", "NATIONALUM", "HINDZINC", "RATNAMANI", "APARINDS", "WELSPUNIND", "WELCORP",
        "DALMIACEM", "RAMCOCEM", "JKCEMENT", "HEIDELBERG", "INDIACEM", "ORIENTCEM", "STARCEM",
        "PETRONET", "GUJGASLTD", "IGL", "MGL", "ATGL", "AEGISLOG", "AARTI", "GNFC",
        "NAVINFLUOR", "ALKYLAMINE", "AKZOINDIA", "ABB", "BHEL", "HAL", "GRINDWELL",
        "THERMAX", "TIMKEN", "BLUESTARCO", "SYMPHONY", "ORIENTELEC", "VGUARD", "KEI",
        "ARVIND", "TRIDENT", "INDHOTEL", "LEMONTREE", "CHALET", "EIH", "VRL",
        "MAHLOG", "TCI", "ALLCARGO", "BLUEDART", "CARTRADE", "DELHIVERY", "FINEORG",
        "HBLPOWER", "HERITGFOOD", "HONAUT", "JKPAPER", "KAJARIACER", "KANSAINER", "LINDEINDIA",
        "LUXIND", "METROBRAND", "MFSL", "PNBHOUSING", "POONAWALLA", "PRAJIND", "SIS",
        "SOLARINDS", "SUDARSCHEM", "SUNTV", "SUPREMEIND", "SWANENERGY", "TANLA", "TATAINVEST",
        "TTKPRESTIG", "UTIAMC", "VIPIND", "VINATIORGA", "ZYDUSLIFE"
    ]
    symbols = list(set(symbols))
    return sorted(symbols)

def analyze_all_indicators(symbols, batch_size=100):
    pre_breakout, live_breakout, momentum = [], [], []
    
    symbols = symbols[:batch_size]
    tickers = [f"{s}.NS" for s in symbols]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text(f"📊 Downloading data for {len(tickers)} stocks...")
        data = yf.download(tickers, period="1y", interval="1d", group_by='ticker', progress=False, threads=True)
        
        for idx, s in enumerate(symbols):
            try:
                progress = (idx + 1) / len(symbols)
                progress_bar.progress(progress)
                status_text.text(f"🔍 Analyzing {s} ({idx+1}/{len(symbols)})...")
                
                # Handling single/multi ticker dataframe structure of yfinance
                if len(tickers) == 1:
                    df = data.copy()
                else:
                    if f"{s}.NS" in data.columns.levels[0]:
                        df = data[f"{s}.NS"].copy()
                    else:
                        continue
                
                df = df.dropna()
                if len(df) < 150:
                    continue
                
                # Extracting Series values to avoid MultiIndex Series issues
                close_series = df['Close'].squeeze()
                high_series = df['High'].squeeze()
                low_series = df['Low'].squeeze()
                vol_series = df['Volume'].squeeze()

                ltp = round(float(close_series.iloc[-1]), 2)
                prev_close = round(float(close_series.iloc[-2]), 2)
                change_pct = round(((ltp - prev_close) / prev_close) * 100, 2)
                
                rsi = float(ta.rsi(close_series, length=14).iloc[-1])
                
                ema_200 = float(ta.ema(close_series, length=200).iloc[-1])
                ema_50 = float(ta.ema(close_series, length=50).iloc[-1])
                ema_20 = float(ta.ema(close_series, length=20).iloc[-1])
                
                adx_df = ta.adx(high_series, low_series, close_series)
                adx = float(adx_df['ADX_14'].iloc[-1]) if adx_df is not None else 0
                
                bbands = ta.bbands(close_series, length=20, std=2)
                upper_bb = float(bbands['BBU_20_2.0'].iloc[-1])
                
                vol_ma_20 = float(vol_series.rolling(20).mean().iloc[-1])
                curr_vol = float(vol_series.iloc[-1])
                vol_ratio = round(curr_vol / vol_ma_20, 2) if vol_ma_20 > 0 else 0
                
                macd = ta.macd(close_series)
                macd_line = float(macd['MACD_12_26_9'].iloc[-1]) if macd is not None else 0
                signal_line = float(macd['MACDs_12_26_9'].iloc[-1]) if macd is not None else 0
                
                supertrend = ta.supertrend(high_series, low_series, close_series, length=10, multiplier=3)
                st_trend = int(supertrend['SUPERTd_10_3.0'].iloc[-1]) if supertrend is not None else 0
                
                signal = "🟡 WAIT"
                reason = "Consolidating"
                category = None
                confidence = 0
                
                if (ltp > upper_bb and 
                    curr_vol > vol_ma_20 * 1.5 and 
                    60 < rsi < 85 and 
                    ltp > ema_20 and
                    st_trend == 1):
                    
                    signal = "🟢 STRONG BUY"
                    reason = f"BB Breakout + {vol_ratio}x Volume + RSI {round(rsi, 1)}"
                    category = "live"
                    confidence = min(95, 70 + (vol_ratio * 5))
                
                elif (ema_200 * 0.97 <= ltp <= ema_200 * 1.05 and 
                      45 < rsi < 60 and
                      ltp > ema_50 and
                      vol_ratio > 0.8):
                    
                    signal = "🔵 BUY SETUP"
                    reason = f"Near 200 EMA Support | RSI {round(rsi, 1)}"
                    category = "pre"
                    confidence = 65
                
                elif (ltp > ema_200 and 
                      ltp > ema_50 and 
                      ltp > ema_20 and
                      rsi > 55 and 
                      adx > 25 and
                      macd_line > signal_line):
                    
                    signal = "🔥 MOMENTUM"
                    reason = f"Triple EMA + ADX {round(adx, 1)} + MACD Bull"
                    category = "mom"
                    confidence = 75
                
                stock_res = {
                    "Symbol": s, "Signal": signal, "LTP": ltp, "Change%": f"{change_pct}%",
                    "RSI": round(rsi, 1), "ADX": round(adx, 1), "Vol Ratio": vol_ratio,
                    "Confidence": f"{round(confidence)}%", "Reason": reason
                }
                
                if category == "live":
                    live_breakout.append(stock_res)
                elif category == "pre":
                    pre_breakout.append(stock_res)
                elif category == "mom":
                    momentum.append(stock_res)
                
            except Exception:
                continue
        
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.error(f"Error during analysis: {e}")
    
    return pre_breakout, live_breakout, momentum

st.markdown("""
    <div class='main-header'>
        <h1>📈 EasyCharts Pro - Nifty 500 Scanner</h1>
        <p>AI-Powered Multi-Indicator Stock Scanner (500+ Stocks)</p>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Scanner Settings")
    all_symbols = load_stock_symbols()
    st.info(f"📊 Total Stocks Available: {len(all_symbols)}")
    
    batch_size = st.slider("Stocks to Scan", 50, 500, 100, 50)
    auto_refresh = st.checkbox("🔄 Auto Refresh", value=False)
    refresh_interval = st.selectbox("Refresh Interval (mins)", [1, 2, 5, 10], index=0)
    show_details = st.checkbox("Show Detailed Metrics", value=True)
    
    st.markdown("---")
    st.markdown("### 📊 Signal Legend")
    st.markdown("""
    - 🟢 **STRONG BUY**: Live breakout
    - 🔵 **BUY SETUP**: Pre-breakout
    - 🔥 **MOMENTUM**: Strong trend
    - 🟡 **WAIT**: Consolidating
    """)
    st.markdown("---")
    st.info(f"⏰ Current Time: {datetime.now().strftime('%I:%M:%S %p')}")

if st.button('🚀 START MARKET SCAN', key='scan_button'):
    try:
        symbols = load_stock_symbols()
        if not symbols:
            st.error("❌ No symbols loaded!")
        else:
            st.info(f"📋 Scanning {min(batch_size, len(symbols))} stocks from Nifty 500...")
            with st.spinner('🔍 Scanning markets...'):
                pre, live, mom = analyze_all_indicators(symbols, batch_size)
            
            if live:
                play_alert()
                st.balloons()
                st.success(f"🎯 Found {len(live)} Live Breakouts!")
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.markdown(f"<div class='stat-box'><h2>{len(pre)}</h2><p>Pre-Breakout Setups</p></div>", unsafe_allow_html=True)
            with col_stat2:
                st.markdown(f"<div class='stat-box'><h2>{len(live)}</h2><p>Live Breakouts</p></div>", unsafe_allow_html=True)
            with col_stat3:
                st.markdown(f"<div class='stat-box'><h2>{len(mom)}</h2><p>Momentum Stocks</p></div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<div class='category-header' style='background:#FF9800;'>🔵 Pre-Breakout Setups</div>", unsafe_allow_html=True)
                if pre:
                    df_pre = pd.DataFrame(pre)
                    if not show_details: df_pre = df_pre[['Symbol', 'Signal', 'LTP', 'RSI', 'Confidence']]
                    st.dataframe(df_pre, use_container_width=True, height=400)
                else: st.info("No pre-breakout setups found")
            
            with col2:
                st.markdown("<div class='category-header' style='background:#4CAF50;'>🟢 Live Breakouts</div>", unsafe_allow_html=True)
                if live:
                    df_live = pd.DataFrame(live)
                    if not show_details: df_live = df_live[['Symbol', 'Signal', 'LTP', 'Vol Ratio', 'Confidence']]
                    st.dataframe(df_live, use_container_width=True, height=400)
                else: st.info("No live breakouts found")
            
            with col3:
                st.markdown("<div class='category-header' style='background:#2196F3;'>🔥 Strong Momentum</div>", unsafe_allow_html=True)
                if mom:
                    df_mom = pd.DataFrame(mom)
                    if not show_details: df_mom = df_mom[['Symbol', 'Signal', 'LTP', 'ADX', 'Confidence']]
                    st.dataframe(df_mom, use_container_width=True, height=400)
                else: st.info("No momentum stocks found")
            
            st.markdown("---")
            col_export1, col_export2, col_export3 = st.columns(3)
            if pre:
                with col_export1: st.download_button("📥 Download Pre-Breakout", pd.DataFrame(pre).to_csv(index=False), "pre_breakout.csv", "text/csv")
            if live:
                with col_export2: st.download_button("📥 Download Live Breakout", pd.DataFrame(live).to_csv(index=False), "live_breakout.csv", "text/csv")
            if mom:
                with col_export3: st.download_button("📥 Download Momentum", pd.DataFrame(mom).to_csv(index=False), "momentum.csv", "text/csv")
            
            st.success(f"✅ Scan completed at {time.strftime('%I:%M:%S %p')}")
            
    except Exception as e:
        st.error(f"❌ Error: {e}")

if auto_refresh:
    time.sleep(refresh_interval * 60)
    st.rerun()