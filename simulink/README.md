# MATLAB/Simulink EV Battery Model

This folder contains the simplified EV battery model developed using MATLAB/Simulink.

## Implemented Features

- SOC estimation using coulomb counting
- Battery terminal voltage calculation using an equivalent-circuit approximation
- Battery temperature estimation using resistive heating and cooling

## Model Parameters

| Parameter | Value |
|---|---|
| Battery capacity | 60 Ah |
| Initial SOC | 80% |
| Discharge current | 20 A |
| Internal resistance | 0.08 Ω |
| Initial temperature | 25 °C |
| Simulation duration | 600 seconds |

## Model Outputs

The model generates battery voltage, current, SOC, and temperature measurements.

These measurements are exported to `data/battery_simulation.csv` for Python-based CAN communication and Digital Twin development.

**Note:** This is a simplified educational simulation, not a validated automotive battery model.
