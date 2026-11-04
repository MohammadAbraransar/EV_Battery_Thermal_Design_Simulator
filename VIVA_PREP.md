# Viva / Demo Preparation

## 30-second introduction
“My project is an educational thermal design study for an EV battery pack. Battery cells generate heat due to internal electrical resistance. I built a simplified lumped thermal model and an interactive dashboard to compare how assumed passive, forced-air, and liquid-cooling strengths affect pack temperature during a constant-power operating case. It demonstrates the relationship between electrical losses, thermal capacity, and heat transfer. The values are illustrative model inputs, so the outputs are simulation results—not experimental test data.”

## Key concepts
- **Why thermal management?** Helps maintain battery performance, useful life, and operating-temperature control.
- **I = P/V:** Electrical current from constant power and nominal voltage.
- **I²R loss:** Equivalent resistive heat generation; increases quadratically with current.
- **Thermal capacity:** Energy required to change the modeled thermal mass temperature by one kelvin.
- **UA:** Effective heat-transfer conductance. Higher UA means stronger modeled heat removal for the same temperature difference.
- **Why plateau?** In the model, heat generation eventually balances heat rejection.
- **Why a single node?** It keeps the concept model transparent; it cannot resolve local hot spots.
- **What is not included?** SOC dependence, detailed cell geometry, coolant flow/temperature, aging, reversible heat, and experimental validation.

## Likely questions
1. What is your project objective?
2. Why is battery cooling necessary in an EV?
3. Explain the energy balance equation.
4. Why does heat generation depend on current squared?
5. What does UA mean and what are its units?
6. How does changing ambient temperature affect the results?
7. Why is the model called lumped-parameter?
8. What is explicit Euler integration?
9. What assumptions affect accuracy?
10. How would you validate the model?
11. How could a real liquid cooling system be modeled more accurately?
12. Are these experimental results? **No. They are outputs from an illustrative numerical model.**

## Be clear when presenting
Do not claim that values were measured at an internship site, that an industrial battery pack was physically built, or that the design is safety-certified. Explain the model honestly and show how its inputs can be replaced with documented data.
