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
    st.write("Columns in dataset:", df.columns.tolist())

    # Convert Launch Date if present
    if "Launch Date" in df.columns:
        df["Launch Date"] = pd.to_datetime(df["Launch Date"], errors="coerce")

    # Handle numeric columns safely
    numeric_cols = [col for col in [
        "Mission Cost", "Payload Weight", "Fuel Consumption",
        "Mission Duration", "Distance from Earth", "Crew Size", "Scientific Yield"
    ] if col in df.columns]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col].fillna(df[col].median(), inplace=True)

    # Handle categorical columns safely
    categorical_cols = [col for col in ["Mission Type", "Launch Vehicle", "Mission Success"] if col in df.columns]
    for col in categorical_cols:
        df[col] = df[col].fillna("Unknown")
        df[col] = df[col].astype(str).str.strip().str.lower()

    # Remove duplicates
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
if "Mission Type" in df.columns:
    mission_type = st.sidebar.selectbox("Select Mission Type", df["Mission Type"].unique())
else:
    mission_type = None

if "Launch Vehicle" in df.columns:
    vehicle = st.sidebar.selectbox("Select Launch Vehicle", df["Launch Vehicle"].unique())
else:
    vehicle = None

filtered_df = df.copy()
if mission_type:
    filtered_df = filtered_df[filtered_df["Mission Type"] == mission_type]
if vehicle:
    filtered_df = filtered_df[filtered_df["Launch Vehicle"] == vehicle]

# -------------------------------
# Visualizations
# -------------------------------
if "Payload Weight" in filtered_df.columns and "Fuel Consumption" in filtered_df.columns:
    st.subheader("1. Payload vs Fuel Consumption")
    fig1 = px.scatter(filtered_df, x="Payload Weight", y="Fuel Consumption",
                      color="Mission Success" if "Mission Success" in filtered_df.columns else None,
                      title="Payload vs Fuel Consumption")
    st.plotly_chart(fig1)

if "Mission Cost" in filtered_df.columns and "Mission Success" in filtered_df.columns:
    st.subheader("2. Mission Cost: Success vs Failure")
    fig2, ax2 = plt.subplots()
    sns.barplot(x="Mission Success", y="Mission Cost", data=filtered_df, ax=ax2)
    ax2.set_title("Mission Cost by Success/Failure")
    st.pyplot(fig2)

if "Distance from Earth" in filtered_df.columns and "Mission Duration" in filtered_df.columns:
    st.subheader("3. Mission Duration vs Distance from Earth")
    fig3 = px.line(filtered_df, x="Distance from Earth", y="Mission Duration",
                   color="Mission Success" if "Mission Success" in filtered_df.columns else None,
                   title="Mission Duration vs Distance")
    st.plotly_chart(fig3)

if "Crew Size" in filtered_df.columns and "Mission Success" in filtered_df.columns:
    st.subheader("4. Crew Size vs Mission Success")
    fig4, ax4 = plt.subplots()
    sns.boxplot(x="Mission Success", y="Crew Size", data=filtered_df, ax=ax4)
    ax4.set_title("Crew Size vs Mission Success")
    st.pyplot(fig4)

if "Mission Cost" in filtered_df.columns and "Scientific Yield" in filtered_df.columns:
    st.subheader("5. Scientific Yield vs Mission Cost")
    fig5 = px.scatter(filtered_df, x="Mission Cost", y="Scientific Yield",
                      color="Mission Success" if "Mission Success" in filtered_df.columns else None,
                      title="Scientific Yield vs Mission Cost")
    st.plotly_chart(fig5)

# -------------------------------
# Data Preview
# -------------------------------
st.subheader("📊 Data Preview")
st.dataframe(filtered_df.head(20))
