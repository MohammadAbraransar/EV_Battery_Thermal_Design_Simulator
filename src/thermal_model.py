"""Transparent first-order lumped battery pack thermal model."""
import numpy as np

def simulate_pack(voltage_v, power_w, resistance_ohm, thermal_capacity_j_k,
                  ua_w_k, ambient_c, duration_min, dt_s=5):
    """Simulate pack temperature using explicit Euler integration.

    C_th dT/dt = I^2 R - UA(T - T_ambient)
    """
    if min(voltage_v, resistance_ohm, thermal_capacity_j_k, ua_w_k, dt_s) <= 0:
        raise ValueError("Voltage, resistance, thermal capacity, UA, and time step must be positive.")
    current_a = power_w / voltage_v
    heat_w = current_a**2 * resistance_ohm
    n = int(duration_min * 60 / dt_s) + 1
    time_s = np.arange(n, dtype=float) * dt_s
    temp = np.empty(n, dtype=float)
    temp[0] = ambient_c
    for i in range(1, n):
        loss_w = ua_w_k * (temp[i-1] - ambient_c)
        temp[i] = temp[i-1] + (heat_w - loss_w) * dt_s / thermal_capacity_j_k
    return {
        "time_s": time_s,
        "temperature_c": temp,
        "current_a": current_a,
        "heat_w": heat_w,
        "steady_state_rise_c": heat_w / ua_w_k,
    }
