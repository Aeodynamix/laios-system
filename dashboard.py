import streamlit as st
import pandas as pd
import sqlite3
import datetime

st.set_page_config(page_title="LAIOS Management Dashboard", layout="wide")

st.title("LAIOS Framework - Operations Dashboard")
st.markdown("Real-time visibility into automated quotations, logistics, and data logs.")

# Database connection placeholder
# conn = sqlite3.connect('laios.db')

# Dummy data for demonstration / initial setup
data = {
    "Quote ID": ["Q-1001", "Q-1002", "Q-1003"],
    "Client": ["Homeowner A", "Contractor B", "Homeowner C"],
    "Material": ["Aggregate G1", "Crusher Dust", "Sand"],
    "Status": ["Pending", "Approved", "Completed"],
    "Date": [datetime.date.today(), datetime.date.today(), datetime.date.today()]
}
df = pd.DataFrame(data)

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Quotes", len(df))
col2.metric("Active Deliveries", 2)
col3.metric("System Status", "Online")

st.subheader("Recent Quotations")
st.dataframe(df, use_container_width=True)

if st.button("Refresh Data"):
    st.rerun()
