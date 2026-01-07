import streamlit as st
import requests
from datetime import datetime, timedelta
import uuid
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Pre-DICKTOR", page_icon="🍆", layout="wide")

# High-tech neon dark theme (same as before)
st.markdown("""
<style>
    .stApp {
        background: #000000;
        color: #e0ffe0;
    }
    .big-title {
        font-size: 5.5rem !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #39ff14, #ff00ff, #00ffff, #39ff14);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: neon-pulse 3s ease-in-out infinite alternate;
        text-shadow: 0 0 20px #39ff14;
    }
    @keyframes neon-pulse {
        from { text-shadow: 0 0 10px #39ff14, 0 0 20px #39ff14; }
        to { text-shadow: 0 0 20px #ff00ff, 0 0 40px #ff00ff; }
    }
    .subtitle {
        font-size: 2.2rem;
        text-align: center;
        color: #ff00ff;
        text-shadow: 0 0 15px #ff00ff;
    }
    .stButton > button {
        background: linear-gradient(45deg, #001a00, #1a0033);
        color: #39ff14;
        border: 2px solid #39ff14;
        border-radius: 15px;
        padding: 15px 30px;
        font-size: 1.3rem;
        font-weight: bold;
        box-shadow: 0 0 25px rgba(57, 255, 20, 0.6);
    }
    .stButton > button:hover {
        box-shadow: 0 0 40px rgba(255, 0, 255, 0.8);
        transform: translateY(-3px);
    }
    .market-card {
        background: rgba(10, 10, 30, 0.8);
        border: 3px solid #ff00ff;
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.5);
    }
    .share-btn {
        background: linear-gradient(45deg, #ff00ff, #8000ff);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 50px;
        font-weight: bold;
        box-shadow: 0 0 25px #ff00ff;
    }
    .dedu-card {
        background: rgba(20, 0, 40, 0.7);
        border: 4px solid #39ff14;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 40px rgba(57, 255, 20, 0.4);
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Disclaimer
if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

if not st.session_state.disclaimer_accepted:
    st.markdown("""
    <div style='background:rgba(20,0,40,0.8);padding:50px;border-radius:20px;border:4px dashed #39ff14;text-align:center;box-shadow:0 0 40px rgba(57,255,20,0.4);max-width:800px;margin:auto'>
        <h1 style='color:#ff00ff'>🔴 ACCESS RESTRICTED 🔴</h1>
        <h2 style='color:#39ff14'>PRE-DICKTOR v2.0 ONLINE</h2>
        <p style='font-size:1.6rem;color:#b0ffb0'>
            NOT financial advice. Extreme volatility zone.<br>
            You may lose all funds instantly.<br>
            Only risk what you can afford to lose.
        </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("EXIT", type="secondary", use_container_width=True):
            st.stop()
    with col2:
        if st.button("ENTER MATRIX – I ACCEPT RISKS", type="primary", use_container_width=True):
            st.session_state.disclaimer_accepted = True
            st.balloons()
            st.rerun()
    st.stop()

# Title
st.markdown('<h1 class="big-title">Pre-DICKTOR</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Meme Prediction Matrix | Powered by $DEDU 🍆</p>', unsafe_allow_html=True)

# Wallet Connect
if 'wallet' not in st.session_state:
    st.session_state.wallet = None

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🔗 CONNECT PHANTOM WALLET", use_container_width=True):
        st.markdown("""
        <script src="https://unpkg.com/@solana/web3.js@latest/lib/index.iife.min.js"></script>
        <script>
        async function connect() {
            if (window.solana && window.solana.isPhantom) {
                try {
                    const resp = await window.solana.connect();
                    window.parent.location = window.parent.location.href.split('?')[0] + '?wallet=' + resp.publicKey.toString();
                } catch (err) {
                    alert("Connection failed");
                }
            } else {
                alert("Install Phantom wallet!");
            }
        }
        connect();
        </script>
        """, unsafe_allow_html=True)

if st.session_state.wallet:
    st.success(f"🟢 CONNECTED: {st.session_state.wallet}")

# Live Prices
st.markdown("<h2 style='text-align:center;color:#ff00ff'>📊 LIVE FEED</h2>", unsafe_allow_html=True)
try:
    prices = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin&vs_currencies=usd").json()
    cols = st.columns(4)
    cols[0].metric("BTC", f"${prices.get('bitcoin',{}).get('usd','N/A'):,}")
    cols[1].metric("ETH", f"${prices.get('ethereum',{}).get('usd','N/A'):,}")
    cols[2].metric("SOL", f"${prices.get('solana',{}).get('usd','N/A'):,}")
    cols[3].metric("BNB", f"${prices.get('binancecoin',{}).get('usd','N/A'):,}")
except:
    st.error("Feed offline")

# $DEDU Token Hub
st.markdown("<div class='dedu-card'>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#39ff14'>💜 $DEDU TOKEN HUB</h2>", unsafe_allow_html=True)
st.markdown("<p style='font-size:1.5rem;color:#ff00ff'>Contract: <code>AqDGzh4jRZipMrkBuekDXDB1Py2huA8G5xCvrSgmpump</code></p>", unsafe_allow_html=True)

# $DEDU Price Chart (fixed length)
dedu_data = pd.DataFrame({
    'Date': pd.date_range(start='2026-01-01', periods=15).strftime('%Y-%m-%d'),
    'Price (USD)': [0.0000048, 0.0000050, 0.0000051, 0.0000052, 0.0000051, 0.0000053, 0.0000054, 0.0000053, 0.0000053, 0.0000053, 0.0000053, 0.0000053, 0.0000053, 0.0000053, 0.0000053],
    'Holders': [20, 22, 25, 27, 29, 31, 32, 33, 34, 35, 35, 35, 35, 35, 35]
})
fig_dedu = px.line(dedu_data, x='Date', y=['Price (USD)', 'Holders'],
                   color_discrete_map={'Price (USD)': '#ff00ff', 'Holders': '#39ff14'})
fig_dedu.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#e0ffe0')
st.plotly_chart(fig_dedu, use_container_width=True)

st.markdown("<p style='font-size:1.6rem;color:#39ff14'>Buy $DEDU now to play Pre-DICKTOR and catch the next leg up! 🚀</p>", unsafe_allow_html=True)

# Swap Widget
st.markdown("<h3 style='color:#ff00ff'>SWAP SOL → $DEDU</h3>", unsafe_allow_html=True)
st.markdown(f"""
<jupiter-widget
  input-mint="So11111111111111111111111111111111111111112"
  output-mint="AqDGzh4jRZipMrkBuekDXDB1Py2huA8G5xCvrSgmpump"
  amount="500000000">
</jupiter-widget>
<script type="module" src="https://unpkg.com/@jup-ag/widget-embedded@latest"></script>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Markets
if 'markets' not in st.session_state:
    st.session_state.markets = []

# Fixed chart data function — same length
def get_market_chart_data():
    num_days = 30
    dates = pd.date_range(end=datetime.today(), periods=num_days).strftime('%Y-%m-%d').tolist()
    yes = list(range(10, 10 + 17 * num_days, 17))[:num_days]  # 30 points
    no = list(range(5, 5 + 13 * num_days, 13))[:num_days]    # 30 points
    return pd.DataFrame({'Date': dates, 'YES Bets': yes, 'NO Bets': no})

# Admin sidebar
with st.sidebar:
    st.markdown("### 🔐 ADMIN")
    pwd = st.text_input("Password", type="password")
    if pwd == "deduction":
        st.success("Access granted")
        with st.form("create_market"):
            question = st.text_input("Question", "Will $BONK 10x in 2026?")
            memecoin = st.text_input("CoinGecko ID", "bonk")
            target = st.number_input("Target Price (USD)", 0.0000001)
            date = st.date_input("Resolution Date")
            submitted = st.form_submit_button("🚀 LAUNCH MARKET")
            if submitted:
                new_market = {
                    "id": str(uuid.uuid4()),
                    "question": question,
                    "memecoin_id": memecoin,
                    "target_price": target,
                    "resolution_date": str(date),
                    "yes_pool": 20000.0,
                    "no_pool": 20000.0,
                    "constant": 400000000.0,
                    "resolved": False
                }
                st.session_state.markets.append(new_market)
                st.success("Market launched!")
                st.balloons()

# Display markets
st.markdown("<h2 style='text-align:center;color:#ff00ff'>🧠 ACTIVE MARKETS</h2>", unsafe_allow_html=True)

if not st.session_state.markets:
    st.info("No active markets yet. Admin, launch one!")
else:
    for market in st.session_state.markets:
        with st.container():
            st.markdown("<div class='market-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;color:#00ffff'>{market['question']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;color:#ff00ff'>Resolves: {market['resolution_date']}</p>", unsafe_allow_html=True)

            # Fixed market chart
            chart_df = get_market_chart_data()
            st.line_chart(chart_df.set_index('Date'), use_container_width=True)

            yes_price = market['no_pool'] / (market['yes_pool'] + market['no_pool'])
            no_price = 1 - yes_price

            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"<h2 style='color:#39ff14;text-align:center'>YES<br>${yes_price:.5f}</h2>", unsafe_allow_html=True)
                if st.button("🟢 LONG", key=f"yes_{market['id']}", use_container_width=True):
                    if st.session_state.wallet:
                        st.success("LONG position opened 📈")
                    else:
                        st.warning("Connect wallet first")
            with col2:
                st.markdown(f"<h2 style='color:#ff0066;text-align:center'>NO<br>${no_price:.5f}</h2>", unsafe_allow_html=True)
                if st.button("🔴 SHORT", key=f"no_{market['id']}", use_container_width=True):
                    if st.session_state.wallet:
                        st.success("SHORT position opened 🩸")
                    else:
                        st.warning("Connect wallet first")
            with col3:
                share_text = f"Pre-DICKTOR Prediction: {market['question']} | YES ${yes_price:.5f} vs NO ${no_price:.5f} 🍆"
                share_url = "https://pre-dicktor.streamlit.app"  # Update after deploy
                twitter_url = f"https://twitter.com/intent/tweet?text={requests.utils.quote(share_text)}&url={requests.utils.quote(share_url)}"
                st.markdown(f'<a href="{twitter_url}" target="_blank"><button class="share-btn">📤 SHARE</button></a>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align:center;margin-top:60px;padding:40px;background:rgba(0,10,30,0.6);border:2px solid #39ff14;border-radius:20px'>
    <h2 style='color:#ff00ff'>Pre-DICKTOR v2.0</h2>
    <p style='color:#39ff14'>$DEDU Powered | Built for Degens | WAGMI 🍆</p>
</div>
""", unsafe_allow_html=True)
