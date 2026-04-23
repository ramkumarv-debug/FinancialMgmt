import streamlit as st
import pandas as pd

st.title("💰 Personal Finance Architect")
st.subheader("Let's build your financial statements.")

# --- INPUT SECTION ---
with st.expander("Step 1: Income & Assets (What you have)"):
    income = st.number_input("Monthly Take-home Pay ($)", value=5000)
    savings = st.number_input("Total Savings/401k ($)", value=25000)

with st.expander("Step 2: Expenses & Debts (What you owe)"):
    monthly_out = st.number_input("Monthly Expenses (Rent, Food, etc) ($)", value=3000)
    cc_debt = st.number_input("Total Credit Card/Loan Debt ($)", value=5000)
    annual_subs = st.number_input("Annual/Periodic Expenses (Total for year) ($)", value=1200)

# --- CALCULATIONS ---
monthly_periodic = annual_subs / 12
net_monthly_cash = income - monthly_out - monthly_periodic
net_worth = savings - cc_debt

# --- OUTPUT STATEMENTS ---
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.metric("Monthly Net Cash Flow", f"${net_monthly_cash:,.2f}")
    st.write("**Income Statement (Monthly)**")
    st.write(f"- Revenue: ${income}")
    st.write(f"- Fixed Expenses: -${monthly_out}")
    st.write(f"- Sinking Funds: -${monthly_periodic}")

with col2:
    st.metric("Net Worth", f"${net_worth:,.2f}")
    st.write("**Balance Sheet**")
    st.write(f"- Assets: ${savings}")
    st.write(f"- Liabilities: -${cc_debt}")
