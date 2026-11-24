# Python Source Code

This directory contains the Python implementation of the CAN-Based Digital Twin for EV Battery Monitoring and Fault Detection.

## Implemented Modules

- `can_simulator.py` — CAN message encoding and virtual transmission using python-can and cantools
- `can_decoder.py` — DBC-based CAN signal decoding
- `database.py` — SQLite time-series storage for simulated battery voltage, current, SOC, SOH, and temperature measurements
- `battery_model.py` — Battery state tracking and SOC/SOH monitoring
- `fault_detection.py` — Rule-based battery fault detection
- `pipeline.py` — End-to-end virtual CAN transmission,
  DBC decoding, and SQLite storage of battery measurements
## Planned Modules

- `dashboard.py` — Streamlit/Plotly battery monitoring dashboard
- `main.py` — Main application entry point

## Development Approach

The project is developed incrementally, with each module implemented, tested, and documented before integration.

The current workflow uses simulated MATLAB/Simulink battery measurements, DBC-based CAN communication, and Python-based data processing.

All battery measurements originate from a simplified simulation model. The project is intended for educational development and portfolio demonstration, not production automotive deployment.
