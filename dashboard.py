import datetime
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="LAIOS Framework - AI OS", page_icon="⚡", layout="wide"
)

# Simulated Live Data (Replace with SQLite / Webhook Data later)
if "quotes_df" not in st.session_state:
    st.session_state.quotes_df = pd.DataFrame(
        {
            "Quote ID": ["Q-1001", "Q-1002", "Q-1003", "Q-1004", "Q-1005"],
            "Client": [
                "Homeowner A",
                "Contractor B",
                "Homeowner C",
                "Construction D",
                "Homeowner E",
            ],
            "Material": [
                "Aggregate G1",
                "Crusher Dust",
                "Sand",
                "19mm Stone",
                "G2 Base",
            ],
            "Tons": [12.5, 30.0, 8.0, 45.0, 15.0],
            "Status": ["Pending", "Approved", "Completed", "Approved", "Pending"],
            "Date": [
                "2026-08-14",
                "2026-08-14",
                "2026-08-14",
                "2026-08-13",
                "2026-08-13",
            ],
        }
    )

if "inventory_df" not in st.session_state:
    st.session_state.inventory_df = pd.DataFrame(
        {
            "Material": [
                "Crusher Dust",
                "Aggregate G1",
                "Aggregate G2",
                "19mm Stone",
                "Building Sand",
            ],
            "Stock Level (Tons)": [1250, 840, 620, 950, 410],
            "Status": [
                "Optimal",
                "Optimal",
                "Low Stock",
                "Optimal",
                "Critical",
            ],
        }
    )

if "fleet_df" not in st.session_state:
    st.session_state.fleet_df = pd.DataFrame(
        {
            "Vehicle ID": ["TRK-01", "TRK-02", "TRK-03"],
            "Driver": ["Sipho M.", "Johan V.", "David K."],
            "Status": ["In Transit", "Loading at Quarry", "Available"],
            "Current Delivery": [
                "Q-1002 (Contractor B)",
                "Q-1004 (Construction D)",
                "None",
            ],
        }
    )

# Sidebar Navigation as an AI OS Shell
st.sidebar.title("⚡ LAIOS Framework")
st.sidebar.caption("Layered AI Operating System v1.0")
menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Operations Overview",
        "Quotation Engine",
        "Inventory & Stock",
        "Logistics & Fleet",
        "System Logs",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("System Telemetry")
st.sidebar.metric("WhatsApp Bot", "Active 🟢", "100% Uptime")
st.sidebar.metric("SQLite DB", "Connected 🟢", "Latency: 12ms")

# --- 1. OPERATIONS OVERVIEW ---
if menu == "Operations Overview":
    st.title("LAIOS - Executive Operations Overview")
    st.write(
        "Real-time unified command center for automated quotes, quarry stock, and logistics."
    )

    col1, col2, col3, col4 = st.columns(4)
    df_quotes = st.session_state.quotes_df
    col1.metric(
        "Total Quotes Today",
        len(df_quotes),
        delta="+3 from yesterday",
    )
    col2.metric(
        "Active Deliveries",
        len(
            st.session_state.fleet_df[
                st.session_state.fleet_df["Status"] != "Available"
            ]
        ),
    )
    col3.metric(
        "Pending Approvals",
        len(df_quotes[df_quotes["Status"] == "Pending"]),
    )
    col4.metric("System Status", "Online", delta="Stable")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Live Quote Status Breakdown")
        status_counts = df_quotes["Status"].value_counts()
        st.bar_chart(status_counts)

    with col_right:
        st.subheader("Material Demand Volume (Tons)")
        material_tons = df_quotes.groupby("Material")["Tons"].sum()
        st.bar_chart(material_tons)

# --- 2. QUOTATION ENGINE ---
elif menu == "Quotation Engine":
    st.title("AI Quotation & Inquiries")
    st.write(
        "Incoming automated quotation requests captured via WhatsApp and web channels."
    )

    if st.button("Refresh Quote Stream"):
        st.rerun()

    st.dataframe(st.session_state.quotes_df, use_container_width=True)

    st.subheader("Simulate Incoming Quote (Webhook Test)")
    with st.form("test_quote_form"):
        new_client = st.text_input("Client Name", "Contractor Test")
        new_material = st.selectbox(
            "Material",
            ["Aggregate G1", "Crusher Dust", "Sand", "19mm Stone", "G2 Base"],
        )
        new_tons = st.number_input("Tons Required", min_value=1.0, value=10.0)
        submitted = st.form_submit_button("Trigger Webhook Quote")
        if submitted:
            new_row = {
                "Quote ID": f"Q-100{len(st.session_state.quotes_df) + 1}",
                "Client": new_client,
                "Material": new_material,
                "Tons": new_tons,
                "Status": "Pending",
                "Date": str(datetime.date.today()),
            }
            st.session_state.quotes_df = pd.concat(
                [pd.DataFrame([new_row]), st.session_state.quotes_df],
                ignore_index=True,
            )
            st.success("New quote successfully processed by LAIOS engine!")
            st.rerun()

# --- 3. INVENTORY & STOCK ---
elif menu == "Inventory & Stock":
    st.title("Quarry & Material Inventory")
    st.write(
        "Monitor stock thresholds, aggregate pile levels, and replenishment alerts."
    )
    st.dataframe(st.session_state.inventory_df, use_container_width=True)

    st.warning("⚠️ Building Sand inventory is running low (Critical threshold).")

# --- 4. LOGISTICS & FLEET ---
elif menu == "Logistics & Fleet":
    st.title("Logistics & Fleet Dispatch")
    st.write("Live tracking of delivery vehicles, drivers, and active routes.")
    st.dataframe(st.session_state.fleet_df, use_container_width=True)

# --- 5. SYSTEM LOGS ---
elif menu == "System Logs":
    st.title("LAIOS Kernel & Audit Logs")
    st.write("Internal system activity, API call traces, and webhook events.")
    st.code(
        """[INFO] 2026-08-14 21:15:02 - LAIOS Core initialized successfully.
[INFO] 2026-08-14 21:16:40 - WhatsApp Webhook received payload from +27821234567.
[INFO] 2026-08-14 21:16:41 - Generated dynamic quote Q-1001 for Homeowner A.
[INFO] 2026-08-14 21:18:22 - SQLite log committed successfully to local store.
[DEBUG] 2026-08-14 21:20:05 - Streamlit UI heartbeat check: OK.""",
        language="text",
    )
