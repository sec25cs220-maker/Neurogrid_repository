# NeuroGrid Architecture

## Data flow

```text
Sensors (soil moisture, temperature, humidity, rainfall)
                         |
                         v
                ESP32 / data collector
                         |
                         v
              Adaptive Spike Encoding
          (change threshold or max interval)
                         |
                         v
                 Local queue/storage
                         |
               Internet available?
                  /           \
                No             Yes
                |               |
       Keep readings locally    v
                         Priority-based sync
                         (HIGH before NORMAL)
                                  |
                                  v
                         Cloud/dashboard (future)
```

## Main modules

1. **Sensor collection:** reads four environmental measurements.
2. **Adaptive Spike Encoding:** keeps a reading when any measurement changes beyond its configured threshold, or after a maximum number of skipped samples.
3. **Local-first queue:** preserves encoded records until the simulated connection is available.
4. **Priority-based synchronization:** sends abnormal/high-priority records before routine records.
5. **Dashboard/cloud:** planned extension; not implemented in this repository.

## Illustrative alert rules

- Soil moisture below 25% → HIGH priority.
- Temperature above 38°C → HIGH priority.
- Rainfall above 20 mm → HIGH priority.

These values are placeholders for demonstration only. Actual thresholds depend on sensor calibration, soil type, crop, and local conditions.

## Prototype validation

The Python simulator and unit tests check encoding, alert classification, and priority ordering. They do not prove hardware reliability, sensor accuracy, or real cloud delivery.
