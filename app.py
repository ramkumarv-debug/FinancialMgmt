import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finance Architect Pro", layout="wide")

# --- 1. ROBUST INITIALIZATION ---
# We initialize all dataframes in session_state if they don't exist yet.
if 'income_df' not in st.session_state:
    st.session_state.income_df = pd.DataFrame([{"Source": "Primary Job", "Amount": 2500.0, "Frequency": "Bi-Weekly"}])

if 'expense_df' not in st.session_state:
    st.session_state.expense_df = pd.DataFrame([{"Category": "Rent", "Amount": 2000.0, "Frequency": "Monthly"}])

if 'asset_df' not in st.session_state:
    st.session_state.asset_df = pd.DataFrame([{"Asset": "401k", "Value": 15000.0}])

if 'savings_cont_df' not in st.session_state:
    st.session_state.savings_cont_df = pd.DataFrame([{"Goal": "401k Contribution", "Amount": 500.0, "Tax Type": "Pre-Tax (401k/HSA)"}])

if 'debt_df' not in st.session_state:
    st.session_state.debt_df = pd.DataFrame([{"Debt": "Credit Card", "Balance": 2000.0}])

if 'step' not in st.session_state:
    st.session_state.step = 1

# --- 2. HELPER LOGIC ---
def normalize_to_monthly(amt, freq):
    if freq == "Weekly": return (amt * 52) / 12
    if freq == "Bi-Weekly": return (amt * 26) / 12
    if freq == "Monthly": return amt
    if freq == "Quarterly": return amt / 3
    if freq == "Semi-Annual": return amt / 6
    if freq == "Annual" or freq == "One-time": return amt / 12
    return amt

st.title("💰 Financial Architect: Pro Edition")

# Progress Bar
progress_mapping = {1: 0.15, 2: 0.3, 3: 0.45, 4: 0.6, 5: 0.75, 6: 1.0}
st.progress(progress_mapping.get(st.session_state.step, 1.0))

# --- STEP 1: INCOME ---
if st.session_state.step == 1:
    st.header("1. Income Sources")
    st.write("Enter your paychecks, bonuses, or benefits. Tip: Press 'Enter' to save a row.")
    
    inc_freq_options = ["Weekly", "Bi-Weekly", "Monthly", "Quarterly", "Annual"]
    inc_config = {"Frequency": st.column_config.SelectboxColumn("Frequency", options=inc_freq_options, required=True)}
    
    edited_inc = st.data_editor(st.session_state.income_df, column_config=inc_config, num_rows="dynamic", use_container_width=True, key="inc_editor")
    
    if st.button("Next →"):
        st.session_state.income_df = edited_inc
        st.session_state.step = 2
        st.rerun()

# --- STEP 2: EXPENSES ---
elif st.session_state.step == 2:
    st.header("2. Expenses (Monthly & Periodic)")
    st.write("Include recurring bills and periodic costs (Vacations, Insurance).")
    
    exp_freq_options = ["Monthly", "Quarterly", "Semi-Annual", "Annual", "One-time"]
    exp_config = {"Frequency": st.column_config.SelectboxColumn("Frequency", options=exp_freq_options, required=True)}
    
    edited_exp = st.data_editor(st.session_state.expense_df, column_config=exp_config, num_rows="dynamic", use_container_width=True, key="exp_editor")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.expense_df = edited_exp
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next →"):
            st.session_state.expense_df = edited_exp
            st.session_state.step = 3
            st.rerun()

# --- STEP 3: SAVINGS CONTRIBUTIONS ---
elif st.session_state.step == 3:
    st.header("3. Monthly Savings & Investments")
    st.write("How much are you contributing to your wealth each month?")
    
    tax_options = ["Pre-Tax (401k/HSA)", "Post-Tax (Roth/Brokerage)"]
    sav_config = {"Tax Type": st.column_config.SelectboxColumn("Tax Type", options=tax_options, required=True)}
    
    edited_sav = st.data_editor(st.session_state.savings_cont_df, column_config=sav_config, num_rows="dynamic", use_container_width=True, key="sav_editor")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.savings_cont_df = edited_sav
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Next →"):
            st.session_state.savings_cont_df = edited_sav
            st.session_state.step = 4
            st.rerun()

# --- STEP 4: ASSETS ---
elif st.session_state.step == 4:
    st.header("4. Current Asset Balances")
    st.write("Total current value of what you own.")
    
    edited_assets = st.data_editor(st.session_state.asset_df, num_rows="dynamic", use_container_width=True, key="asset_editor")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.asset_df = edited_assets
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("Next →"):
            st.session_state.asset_df = edited_assets
            st.session_state.step = 5
            st.rerun()

# --- STEP 5: DEBTS ---
elif st.session_state.step == 5:
    st.header("5. Debts & Liabilities")
    st.write("What do you currently owe?")
    
    edited_debts = st.data_editor(st.session_state.debt_df, num_rows="dynamic", use_container_width=True, key="debt_editor")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back"):
            st.session_state.debt_df = edited_debts
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("Generate Statements →"):
            st.session_state.debt_df = edited_debts
            st.session_state.step = 6
            st.rerun()

# --- STEP 6: FINAL STATEMENTS ---
elif st.session_state.step == 6:
    st.header("📊 Final Financial Statements")
    
    # CALCULATIONS
    temp_inc = st.session_state.income_df.copy()
    temp_inc['Mo_Equiv'] = temp_inc.apply(lambda x: normalize_to_monthly(x['Amount'], x['Frequency']), axis=1)
    total_mo_income = temp_inc['Mo_Equiv'].sum()
    
    temp_exp = st.session_state.expense_df.copy()
    temp_exp['Mo_Equiv'] = temp_exp.apply(lambda x: normalize_to_monthly(x['Amount'], x['Frequency']), axis=1)
    total_mo_expense = temp_exp['Mo_Equiv'].sum()
    
    pre_tax_sav = st.session_state.savings_cont_df[st.session_state.savings_cont_df["Tax Type"].str.contains("Pre-Tax")]["Amount"].sum()
    post_tax_sav = st.session_state.savings_cont_df[st.session_state.savings_cont_df["Tax Type"].str.contains("Post-Tax")]["Amount"].sum()
    
    total_assets = st.session_state.asset_df["Value"].sum()
    total_debts = st.session_state.debt_df["Balance"].sum()

    # DASHBOARD
    tab1, tab2 = st.tabs(["Income & Cash Flow", "Balance Sheet"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        net_cash = total_mo_income - total_mo_expense - post_tax_sav
        col_a.metric("Monthly Net Cash Flow", f"${net_cash:,.2f}")
        col_b.metric("Total Monthly Savings", f"${pre_tax_sav + post_tax_sav:,.2f}")
        
        st.write("### Monthly Income Statement")
        st.write(f"Normalized Income: **${total_mo_income:,.2f}**")
        st.write(f"Normalized Expenses: **-${total_mo_expense:,.2f}**")
        st.write(f"Post-Tax Savings: **-${post_tax_sav:,.2f}**")
        st.divider()
        st.write(f"**Monthly Surplus/Deficit:** ${net_cash:,.2f}")

    with tab2:
        st.metric("Net Worth", f"${total_assets - total_debts:,.2f}")
        st.write("### Balance Sheet")
        st.write(f"**Total Assets:** ${total_assets:,.2f}")
        st.write(f"**Total Liabilities:** ${total_debts:,.2f}")

    if st.button("Restart"): 
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
