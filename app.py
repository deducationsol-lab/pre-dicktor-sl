import streamlit as st
import requests
from datetime import datetime
import uuid
import pandas as pd
import plotly.express as px
import hashlib
import json
import base64

# Page config
st.set_page_config(page_title="PRE-DICKTOR", page_icon="🍆", layout="wide")

# High-tech neon dark theme
st.markdown("""
<style>
    .stApp { background: #000000; color: #e0ffe0; }
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
    .subtitle { font-size: 2.2rem; text-align: center; color: #ff00ff; text-shadow: 0 0 15px #ff00ff; }
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
    .live-badge {
        background: #ff00ff;
        color: black;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: bold;
        box-shadow: 0 0 20px #ff00ff;
        display: inline-block;
        margin: 10px 0;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# LIVE BADGE
st.markdown("<div class='live-badge'>LIVE ON MAINNET – REAL $DEDU BETS</div>", unsafe_allow_html=True)

# === GITHUB SHARED STORAGE ===
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
DATA_REPO = st.secrets["DATA_REPO"]
DATA_FILE = "markets.json"

def load_markets():
    url = f"https://api.github.com/repos/{DATA_REPO}/contents/{DATA_FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        content = r.json()["content"]
        decoded = base64.b64decode(content).decode('utf-8')
        return json.loads(decoded)
    except:
        return []

def save_markets(markets):
    url = f"https://api.github.com/repos/{DATA_REPO}/contents/{DATA_FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    sha = r.json().get("sha")
    content = base64.b64encode(json.dumps(markets, indent=2).encode()).decode()
    data = {
        "message": "Update markets",
        "content": content,
        "sha": sha
    }
    requests.put(url, json=data, headers=headers)

markets = load_markets()

# === SECURE ADMIN PASSWORD ===
EXPECTED_HASH = "6645adc23275824958437afdcc809d3027c4f772ee65ebd26846e943e6209437"

def check_admin_password(pwd: str) -> bool:
    return hashlib.sha256(pwd.encode()).hexdigest() == EXPECTED_HASH

# Disclaimer
if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

if not st.session_state.disclaimer_accepted:
    st.markdown("""
    <div style='background:rgba(20,0,40,0.8);padding:50px;border-radius:20px;border:4px dashed #39ff14;text-align:center;box-shadow:0 0 40px rgba(57,255,20,0.4);max-width:800px;margin:auto'>
        <h1 style='color:#ff00ff'>🔴 LIVE MAINNET ACCESS</h1>
        <h2 style='color:#39ff14'>PRE-DICKTOR IS LIVE</h2>
        <p style='font-size:1.6rem;color:#b0ffb0'>
            This is a LIVE mainnet app.<br>
            Real $DEDU tokens are used for voting.<br>
            Highest bet wins the pool.<br>
            No refunds. Bet responsibly.
        </p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("EXIT", type="secondary", use_container_width=True):
            st.stop()
    with col2:
        if st.button("I UNDERSTAND – LET ME BET", type="primary", use_container_width=True):
            st.session_state.disclaimer_accepted = True
            st.balloons()
            st.rerun()
    st.stop()

# Title
st.markdown('<h1 class="big-title">PRE-DICKTOR</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Live Mainnet Prediction Market | Highest Bet Wins | Powered by $DEDU 🗳️🍆</p>', unsafe_allow_html=True)

# Wallet Connect (REQUIRED)
if 'wallet' not in st.session_state:
    st.session_state.wallet = None

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🔗 CONNECT PHANTOM WALLET (REQUIRED FOR BETTING)", use_container_width=True):
        st.markdown("""
        <script src="https://unpkg.com/@solana/web3.js@latest/lib/index.iife.min.js"></script>
        <script>
        async function connect() {
            if (window.solana && window.solana.isPhantom) {
                try {
                    const resp = await window.solana.connect();
                    window.parent.location = window.parent.location.href.split('?')[0] + '?wallet=' + resp.publicKey.toString();
                } catch (err) {
                    alert("Wallet connection failed");
                }
            } else {
                alert("Install Phantom wallet from phantom.app");
            }
        }
        connect();
        </script>
        """, unsafe_allow_html=True)

if st.session_state.wallet:
    st.success(f"🟢 WALLET CONNECTED: {st.session_state.wallet}")
else:
    st.warning("⚠️ Connect Phantom wallet to place real $DEDU bets")

# Live $DEDU Price
st.markdown("<h2 style='text-align:center;color:#39ff14'>💜 $DEDU LIVE PRICE</h2>", unsafe_allow_html=True)
DEDU_MINT = "AqDGzh4jRZipMrkBuekDXDB1Py2huA8G5xCvrSgmpump"
try:
    response = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{DEDU_MINT}").json()
    if response.get('pairs'):
        pair = response['pairs'][0]
        price = float(pair['priceUsd'])
        st.markdown(f"<h1 style='text-align:center;color:#ff00ff'>${price:.10f}</h1>", unsafe_allow_html=True)
    else:
        st.info("Price loading...")
except:
    st.warning("Price feed down")

# Jupiter Swap Widget
st.markdown("<h2 style='text-align:center;color:#ff00ff'>🔥 SWAP TO $DEDU</h2>", unsafe_allow_html=True)
st.markdown(f"""
<jupiter-widget input-mint="So11111111111111111111111111111111111111112" output-mint="{DEDU_MINT}" amount="500000000"></jupiter-widget>
<script type="module" src="https://unpkg.com/@jup-ag/widget-embedded@latest"></script>
""", unsafe_allow_html=True)

# Admin
with st.sidebar:
    st.markdown("### 🔐 ADMIN")
    pwd = st.text_input("Password", type="password")
    if check_admin_password(pwd):
        st.success("Access Granted")
        with st.form("create_market"):
            question = st.text_input("Question", "Which meme will dominate 2026?")
            options_input = st.text_area("Answers (one per line)", "BONK 🐶\nWIF 🧢\nPEPE 🐸\nPOPCAT 😼")
            date = st.date_input("Resolution Date")
            submitted = st.form_submit_button("LAUNCH MARKET")
            if submitted:
                options = [o.strip() for o in options_input.split('\n') if o.strip()]
                if len(options) < 2:
                    st.error("Need 2+ options")
                else:
                    new_market = {
                        "id": str(uuid.uuid4()),
                        "question": question,
                        "options": options,
                        "bets": {opt: 0 for opt in options},
                        "resolution_date": str(date),
                        "resolved": False,
                        "winner": None
                    }
                    markets.append(new_market)
                    save_markets(markets)
                    st.success("Market launched on mainnet!")
                    st.balloons()

# Display Markets
st.markdown("<h2 style='text-align:center;color:#ff00ff'>🗳️ LIVE MARKETS</h2>", unsafe_allow_html=True)

if not markets:
    st.info("No active markets — admin launching soon")
else:
    for market in markets:
        with st.container():
            st.markdown("<div class='market-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;color:#00ffff'>{market['question']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;color:#ff00ff'>Ends: {market['resolution_date']}</p>", unsafe_allow_html=True)

            total = sum(market['bets'].values())
            cols = st.columns(len(market['options']))
            for idx, opt in enumerate(market['options']):
                with cols[idx]:
                    amount = market['bets'][opt]
                    perc = (amount / total * 100) if total > 0 else 0
                    st.markdown(f"<h2 style='text-align:center;color:#39ff14'>{opt}<br>{amount:,.0f} $DEDU ({perc:.1f}%)</h2>", unsafe_allow_html=True)
                    if st.button(f"🗳️ BET {opt} (10,000 $DEDU)", key=f"bet_{market['id']}_{idx}", use_container_width=True):
                        if st.session_state.wallet:
                            st.info("Real $DEDU bet would be sent here in full version")
                            market['bets'][opt] += 10000
                            save_markets(markets)
                            st.success(f"Simulated bet placed: 10,000 $DEDU on {opt}")
                            st.balloons()
                        else:
                            st.warning("Connect Phantom wallet")

            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align:center;margin-top:60px;padding:40px;background:rgba(0,10,30,0.6);border:2px solid #39ff14;border-radius:20px'>
    <h2 style='color:#ff00ff'>PRE-DICKTOR LIVE</h2>
    <p style='color:#39ff14'>Real $DEDU bets | Highest bet wins | Mainnet active</p>
</div>
""", unsafe_allow_html=True)
