# NeuroGrid — Offline-Resilient Smart Farming

NeuroGrid is a prototype concept for monitoring farm conditions when internet connectivity is unreliable. It collects soil moisture, temperature, humidity, and rainfall readings, stores readings locally during outages, and prioritizes important events for synchronization when connectivity returns.

> **Prototype status:** This repository contains a runnable Python simulation and example ESP32 firmware scaffold. The ESP32 hardware integration has not been validated on physical hardware. Sensor pins, calibration, and network credentials must be configured for the target build.

## Problem

Rural farms may use sensors to guide irrigation and field decisions, but intermittent internet can interrupt cloud uploads and cause gaps in monitoring data.

## Proposed solution

- **Sensor monitoring:** soil moisture, temperature, humidity, and rainfall.
- **Adaptive Spike Encoding (simulation):** records a reading when a value changes enough or a maximum interval is reached, reducing redundant records.
- **Local-first storage:** retains readings while offline.
- **Priority-Based Synchronization:** uploads alert/abnormal readings before routine readings when connectivity returns.
- **Offline simulation:** test outages without needing physical hardware or a cloud account.

## Repository layout

```text
NeuroGrid_project/
├── firmware/
│   └── neurogrid_esp32.ino
├── simulator/
│   └── neurogrid.py
├── data/
│   └── sample_sensor_readings.csv
├── docs/
│   └── architecture.md
├── tests/
│   └── test_neurogrid.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Run the simulation

Requires Python 3.10+; no third-party packages are needed.

```bash
python simulator/neurogrid.py --input data/sample_sensor_readings.csv --offline-every 4
```

The simulation prints encoded records and the order in which queued readings would be synchronized.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## ESP32 firmware scaffold

Open `firmware/neurogrid_esp32.ino` in Arduino IDE. Select a suitable ESP32 board and install the relevant sensor libraries before adapting the scaffold. The current sketch demonstrates the data model and offline queue concept; sensor pins, actual sensor drivers, persistent storage, and network upload are marked as integration tasks.

## Suggested demo

1. Run the Python simulation.
2. Show readings being generated while the simulated connection is offline.
3. Point out that only changed/periodic values are encoded.
4. Restore connectivity and show priority events being synchronized first.
5. Explain that the simulation validates logic, not field performance.

## Safety and limitations

- Thresholds in the simulator are illustrative and must be calibrated for local crops, soil, and sensors.
- The code does not automatically control irrigation equipment.
- Do not place real Wi-Fi passwords, API keys, or personal information in this repository.
- This is a student prototype, not a certified agricultural monitoring product.

## Future work

- Integrate calibrated sensors and SD-card/flash storage.
- Add MQTT/HTTPS upload and acknowledgements.
- Add retry handling, duplicate prevention, and power-loss recovery.
- Evaluate encoding efficiency and data-loss rate using field measurements.
