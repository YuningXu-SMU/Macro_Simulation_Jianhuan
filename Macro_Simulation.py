import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("Macroeconomics Simulation")

st.sidebar.header("Global Economic Parameters")

st.sidebar.subheader("Demand Side (IS Curve)")
r_star = st.sidebar.slider("Natural Real Interest Rate (r*)", 0.0, 5.0, 2.0)
sigma_x = st.sidebar.slider("IS Curve Shock Volatility (Std Dev)", 0.0, 3.0, 1.0)

st.sidebar.subheader("Supply Side (Phillips Curve)")
b_param = st.sidebar.slider("Output Gap Sensitivity (b)", 0.05, 1.0, 0.25)
sigma_u = st.sidebar.slider("Phillips Curve Shock Volatility (Std Dev)", 0.0, 3.0, 1.0)

st.sidebar.subheader("Central Bank Preferences")
pi_bar = st.sidebar.slider("Inflation Target (pi_bar)", 0.0, 5.0, 2.5)
kappa = st.sidebar.slider("Output Gap Weight (kappa)", 0.0, 1.0, 0.1)

# 1. Pull data from Google Sheets
sheet_url_L = "https://docs.google.com/spreadsheets/d/1bpNT6HZsvexo5s8WDxVqgw0x7IymI8s-soCx4liuCS0/export?format=csv&gid=1717631077"
sheet_url_R = "https://docs.google.com/spreadsheets/d/1bpNT6HZsvexo5s8WDxVqgw0x7IymI8s-soCx4liuCS0/export?format=csv&gid=709519525"

# Loading data
df_L = pd.read_csv(sheet_url_L)
df_R = pd.read_csv(sheet_url_R)
avg_expected_inflation_L = df_L.iloc[:, 1].mean()
avg_expected_inflation_R = df_R.iloc[:, 1].mean()

st.subheader(f"Average Expected Inflation of Group L: {avg_expected_inflation_L:.2f}%")
st.subheader(f"Average Expected Inflation of Group R: {avg_expected_inflation_R:.2f}%")

# 2. Input Section with Subheader Styling
col_in1, col_in2 = st.columns(2)
with col_in1:
    st.subheader("Central Bank L Rate (%)")
    r_L = st.number_input("CB_L_Input", label_visibility="collapsed", value=2.0, key="L")
with col_in2:
    st.subheader("Central Bank R Rate (%)")
    r_R = st.number_input("CB_R_Input", label_visibility="collapsed", value=2.0, key="R")

# 3. The "Gate" - Only show results when this button is clicked
if st.button("Run Simulation and Calculate Results"):
    
    # Random shocks (generated only when button is clicked)
    x = np.random.normal(0, sigma_x)
    u = np.random.normal(0, sigma_u)
    
    # Calculations
    output_gap_L = -(r_L - r_star) + x
    pi_L = avg_expected_inflation_L + b_param * output_gap_L + u
    
    output_gap_R = -(r_R - r_star) + x
    pi_R = avg_expected_inflation_R + b_param * output_gap_R + u

    utility_private_L = 10 - (pi_L - avg_expected_inflation_L)**2
    utility_private_R = 10 - (pi_R - avg_expected_inflation_R)**2
    utility_CB_L = 20 - (pi_L - pi_bar)**2
    utility_CB_R = 20 - (pi_R - pi_bar)**2 - kappa * output_gap_R**2

    # 4. Output Display
    st.divider() # Visual line to separate inputs from results
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Group L Results")
        st.subheader(f"Output Gap: {output_gap_L:.2f}")
        st.subheader(f"Inflation: {pi_L:.2f}%")
        st.subheader(f"Utility (Private): {utility_private_L:.2f}")
        st.subheader(f"Utility (Central Bank): {utility_CB_L:.2f}")

    with col2:
        st.header("Group R Results")
        st.subheader(f"Output Gap: {output_gap_R:.2f}")
        st.subheader(f"Inflation: {pi_R:.2f}%")
        st.subheader(f"Utility (Private): {utility_private_R:.2f}")
        st.subheader(f"Utility (Central Bank): {utility_CB_R:.2f}")
else:
    st.info("Waiting for Central Bank interest rates. Click the button above to see results.")

