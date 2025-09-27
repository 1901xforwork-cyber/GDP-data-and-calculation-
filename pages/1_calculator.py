import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("📈 GDP Calculator")

# Sidebar inputs
st.sidebar.header("Input Components")

consumption = st.sidebar.number_input("Consumption (C)", min_value=0.0, value=1000.0, step=100.0)
investment = st.sidebar.number_input("Investment (I)", min_value=0.0, value=500.0, step=100.0)
government = st.sidebar.number_input("Government Spending (G)", min_value=0.0, value=800.0, step=100.0)
export_value = st.sidebar.number_input("Exports (X)", min_value=0.0, value=600.0, step=100.0)
import_value = st.sidebar.number_input("Imports (M)", min_value=0.0, value=400.0, step=100.0)

# GDP calculation
net_export = export_value - import_value
gdp = consumption + investment + government + net_export

# Display results
st.subheader("📊 GDP Result")
st.write(f"**GDP:** {gdp:,.2f}")

# Data for visualization
data = {
    "Component": ["Consumption", "Investment", "Government", "Net Export"],
    "Value": [consumption, investment, government, net_export]
}
df = pd.DataFrame(data)

# Plot GDP composition
fig = px.pie(df, names="Component", values="Value", title="GDP Composition", hole=0.4)
st.plotly_chart(fig)

# Show dataframe table
st.subheader("📋 GDP Breakdown")
st.dataframe(df)
