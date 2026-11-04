# EV Battery Thermal Design Studio

A deployable interactive educational project for the broad internship area **Electric Vehicle Design & Simulation**.

## Project
**Design and Thermal Performance Analysis of an Electric Vehicle Battery Pack**

This application models a simplified battery pack and compares passive, forced-air, and liquid-cooling scenarios. It is suitable as a learning/demo artifact for mechanical engineering concepts: heat generation, thermal capacity, heat transfer, system assumptions, simulation, and engineering interpretation.

### Important integrity / technical note
The model is an independent educational simulation. It does not establish that a particular internship task was completed. All input values and resulting numbers are illustrative model outputs, not actual internship measurements or manufacturer-approved specifications. State this clearly during any presentation.

## Run locally (Windows / VS Code)
1. Install Python 3.10 or later.
2. Extract the ZIP and open this folder in VS Code.
3. In Terminal:
   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   streamlit run app.py
   ```
4. The app opens in a browser at the local Streamlit address.

## Deploy
### Streamlit Community Cloud
Push the folder to a GitHub repository. In Streamlit Community Cloud, select the repo, branch, and `app.py`; install dependencies from `requirements.txt`.

### Render
Create a Python web service using:
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## Governing equations
- `I = P / V`
- `Q_gen = I² R`
- `C_th dT/dt = I²R - UA(T - T_ambient)`
- `ΔT_ss = Q_gen / UA`

`UA` represents effective heat-transfer conductance in W/K. In this scenario comparison, higher UA indicates stronger modeled heat rejection. It is not a precise cooling-system design model.

## Scope and limitations
Single uniform pack temperature; constant pack voltage, power, resistance, heat capacity and UA; no SOC-dependent properties, aging, detailed electrochemistry, cell-level hot spots, coolant flow, or experimental validation. Use for concept exploration only.

## Files
- `app.py` — interactive dashboard
- `src/thermal_model.py` — model implementation
- `requirements.txt` — Python packages
- `render.yaml` — optional Render blueprint
