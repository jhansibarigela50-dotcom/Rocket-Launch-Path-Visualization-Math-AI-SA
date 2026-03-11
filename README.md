# IDAI1021000480-Jhansi-Barigela
# Rocket Launch Path Visualization Web App
# Candidate Name: Jhansi Barigela
# Registration Number: 1000480
# CRS: Artificial Intelligence
# Course Name: Mathematics for AI
# School Name: Birla Open Minds International School

**App Link:** https://rocket-launch-path-visualization-math-ai-sa-akuzqujhejatj4jubq.streamlit.app/

**App Overview**

This project delivers a Streamlit web application that combines interactive data analysis of space missions with a physics-based rocket launch simulation. The dashboard visualizes mission datasets through scatter plots, box plots, and correlation heatmaps, allowing users to explore relationships such as payload versus fuel consumption, mission cost versus success, and scientific yield versus investment. Alongside these insights, the simulation module models rocket dynamics step by step using differential equations, updating acceleration, velocity, altitude, and fuel burn over time. Together, the two components provide both empirical analysis of past missions and a realistic simulation of rocket performance, creating a comprehensive tool for learning, exploration, and validation.

# Integration Details

The Rocket Launch project integrates two major components into a single Streamlit web application: 

**Mission Data Dashboard**

* Loads and cleans the dataset (missions.csv) using pandas.

* Visualizations built with Matplotlib, Seaborn, and Plotly are embedded directly in Streamlit using st.pyplot() and st.plotly_chart().

* Interactive filters (st.selectbox) allows users to explore missions by type and launch vehicle.

* Each visualization includes explanatory insights to validate whether the dataset reflects realistic mission behavior.

**Rocket Launch Simulation**

* Implements a physics-based simulation loop using differential equations.

* User inputs (mass, thrust, fuel, payload, drag factor, time steps) are collected via Streamlit widgets (st.number_input, st.slider).

* At each time step, acceleration, velocity, altitude, and fuel burn are calculated and stored in a pandas DataFrame.

* Results are visualized with Plotly line charts (altitude vs time, velocity vs time, fuel remaining vs time).

* Insights explain how thrust, gravity, drag, and fuel consumption affect rocket performance.

**Deployment & Accessibility**

* The app is organized in a single app.py file for easy deployment.

* Dependencies are listed in requirements.txt (Streamlit, pandas, seaborn, matplotlib, plotly).

* Hosted on Streamlit Cloud, with a live link provided in the README.

* Code and documentation are maintained in a GitHub repository for version control and collaboration.
