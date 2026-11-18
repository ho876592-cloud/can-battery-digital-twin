# Python Source Code

This directory contains the Python implementation of the CAN-Based Digital Twin for EV Battery Monitoring and Fault Detection.

## CAN Communication Modules

- `can_simulator.py` — CAN message encoding and virtual transmission using python-can and cantools
- `can_decoder.py` — DBC-based CAN signal decoding

## Planned Modules

- `battery_model.py` — Battery state tracking and SOC/SOH monitoring
- `database.py` — SQLite battery time-series storage
- `fault_detection.py` — Rule-based battery fault detection
- `dashboard.py` — Streamlit/Plotly battery monitoring dashboard
- `main.py` — Main application entry point

## Development Approach

The project is developed incrementally, with each module implemented, tested, and documented before integration.

All battery measurements originate from a simplified MATLAB/Simulink model and are intended for simulation-based development and testing.
