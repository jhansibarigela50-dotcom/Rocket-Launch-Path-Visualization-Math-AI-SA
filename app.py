import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# -------------------------------
# Load and Clean Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("missions.csv")

    # Show column names for debugging
    st.write("Available columns:", df.columns.tolist())

    # Rename columns for easier access
    df.rename(columns=lambda x: x.strip(), inplace=True)

    # Convert Launch Date
    if "Launch Date" in df.columns:
        df["Launch Date"] = pd.to_datetime(df["Launch Date"], errors="coerce")

    # Clean numeric columns
    numeric_cols = [col for col in [
        "Mission Cost (billion USD)", "Payload Weight (tons)", "Fuel Consumption (tons)",
        "Mission Duration (years)", "Distance from Earth (light-years)", "Crew Size", "Scientific Yield (points)"
    ] if col in df.columns]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col].fillna(df[col].median(), inplace=True)

    # Clean categorical columns
    for col in ["Mission Type", "Launch Vehicle"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown").astype(str).str.strip().str.lower()

    # Clean Mission Success (%)
    if "Mission Success (%)" in df.columns:
        df["Mission Success (%)"] = pd.to_numeric(df["Mission Success (%)"], errors="coerce")
        df["Mission Success (%)"].fillna(df["Mission Success (%)"].median(), inplace=True)

    df.drop_duplicates(inplace=True)
    return df

df = load_data()

# -------------------------------
# Streamlit App Layout
# -------------------------------
st.title("🚀 Rocket Launch Visualization Dashboard")
st.write("Explore mission data: payloads, fuel, costs, crew, and outcomes.")

# Sidebar filters
st.sidebar.header("Filters")
mission_type = st.sidebar.selectbox("Select Mission Type", df["Mission Type"].unique()) if "Mission Type" in df.columns else None
vehicle = st.sidebar.selectbox("Select Launch Vehicle", df["Launch Vehicle"].unique()) if "Launch Vehicle" in df.columns else None

filtered_df = df.copy()
if mission_type:
    filtered_df = filtered_df[filtered_df["Mission Type"] == mission_type]
if vehicle:
    filtered_df = filtered_df[filtered_df["Launch Vehicle"] == vehicle]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")

# -------------------------------
# Visualizations
# -------------------------------
if not filtered_df.empty:
    if {"Payload Weight (tons)", "Fuel Consumption (tons)"} <= set(filtered_df.columns):
        st.subheader("1. Payload vs Fuel Consumption")
        fig1 = px.scatter(filtered_df, x="Payload Weight (tons)", y="Fuel Consumption (tons)",
                          color="Mission Success (%)" if "Mission Success (%)" in filtered_df.columns else None,
                          title="Payload vs Fuel Consumption")
        st.plotly_chart(fig1)

    if {"Mission Cost (billion USD)", "Mission Success (%)"} <= set(filtered_df.columns):
        st.subheader("2. Mission Cost: Success vs Failure")
        fig2, ax2 = plt.subplots()
        sns.barplot(x="Mission Success (%)", y="Mission Cost (billion USD)", data=filtered_df, ax=ax2)
        ax2.set_title("Mission Cost by Success Rate")
        st.pyplot(fig2)

    if {"Distance from Earth (light-years)", "Mission Duration (years)"} <= set(filtered_df.columns):
        st.subheader("3. Mission Duration vs Distance from Earth")
        fig3 = px.line(filtered_df, x="Distance from Earth (light-years)", y="Mission Duration (years)",
                       color="Mission Success (%)" if "Mission Success (%)" in filtered_df.columns else None,
                       title="Mission Duration vs Distance")
        st.plotly_chart(fig3)

    if {"Crew Size", "Mission Success (%)"} <= set(filtered_df.columns):
        st.subheader("4. Crew Size vs Mission Success")
        fig4, ax4 = plt.subplots()
        sns.boxplot(x="Mission Success (%)", y="Crew Size", data=filtered_df, ax=ax4)
        ax4.set_title("Crew Size vs Mission Success")
        st.pyplot(fig4)

    if {"Mission Cost (billion USD)", "Scientific Yield (points)"} <= set(filtered_df.columns):
        st.subheader("5. Scientific Yield vs Mission Cost")
        fig5 = px.scatter(filtered_df, x="Mission Cost (billion USD)", y="Scientific Yield (points)",
                          color="Mission Success (%)" if "Mission Success (%)" in filtered_df.columns else None,
                          title="Scientific Yield vs Mission Cost")
        st.plotly_chart(fig5)

# -------------------------------
# Data Preview
# -------------------------------
st.subheader("📊 Data Preview")
st.dataframe(filtered_df.head(20))
