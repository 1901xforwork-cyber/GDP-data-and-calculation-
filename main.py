import streamlit as st
import pandas as pd
import plotly.express as px

# Load your dataset directly (instead of uploading)
data = pd.read_csv("2020-2025.csv")

# Set page configuration
st.set_page_config(
    page_title="GDP per Country 2020–2025 Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title of the dashboard
st.title("📊 GDP per Country 2020–2025")

# Username check from session state
if 'username' in st.session_state:
    st.write(f"👋 Welcome {st.session_state['username']}!")
else:
    st.info("ℹ️ Please set your name in Setting page")

# Display basic dataset information
st.header("📝 Dataset Overview")
col1, col2, col3 = st.columns(3)

# Metrics
with col1:
    st.metric(
        label="Total Rows",
        value=len(data),
        delta=f"{len(data.columns)} columns"
    )

with col2:
    if 'sales' in data.columns:
        total_sales = data['sales'].sum()
        avg_sales = data['sales'].mean()
        st.metric(
            label="Total Sales",
            value=f"${total_sales:,.2f}",
            delta=f"Avg: ${avg_sales:,.2f}"
        )

with col3:
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        st.metric(
            label="Numeric Columns",
            value=len(numeric_cols),
            delta=f"{len(data.columns) - len(numeric_cols)} non-numeric"
        )

# Charts Section
st.header("📈 Data Visualization")

# Select columns for visualization
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns

# Chart Type Selector
chart_type = st.selectbox(
    "Select Chart Type",
    ["Line Chart", "Bar Chart", "Scatter Plot", "Box Plot"]
)

# Column Selectors
col1, col2 = st.columns(2)
with col1:
    x_axis = st.selectbox("Select X-axis", data.columns)
with col2:
    y_axis = st.selectbox("Select Y-axis", numeric_columns)

# Create different types of charts based on selection
if chart_type == "Line Chart":
    fig = px.line(data, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Bar Chart":
    fig = px.bar(data, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Scatter Plot":
    fig = px.scatter(data, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Box Plot":
    fig = px.box(data, x=x_axis, y=y_axis, title=f"Distribution of {y_axis} by {x_axis}")
    st.plotly_chart(fig, use_container_width=True)

# Data Table Section
st.header("📋 Data Table")

# Add search functionality
search_term = st.text_input("Search in data:")

if search_term:
    # Search through all columns
    mask = data.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
    filtered_data = data[mask]
else:
    filtered_data = data

# Show number of rows per page selector
rows_per_page = st.selectbox("Rows per page:", [10, 25, 50, 100])

# Display the table with pagination
start_idx = st.number_input("Page", min_value=1, value=1) - 1
start_idx = start_idx * rows_per_page
end_idx = start_idx + rows_per_page

st.dataframe(
    filtered_data.iloc[start_idx:end_idx],
    use_container_width=True
)

# Display total number of records
st.info(f"Showing {len(filtered_data)} records {' (filtered)' if search_term else ''}")

# Add download button
st.download_button(
    label="Download data as CSV",
    data=filtered_data.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv",
)
