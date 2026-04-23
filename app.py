import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finance Architect Pro", layout="wide")

# Initialize session state with new columns
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.income_df = pd.DataFrame([{"Source": "Salary", "Amount": 5000.0}])
    # Expenses now include Frequency
    st.session_state.expense_df = pd.DataFrame([{"Category": "Rent", "Amount": 2000.0, "Frequency": "Monthly"}])
    # Assets
    st.session_state.asset_df = pd.DataFrame([{"Asset": "401k", "Value": 15000.0}])
    # New: Savings Contributions
    st.session_state.savings_cont_df = pd.DataFrame([{"Goal": "401k Contribution", "Amount": 500.0, "Tax Type": "Pre-Tax"}])
    st.session_state.debt_df = pd.DataFrame([{"Debt": "Credit Card", "Balance": 2000.0}])

st.title("💰 Financial Architect: Pro Edition")

# Progress Bar
progress_mapping = {1: 0.15, 2: 0.3, 3: 0.45, 4: 0.6, 5: 0.75, 6: 1.0}
st.progress(progress_mapping.get(st.session_state.step, 1.0))

# --- STEP 1: INCOME ---
if st.session_state.step == 1:
    st.header("1. Monthly Income")
    st.session_state.income_df = st.data_editor(st.session_state.income_df, num_rows="dynamic", use_container_width=True)
    if st.button("Next →"): st.session_state.step = 2; st.rerun()

# --- STEP 2: PERIODIC EXPENSES ---
elif st.session_state.step == 2:
    st.header("2. Expenses (Monthly & Periodic)")
    st.write("Enter everything from rent (monthly) to car insurance (semi-annual) or vacations (annual).")
    
    # Define frequency options
    freq_options = ["Monthly", "Quarterly", "Semi-Annual", "Annual", "One-time"]
    
    # Configure the table to have a dropdown for frequency
    column_config = {"Frequency": st.column_config.SelectboxColumn("Frequency", options=freq_options, required=True)}
    
    st.session_state.expense_df = st.data_editor(st.session_state.expense_df, column_config=column_config, num_rows="dynamic", use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"): st.session_state.step = 1; st.rerun()
    with col2:
        if st.button("Next →"): st.session_state.step = 3; st.rerun()

# --- STEP 3: SAVINGS CONTRIBUTIONS ---
elif st.session_state.step == 3:
    st.header("3. Monthly Savings & Investments")
    st.write("How much are you adding to your accounts each month?")
    
    tax_options = ["Pre-Tax (401k/HSA)", "Post-Tax (Roth/Brokerage)"]
    column_config = {"Tax Type": st.column_config.SelectboxColumn("Tax Type", options=tax_options, required=True)}
    
    st.session_state.savings_cont_df = st.data_editor(st.session_state.savings_cont_df, column_config=column_config, num_rows="dynamic", use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"): st.session_state.step = 2; st.rerun()
    with col2:
        if st.button("Next →"): st.session_state.step = 4; st.rerun()

# --- STEP 4: ASSETS (TOTAL BALANCES) ---
elif st.session_state.step == 4:
    st.header("4. Current Asset Balances")
    st.write("Total current value of your accounts.")
    st.session_state.asset_df = st.data_editor(st.session_state.asset_df, num_rows="dynamic", use_container_width=True)
    if st.button("Next →"): st.session_state.step = 5; st.rerun()

# --- STEP 5: DEBTS ---
elif st.session_state.step == 5:
    st.header("5. Debts & Liabilities")
    st.session_state.debt_df = st.data_editor(st.session_state.debt_df, num_rows="dynamic", use_container_width=True)
    if st.button("Calculate Final Statements →"): st.session_state.step = 6; st.rerun()

# --- STEP 6: FINAL STATEMENTS ---
elif st.session_state.step == 6:
    st.header("📊 Final Financial Statements")
    
    # --- CALCULATION ENGINE ---
    # 1. Normalize Expenses to Monthly
    def normalize_expense(row):
        amt = row['Amount']
        freq = row['Frequency']
        if freq == "Monthly": return amt
        if freq == "Quarterly": return amt / 3
        if freq == "Semi-Annual": return amt / 6
        if freq == "Annual" or freq == "One-time": return amt / 12
        return amt

    temp_exp = st.session_state.expense_df.copy()
    temp_exp['Monthly_Equiv'] = temp_exp.apply(normalize_expense, axis=1)
    total_mo_expense = temp_exp['Monthly_Equiv'].sum()
    
    # 2. Income & Savings
    total_income = st.session_state.income_df["Amount"].sum()
    post_tax_savings = st.session_state.savings_cont_df[st.session_state.savings_cont_df["Tax Type"] == "Post-Tax (Roth/Brokerage)"]["Amount"].sum()
    
    # 3. Balance Sheet
    total_assets = st.session_state.asset_df["Value"].sum()
    total_debts = st.session_state.debt_df["Balance"].sum()

    # --- DISPLAY ---
    tab1, tab2 = st.tabs(["Income & Cash Flow", "Balance Sheet"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        net_cash = total_income - total_mo_expense - post_tax_savings
        col_a.metric("Monthly Net Cash Flow", f"${net_cash:,.2f}", help="Income - Expenses - PostTax Savings")
        col_b.metric("Monthly Savings Rate", f"{( (total_income - net_cash) / total_income ) * 100:.1f}%")
        
        st.write("### Income Statement")
        st.write(f"Total Monthly Income: **${total_income:,.2f}**")
        st.write(f"Total Monthly Expenses (Normalized): **-${total_mo_expense:,.2f}**")
        st.write(f"Post-Tax Savings Contributions: **-${post_tax_savings:,.2f}**")

    with tab2:
        st.metric("Net Worth", f"${total_assets - total_debts:,.2f}")
        st.write(f"**Total Assets:** ${total_assets:,.2f}")
        st.write(f"**Total Liabilities:** ${total_debts:,.2f}")

    if st.button("Restart"): st.session_state.step = 1; st.rerun()
