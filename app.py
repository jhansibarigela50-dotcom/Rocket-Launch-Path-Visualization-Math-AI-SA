import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# -------------------------------
# Load and Clean Dataset
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("missions.csv")
    st.write("Available columns:", df.columns.tolist())

    if "Launch Date" in df.columns:
        df["Launch Date"] = pd.to_datetime(df["Launch Date"], errors="coerce")

    numeric_cols = [col for col in [
        "Mission Cost (billion USD)", "Payload Weight (tons)", "Fuel Consumption (tons)",
        "Mission Duration (years)", "Distance from Earth (light-years)", "Crew Size", "Scientific Yield (points)"
    ] if col in df.columns]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col].fillna(df[col].median(), inplace=True)

    for col in ["Mission Type", "Launch Vehicle"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown").astype(str).str.strip().str.lower()

    if "Mission Success (%)" in df.columns:
        df["Mission Success (%)"] = pd.to_numeric(df["Mission Success (%)"], errors="coerce")
        df["Mission Success (%)"].fillna(df["Mission Success (%)"].median(), inplace=True)

    df.drop_duplicates(inplace=True)
    return df

df = load_data()

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Dashboard", "Simulation"])

# -------------------------------
# Dashboard Page
# -------------------------------
if page == "Dashboard":
    st.title("🚀 Rocket Launch Visualization Dashboard")
    st.write("Explore mission data: payloads, fuel, costs, crew, and outcomes.")

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

    if not filtered_df.empty:
        # 1. Payload vs Fuel Consumption
        if {"Payload Weight (tons)", "Fuel Consumption (tons)"} <= set(filtered_df.columns):
            st.subheader("1. Payload vs Fuel Consumption")
            fig1 = px.scatter(filtered_df, x="Payload Weight (tons)", y="Fuel Consumption (tons)",
                              color="Mission Success (%)" if "Mission Success (%)" in filtered_df.columns else None,
                              hover_data=["Mission Name"] if "Mission Name" in filtered_df.columns else None,
                              title="Payload vs Fuel Consumption")
            st.plotly_chart(fig1)
            st.info("Insight: Heavier payloads generally require more fuel — this matches realistic expectations.")

        # 2. Mission Cost: Success vs Failure
        if {"Mission Cost (billion USD)", "Mission Success (%)"} <= set(filtered_df.columns):
            st.subheader("2. Mission Cost: Success vs Failure")
            fig2, ax2 = plt.subplots()
            sns.boxplot(x="Mission Success (%)", y="Mission Cost (billion USD)", data=filtered_df, ax=ax2)
            ax2.set_title("Mission Cost Distribution by Success Rate")
            st.pyplot(fig2)
            st.info("Insight: Successful missions tend to cluster at higher costs, suggesting investment improves outcomes.")

        # 3. Mission Duration vs Distance from Earth
        if {"Distance from Earth (light-years)", "Mission Duration (years)"} <= set(filtered_df.columns):
            st.subheader("3. Mission Duration vs Distance from Earth")
            fig3 = px.scatter(filtered_df,
                              x="Distance from Earth (light-years)",
                              y="Mission Duration (years)",
                              color="Mission Success (%)" if "Mission Success (%)" in filtered_df.columns else None,
                              size="Crew Size" if "Crew Size" in filtered_df.columns else None,
                              hover_data=["Mission Name", "Target Name"] if {"Mission Name","Target Name"} <= set(filtered_df.columns) else None,
                              title="Mission Duration vs Distance from Earth")
            st.plotly_chart(fig3)
            st.info("Insight: Longer distances correspond to longer mission durations — confirming realistic behavior.")

        # 4. Crew Size vs Mission Success
        if {"Crew Size", "Mission Success (%)"} <= set(filtered_df.columns):
            st.subheader("4. Crew Size vs Mission Success")
            fig4, ax4 = plt.subplots()
            sns.boxplot(x="Mission Success (%)", y="Crew Size", data=filtered_df, ax=ax4)
            ax4.set_title("Crew Size vs Mission Success")
            st.pyplot(fig4)
            st.info("Insight: Larger crews may correlate with higher success, reflecting better mission support.")

        # 5. Scientific Yield vs Mission Cost
        if {"Mission Cost (billion USD)", "Scientific Yield (points)"} <= set(filtered_df.columns):
            st.subheader("5. Scientific Yield vs Mission Cost")
            fig5 = px.scatter(filtered_df, x="Mission Cost (billion USD)", y="Scientific Yield (points)",
                              color="Mission Success (%)" if "Mission Success (%)" in filtered_df.columns else None,
                              title="Scientific Yield vs Mission Cost")
            st.plotly_chart(fig5)
            st.info("Insight: Higher mission costs often lead to greater scientific yield — consistent with expectations.")

        # 6. Correlation Heatmap
        st.subheader("6. Correlation Heatmap")
        numeric_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns
        if len(numeric_cols) > 1:
            corr = filtered_df[numeric_cols].corr()
            fig6, ax6 = plt.subplots(figsize=(8,6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax6)
            ax6.set_title("Correlation Heatmap of Numeric Features")
            st.pyplot(fig6)
            st.info("Insight: Correlation values highlight which factors most strongly relate to mission success.")
        else:
            st.info("Not enough numeric data to compute correlations.")

    st.subheader("📊 Data Preview")
    st.dataframe(filtered_df.head(20))

# -------------------------------
# Simulation Page
# -------------------------------
elif page == "Simulation":
    st.title("🛰️ Rocket Launch Simulation")
    st.write("This simulation uses differential equations to model a rocket launch step by step.")

    # User inputs
    mass = st.number_input("Initial Rocket Mass (kg)", value=500000)
    thrust = st.number_input("Thrust (N)", value=7.6e6)
    fuel = st.number_input("Fuel Mass (kg)", value=300000)
    payload = st.number_input("Payload Mass (kg)", value=20000)
    drag_factor = st.number_input("Drag Factor", value=0.5)
    time_steps = st.slider("Number of Time Steps", 50, 500, 200)

    if st.button("Run Simulation"):
        g = 9.81
        dt = 1  # seconds per step

        velocity = 0
        altitude = 0
        results = []

        current_mass = mass
        fuel_remaining = fuel

        for t in range(time_steps):
            # Forces
            gravity_force = current_mass * g
            drag_force = drag_factor * velocity**2
            net_force = thrust - gravity_force - drag_force

            # Acceleration
            acceleration = net_force / current_mass

            # Update velocity and altitude
            velocity += acceleration * dt
            altitude += velocity * dt

            # Burn fuel
            if fuel_remaining > 0:
                fuel_burn = fuel / time_steps
                fuel_remaining -= fuel_burn
                current_mass -= fuel_burn

            results.append([t, altitude, velocity, acceleration, fuel_remaining])

        sim_df = pd.DataFrame(results, columns=["Time (s)", "Altitude (m)", "Velocity (m/s)", "Acceleration (m/s^2)", "Fuel Remaining (kg)"])

        st.subheader("Simulation Results")
        st.dataframe(sim_df.head(20))

        # Plot altitude vs time
        fig_alt = px.line(sim_df, x="Time (s)", y="Altitude (m)", title="Altitude vs Time")
        st.plotly_chart(fig_alt)

        # Plot velocity vs time
        fig_vel = px.line(sim_df, x="Time (s)", y="Velocity (m/s)", title="Velocity vs Time")
        st.plotly_chart(fig_vel)

        # Plot fuel vs time
        fig_fuel = px.line(sim_df, x="Time (s)", y="Fuel Remaining (kg)", title="Fuel Remaining vs Time")
        st.plotly_chart(fig_fuel)

        st.info("Insight: Altitude increases as thrust overcomes gravity and drag. Fuel burn reduces mass, affecting acceleration.")
