import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finance Architect", layout="wide")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.income_df = pd.DataFrame([{"Source": "Salary", "Amount": 5000.0}])
    st.session_state.expense_df = pd.DataFrame([{"Category": "Rent", "Amount": 2000.0}])
    st.session_state.asset_df = pd.DataFrame([{"Asset": "401k", "Value": 15000.0}])
    st.session_state.debt_df = pd.DataFrame([{"Debt": "Credit Card", "Balance": 2000.0}])

st.title("💰 Personal Finance Interview")

# Progress Bar (Now handles 5 steps to avoid that KeyError!)
progress_mapping = {1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1.0}
st.progress(progress_mapping.get(st.session_state.step, 1.0))

# --- STEP 1: INCOME ---
if st.session_state.step == 1:
    st.header("Step 1: Income Sources")
    st.write("Add your take-home pay, SSN, alimony, etc.")
    st.session_state.income_df = st.data_editor(st.session_state.income_df, num_rows="dynamic", use_container_width=True)
    if st.button("Next: Expenses →"):
        st.session_state.step = 2
        st.rerun()

# --- STEP 2: EXPENSES ---
elif st.session_state.step == 2:
    st.header("Step 2: Monthly Expenses")
    st.write("List your monthly outflows (Rent, Groceries, Utilities).")
    st.session_state.expense_df = st.data_editor(st.session_state.expense_df, num_rows="dynamic", use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"): st.session_state.step = 1; st.rerun()
    with col2:
        if st.button("Next: Assets →"): st.session_state.step = 3; st.rerun()

# --- STEP 3: ASSETS ---
elif st.session_state.step == 3:
    st.header("Step 3: Assets & Wealth")
    st.write("What do you own? (401k, Home Equity, Savings, etc.)")
    st.session_state.asset_df = st.data_editor(st.session_state.asset_df, num_rows="dynamic", use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"): st.session_state.step = 2; st.rerun()
    with col2:
        if st.button("Next: Debts →"): st.session_state.step = 4; st.rerun()

# --- STEP 4: DEBTS ---
elif st.session_state.step == 4:
    st.header("Step 4: Debts & Liabilities")
    st.write("What do you owe? (Credit Cards, Personal Loans, Mortgages).")
    st.session_state.debt_df = st.data_editor(st.session_state.debt_df, num_rows="dynamic", use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"): st.session_state.step = 3; st.rerun()
    with col2:
        if st.button("Generate Statements →"): st.session_state.step = 5; st.rerun()

# --- STEP 5: FINAL STATEMENTS ---
elif st.session_state.step == 5:
    st.header("📊 Your Financial Statements")
    
    # Calculate Totals
    total_income = st.session_state.income_df["Amount"].sum()
    total_expense = st.session_state.expense_df["Amount"].sum()
    total_assets = st.session_state.asset_df["Value"].sum()
    total_debts = st.session_state.debt_df["Balance"].sum()
    
    # Dashboard Tabs
    tab1, tab2, tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])
    
    with tab1:
        st.subheader("Monthly Income Statement")
        st.write(f"**Total Income:** ${total_income:,.2f}")
        st.write(f"**Total Expenses:** -${total_expense:,.2f}")
        st.divider()
        st.metric("Net Income (Profit/Loss)", f"${total_income - total_expense:,.2f}")

    with tab2:
        st.subheader("Personal Balance Sheet")
        st.write(f"**Total Assets:** ${total_assets:,.2f}")
        st.write(f"**Total Liabilities:** -${total_debts:,.2f}")
        st.divider()
        st.metric("Net Worth", f"${total_assets - total_debts:,.2f}")

    with tab3:
        st.subheader("Monthly Cash Flow")
        st.write("This shows how much 'dry powder' you have left each month.")
        st.metric("Disposable Cash", f"${total_income - total_expense:,.2f}")

    if st.button("Restart Interview"):
        st.session_state.step = 1
        st.rerun()
