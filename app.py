import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Finlords Investor Portal", layout="wide")

st.title("📊 Finlords Investor Portal (Simulation)")
st.caption("NSE Equity Strategy • Read-only Investor View")

# ---------------- DATA ----------------
investors = pd.DataFrame({
    "Investor": ["Alice", "Bob", "Carol"],
    "Capital": [500000, 300000, 200000],
    "Bank Cash": [25000, 10000, 10000],
    "MMF": [25000, 10000, 10000]
})

holdings = pd.DataFrame({
    "Stock": ["SCBK", "EQTY", "COOP", "BAT", "KEGN", "SBIC"],
    "Shares": [1000, 800, 700, 600, 500, 400],
    "Avg Buy Price": [150, 175, 185, 210, 250, 300],
    "Current Price": [160, 180, 190, 220, 260, 315]
})

holdings["Market Value"] = holdings["Shares"] * holdings["Current Price"]
holdings["Unrealized G/L"] = (
    holdings["Current Price"] - holdings["Avg Buy Price"]
) * holdings["Shares"]

# ---------------- SIDEBAR ----------------
st.sidebar.header("Investor View")
selected_investor = st.sidebar.selectbox(
    "Select Investor",
    investors["Investor"]
)

investor = investors[investors["Investor"] == selected_investor].iloc[0]

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Portfolio Value (KES)", f"{holdings['Market Value'].sum():,.0f}")
col2.metric("Unrealized P/L (KES)", f"{holdings['Unrealized G/L'].sum():,.0f}")
col3.metric("Bank Cash (KES)", f"{investor['Bank Cash']:,.0f}")
col4.metric("MMF (KES)", f"{investor['MMF']:,.0f}")

st.divider()

# ---------------- HOLDINGS ----------------
st.subheader("📈 NSE Equity Holdings")

holdings["Return %"] = (
    (holdings["Current Price"] / holdings["Avg Buy Price"] - 1) * 100
).round(2)

st.dataframe(
    holdings[[
        "Stock", "Shares", "Avg Buy Price",
        "Current Price", "Market Value",
        "Unrealized G/L", "Return %"
    ]],
    use_container_width=True
)

# ---------------- PROFIT LOCK ----------------
st.subheader("⚡ Tactical Profit Lock")

threshold = st.slider("Profit-lock trigger (%)", 5, 50, 20)

holdings["Signal"] = np.where(
    holdings["Return %"] >= threshold,
    "SELL / LOCK PROFIT",
    "HOLD"
)

st.dataframe(
    holdings[["Stock", "Return %", "Signal"]],
    use_container_width=True
)

# ---------------- SIMULATED SELL ----------------
st.subheader("💰 Simulate Profit Taking")

stock = st.selectbox("Select stock", holdings["Stock"])
sell_pct = st.slider("Sell % of position", 10, 100, 50, 10)

if st.button("Execute Simulated Sale"):
    row = holdings[holdings["Stock"] == stock].iloc[0]
    shares_sold = int(row["Shares"] * sell_pct / 100)
    value = shares_sold * row["Current Price"]

    st.success(
        f"Sold {shares_sold} shares of {stock} "
        f"for KES {value:,.0f}. "
        "Funds transferred to bank."
    )

# ---------------- CASH POLICY ----------------
st.subheader("🏦 Liquidity Policy")
st.info(
    "• Minimum 15% held in cash/MMF\n"
    "• Short-term profits parked in bank\n"
    "• Reinvested during rebalancing cycles"
)

st.caption("© Finlords Limited • Simulation Environment")
