import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finance Architect", layout="wide")

# Initialize the "Step" in the interview if it doesn't exist
if 'step' not in st.session_state:
    st.session_state.step = 1

st.title("💰 Personal Finance Interview")

# Progress Bar
progress_mapping = {1: 0.33, 2: 0.66, 3: 1.0}
st.progress(progress_mapping[st.session_state.step])

# --- STEP 1: INCOME ---
if st.session_state.step == 1:
    st.header("Step 1: Where does your money come from?")
    st.write("List all sources of income (e.g., Salary, SSN, Alimony, Rental Income).")
    
    income_data = pd.DataFrame([{"Source": "Main Job", "Monthly Amount": 5000.0}])
    edited_income = st.data_editor(income_data, num_rows="dynamic", use_container_width=True)
    
    if st.button("Next: Expenses →"):
        st.session_state.income_total = edited_income["Monthly Amount"].sum()
        st.session_state.step = 2
        st.rerun()

# --- STEP 2: EXPENSES ---
elif st.session_state.step == 2:
    st.header("Step 2: Where does your money go?")
    st.write("Create your own expense categories (e.g., Rent, Grocery, Car).")
    
    expense_data = pd.DataFrame([{"Category": "Housing", "Monthly Amount": 2000.0}])
    edited_expenses = st.data_editor(expense_data, num_rows="dynamic", use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next: Savings & Investments →"):
            st.session_state.expense_total = edited_expenses["Monthly Amount"].sum()
            st.session_state.step = 3
            st.rerun()

# --- STEP 3: SAVINGS & ASSETS ---
elif st.session_state.step == 3:
    st.header("Step 3: Building Wealth")
    st.write("Where are you putting your money for the future?")
    
    asset_options = ["401K", "Investment Account", "College Fund", "Home Equity", "Savings"]
    asset_data = pd.DataFrame([{"Type": "401K", "Current Balance": 10000.0}])
    
    edited_assets = st.data_editor(asset_data, num_rows="dynamic", use_container_width=True)
    
    if st.button("Finish & View Statements"):
        st.session_state.asset_total = edited_assets["Current Balance"].sum()
        st.session_state.step = 4
        st.rerun()

# --- FINAL VIEW: THE STATEMENTS ---
elif st.session_state.step == 4:
    st.success("Interview Complete!")
    
    # Simple Logic for Statements
    net_cash = st.session_state.income_total - st.session_state.expense_total
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Net Monthly Cash Flow", f"${net_cash:,.2f}")
    with col2:
        st.metric("Total Tracked Assets", f"${st.session_state.asset_total:,.2f}")
    
    if st.button("Restart Interview"):
        st.session_state.step = 1
        st.rerun()
