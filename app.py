import streamlit as st  # type: ignore
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Sri Lanka Revenue Dashboard", layout="centered")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("CW2_dataset_cleaned.xls")  # <- notice it's read_csv
    df = df.dropna(how='all')  # Remove fully empty rows
    df = df.dropna(axis=1, how='all')  # Remove fully empty columns
    return df



df = load_data()

# Melt the data to long format
df_long = df.melt(id_vars=["Category"], var_name="Year", value_name="Revenue")
df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
df_long['Revenue'] = pd.to_numeric(df_long['Revenue'], errors='coerce')
df_long.dropna(subset=["Year", "Revenue"], inplace=True)

# --- Sidebar ---
# Sidebar
st.sidebar.title("🔧 Controls")
years = df_long['Year'].astype(int)
year_min, year_max = years.min(), years.max()
year_range = st.sidebar.slider("Select Year Range", int(year_min), int(year_max), (2015, 2025))

categories = df_long['Category'].dropna().unique()   # <- FIX here
selected_category = st.sidebar.selectbox("Select Revenue Category", sorted(categories))


# --- Filtered Data ---
filtered_df = df_long[(df_long['Category'] == selected_category) &
                      (df_long['Year'] >= year_range[0]) &
                      (df_long['Year'] <= year_range[1])]

# --- Title & Intro ---
st.markdown("# 💰 Sri Lanka Revenue Dashboard")
st.markdown("""
Analyze trends in various government revenue streams in Sri Lanka from 2015 to 2025.  
Use the sidebar to select a revenue category and a year range.
""")
st.markdown("---")

# --- Chart ---
st.markdown(f"### 📊 {selected_category} ({year_range[0]} – {year_range[1]})")
fig = px.line(filtered_df, x="Year", y="Revenue", title=selected_category)
st.plotly_chart(fig, use_container_width=True)

# --- KPIs ---
st.markdown("### 📌 Key Stats")
latest_year = filtered_df['Year'].max()
latest_revenue = filtered_df[filtered_df['Year'] == latest_year]['Revenue'].values[0]
average_revenue = round(filtered_df['Revenue'].mean(), 2)
max_revenue = filtered_df['Revenue'].max()

col1, col2, col3 = st.columns(3)
col1.metric("Latest Revenue", f"{latest_revenue:,.0f}")
col2.metric("Max Revenue", f"{max_revenue:,.0f}")
col3.metric("Average Revenue", f"{average_revenue:,.0f}")

# --- Footer ---
st.markdown("---")
st.markdown("📘 Created by **Dinethya Marasinghe** – IIT ID: 20233069  \n🧾 Module: 5DATA004W – Data Science Project Lifecycle")

