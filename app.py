import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.thermal_model import simulate_pack

st.set_page_config(page_title="EV Battery Thermal Design Studio", page_icon="⚡", layout="wide")

st.title("⚡ EV Battery Thermal Design Studio")
st.caption("A mechanical-engineering design study | Lumped thermal simulation | Educational model")

with st.sidebar:
    st.header("Design inputs")
    st.markdown("Adjust assumptions and run the model. Values are illustrative—not manufacturer specifications.")
    voltage = st.slider("Nominal pack voltage (V)", 200, 800, 400, 25)
    power_kw = st.slider("Pack power demand (kW)", 10, 150, 60, 5)
    resistance = st.number_input("Equivalent pack resistance (Ω)", min_value=0.001, max_value=0.2, value=0.025, step=0.001, format="%.3f")
    thermal_capacity = st.number_input("Pack thermal capacity (J/K)", min_value=10000, max_value=500000, value=100000, step=10000)
    ambient = st.slider("Ambient temperature (°C)", -10, 50, 25)
    duration = st.slider("Simulation duration (minutes)", 15, 240, 120, 15)
    st.subheader("Cooling scenarios: UA (W/K)")
    ua_passive = st.slider("Passive", 5, 40, 12)
    ua_air = st.slider("Forced air", 15, 100, 45)
    ua_liquid = st.slider("Liquid cooling", 30, 200, 95)
    run = st.button("Run simulation", type="primary", use_container_width=True)

if "run" not in st.session_state:
    st.session_state.run = True
if run:
    st.session_state.run = True

if st.session_state.run:
    scenarios = {
        "Passive cooling": ua_passive,
        "Forced-air cooling": ua_air,
        "Liquid cooling": ua_liquid,
    }
    all_data, summary = [], []
    for name, ua in scenarios.items():
        result = simulate_pack(
            voltage_v=voltage, power_w=power_kw*1000, resistance_ohm=resistance,
            thermal_capacity_j_k=thermal_capacity, ua_w_k=ua,
            ambient_c=ambient, duration_min=duration, dt_s=5
        )
        all_data.append(pd.DataFrame({
            "Time (min)": result["time_s"]/60,
            "Temperature (°C)": result["temperature_c"],
            "Cooling scenario": name,
        }))
        summary.append({
            "Cooling scenario": name,
            "UA (W/K)": ua,
            "Current (A)": result["current_a"],
            "Resistive heat (W)": result["heat_w"],
            "Peak temperature (°C)": float(np.max(result["temperature_c"])),
            "Final temperature (°C)": float(result["temperature_c"][-1]),
            "Steady-state rise (°C)": result["steady_state_rise_c"],
        })
    curves = pd.concat(all_data, ignore_index=True)
    summary_df = pd.DataFrame(summary)

    current = power_kw*1000/voltage
    heat = current**2*resistance
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pack current", f"{current:.1f} A")
    c2.metric("Estimated I²R heat", f"{heat:.1f} W")
    c3.metric("Pack power", f"{power_kw:.0f} kW")
    c4.metric("Ambient", f"{ambient} °C")

    st.subheader("Temperature response")
    fig, ax = plt.subplots(figsize=(10, 4.8))
    for name, frame in curves.groupby("Cooling scenario"):
        ax.plot(frame["Time (min)"], frame["Temperature (°C)"], label=name, linewidth=2.4)
    ax.axhline(ambient, linestyle="--", linewidth=1, label="Ambient")
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Modeled pack temperature (°C)")
    ax.grid(alpha=.25)
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.subheader("Scenario comparison")
    st.dataframe(summary_df.round(3), use_container_width=True, hide_index=True)
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(summary_df["Cooling scenario"], summary_df["Peak temperature (°C)"])
    ax2.set_ylabel("Peak temperature (°C)")
    ax2.set_title("Peak modeled temperature by cooling scenario")
    ax2.grid(axis="y", alpha=.25)
    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)

    st.download_button(
        "Download simulation results (CSV)",
        data=summary_df.to_csv(index=False).encode("utf-8"),
        file_name="ev_thermal_scenario_summary.csv",
        mime="text/csv",
    )
    st.info(
        "Interpretation: at the same current and heat generation, a higher UA represents stronger "
        "heat rejection and generally produces a lower temperature rise. The model is a single-node "
        "lumped approximation; it does not predict cell hot spots or certify battery safety."
    )

with st.expander("Engineering model, assumptions & limitations"):
    st.latex(r"I = \\frac{P}{V}")
    st.latex(r"\\dot{Q}_{gen} = I^2 R")
    st.latex(r"C_{th}\\frac{dT}{dt}=I^2R-UA(T-T_{amb})")
    st.markdown("""
    **Model assumptions:** constant power, voltage, equivalent resistance, thermal capacity and UA;
    uniform pack temperature; initially at ambient temperature; no SOC dependence, aging,
    electrochemical reversible heat, coolant dynamics, or spatial gradients.

    **Use:** educational comparison and concept demonstration. Inputs are scenario assumptions.
    Validate with credible component data and test measurements before using for design decisions.
    """)
