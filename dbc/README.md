# CAN Database (DBC)

This directory contains the custom CAN database for the simulated EV Battery Management System (BMS).

## CAN Message Definitions

| CAN ID | Message | Signals |
|---|---|---|
| 0x100 | Battery_Status | PackVoltage, PackCurrent, SOC |
| 0x101 | Battery_Thermal | PackTemperature, SOH |

Both messages use standard 11-bit CAN identifiers and 8-byte payloads.

The DBC defines signal positions, scaling factors, signedness, and engineering units.

The database was validated using Python `cantools`, including a battery status encoding and decoding round-trip test.

All messages are simulated and do not represent an OEM vehicle communication specification.
