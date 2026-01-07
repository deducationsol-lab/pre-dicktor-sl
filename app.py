import streamlit as st
import requests
import json
from datetime import datetime
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page config
st.set_page_config(page_title="MemeMarket", page_icon="🚀", layout="centered")

# Disclaimer (shown once)
if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

if not st.session_state.disclaimer_accepted:
    st.markdown("""
    <div style="background:#000;padding:30px;border-radius:16px;border:2px solid #0f0;text-align:center;max-width:600px;margin:auto">
        <h2 style="color:#ff4444">⚠️ RISK DISCLAIMER</h2>
        <p><strong>This is NOT financial advice.</strong></p>
        <p>MemeMarket is a high-risk prediction platform for memecoins using <strong>$DEDU</strong>.</p>
        <p><strong>You can lose 100% of your investment.</strong> Only use money you can afford to lose completely.</p>
        <p>By continuing, you confirm you fully understand the risks of trading volatile crypto assets.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("I Do Not Accept", type="secondary"):
            st.error("You cannot use MemeMarket without accepting the risks.")
            st.stop()
    with col2:
        if st.button("I Understand & Accept the Risks", type="primary"):
            st.session_state.disclaimer_accepted = True
            st.rerun()
    st.stop()

# Initialize markets in session state
if 'markets' not in st.session_state:
    st.session_state.markets = []

DEDU_MINT = "AqDGzh4jRZipMrkBuekDXDB1Py2huA8G5xCvrSgmpump"

# Header
st.title("🚀 MemeMarket")
st.markdown("**The $DEDU-Powered Memecoin Prediction Platform**")

# Wallet Connect (Phantom)
if 'wallet' not in st.session_state:
    st.session_state.wallet = None

if st.button("Connect Phantom Wallet"):
    st.markdown("""
    <script src="https://unpkg.com/@solana/web3.js@latest/lib/index.iife.min.js"></script>
    <script>
    async function connect() {
        if (window.solana && window.solana.isPhantom) {
            try {
                const resp = await window.solana.connect();
                window.location.href = window.location.href + "?wallet=" + resp.publicKey.toString();
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

# Get wallet from URL
import urllib.parse
params = urllib.parse.parse_qs(urllib.parse.urlparse(st.experimental_get_query_params().get("request_uri", [""])[0]).query)
if "wallet" in params:
    st.session_state.wallet = params["wallet"][0][:8] + "..." + params["wallet"][0][-4:]
    st.success(f"Wallet connected: {st.session_state.wallet}")

# Live Prices
st.subheader("Live Crypto Prices (USD)")
try:
    prices = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin&vs_currencies=usd").json()
    cols = st.columns(4)
    cols[0].metric("Bitcoin", f"${prices.get('bitcoin', {}).get('usd', 'N/A')}")
    cols[1].metric("Ethereum", f"${prices.get('ethereum', {}).get('usd', 'N/A')}")
    cols[2].metric("Solana", f"${prices.get('solana', {}).get('usd', 'N/A')}")
    cols[3].metric("BNB", f"${prices.get('binancecoin', {}).get('usd', 'N/A')}")
except:
    st.error("Price fetch failed")

# Swap to $DEDU
st.subheader("Get $DEDU to Trade")
st.markdown("Swap SOL directly to $DEDU using Jupiter:")
st.markdown(f"""
<jupiter-widget
  input-mint="So11111111111111111111111111111111111111112"
  output-mint="{DEDU_MINT}"
  amount="100000000">
</jupiter-widget>
<script type="module" src="https://unpkg.com/@jup-ag/widget-embedded@latest"></script>
""", unsafe_allow_html=True)

# Admin Panel (simple - use your email)
if st.sidebar.checkbox("Admin Mode"):
    if st.sidebar.text_input("Admin Email") == "deducation.sol@gmail.com":
        st.sidebar.success("Admin access granted")
        
        st.subheader("Create New Market")
        with st.form("create_market"):
            question = st.text_input("Question", "Will $PEPE reach $0.0001 by end of month?")
            memecoin = st.text_input("CoinGecko ID", "pepe")
            target = st.number_input("Target Price (USD)", 0.000001)
            date = st.date_input("Resolution Date")
            submitted = st.form_submit_button("Create Market")
            
            if submitted:
                market = {
                    "id": str(uuid.uuid4()),
                    "question": question,
                    "memecoin_id": memecoin,
                    "target_price": target,
                    "resolution_date": str(date),
                    "yes_pool": 10000.0,
                    "no_pool": 10000.0,
                    "constant": 100000000.0,
                    "resolved": False
                }
                st.session_state.markets.append(market)
                st.success("Market created!")

# Markets Display & Trading
st.subheader("Active Prediction Markets")
for market in st.session_state.markets:
    with st.expander(f"📈 {market['question']} | Ends: {market['resolution_date']}"):
        yes_price = market['no_pool'] / (market['yes_pool'] + market['no_pool'])
        no_price = 1 - yes_price
        
        col1, col2 = st.columns(2)
        col1.metric("YES Price", f"${yes_price:.4f}")
        col2.metric("NO Price", f"${no_price:.4f}")
        
        col3, col4 = st.columns(2)
        if col3.button("Buy YES (100 $DEDU)", key=f"yes_{market['id']}"):
            if st.session_state.wallet:
                st.success("Simulated: Bought 100 $DEDU on YES")
            else:
                st.warning("Connect wallet first!")
        if col4.button("Buy NO (100 $DEDU)", key=f"no_{market['id']}"):
            if st.session_state.wallet:
                st.success("Simulated: Bought 100 $DEDU on NO")
            else:
                st.warning("Connect wallet first!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Deduction | Powered by $DEDU")
