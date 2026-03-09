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

    # Convert Launch Date
    df['Launch Date'] = pd.to_datetime(df['Launch Date'], errors='coerce')

    # Convert numeric columns
    numeric_cols = ['Mission Cost', 'Payload Weight', 'Fuel Consumption',
                    'Mission Duration', 'Distance from Earth', 'Crew Size', 'Scientific Yield']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill missing values
    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)
    df['Mission Type'].fillna("Unknown", inplace=True)
    df['Launch Vehicle'].fillna("Unknown", inplace=True)
    df['Mission Success'] = df['Mission Success'].fillna("Unknown").str.strip().str.lower()

    # Remove duplicates and invalids
    df.drop_duplicates(inplace=True)
    df = df[df['Payload Weight'] >= 0]
    df = df[df['Fuel Consumption'] >= 0]

    return df

df = load_data()
st.write(df.columns.tolist())


# -------------------------------
# Streamlit App Layout
# -------------------------------
st.title("🚀 Rocket Launch Visualization Dashboard")
st.write("Explore mission data: payloads, fuel, costs, crew, and outcomes.")

# Sidebar filters
st.sidebar.header("Filters")
mission_type = st.sidebar.selectbox("Select Mission Type", df["Mission Type"].unique())
vehicle = st.sidebar.selectbox("Select Launch Vehicle", df["Launch Vehicle"].unique())

filtered_df = df[(df["Mission Type"] == mission_type) & (df["Launch Vehicle"] == vehicle)]

# -------------------------------
# Visualizations
# -------------------------------

st.subheader("1. Payload vs Fuel Consumption")
fig1 = px.scatter(filtered_df, x="Payload Weight", y="Fuel Consumption",
                  color="Mission Success", title="Payload vs Fuel Consumption")
st.plotly_chart(fig1)

st.subheader("2. Mission Cost: Success vs Failure")
fig2, ax2 = plt.subplots()
sns.barplot(x="Mission Success", y="Mission Cost", data=filtered_df, ax=ax2)
ax2.set_title("Mission Cost by Success/Failure")
st.pyplot(fig2)

st.subheader("3. Mission Duration vs Distance from Earth")
fig3 = px.line(filtered_df, x="Distance from Earth", y="Mission Duration",
               color="Mission Success", title="Mission Duration vs Distance")
st.plotly_chart(fig3)

st.subheader("4. Crew Size vs Mission Success")
fig4, ax4 = plt.subplots()
sns.boxplot(x="Mission Success", y="Crew Size", data=filtered_df, ax=ax4)
ax4.set_title("Crew Size vs Mission Success")
st.pyplot(fig4)

st.subheader("5. Scientific Yield vs Mission Cost")
fig5 = px.scatter(filtered_df, x="Mission Cost", y="Scientific Yield",
                  color="Mission Success", title="Scientific Yield vs Mission Cost")
st.plotly_chart(fig5)

# -------------------------------
# Data Preview
# -------------------------------
st.subheader("📊 Data Preview")
st.dataframe(filtered_df.head(20))
