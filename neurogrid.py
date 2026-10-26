"""NeuroGrid offline-first sensor monitoring simulation (standard library only)."""
from __future__ import annotations
import argparse
import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

@dataclass
class Reading:
    timestamp: str
    soil_moisture: float
    temperature: float
    humidity: float
    rainfall: float

    def is_abnormal(self) -> bool:
        # Illustrative thresholds only; calibrate for the actual farm and sensors.
        return self.soil_moisture < 25 or self.temperature > 38 or self.rainfall > 20

class AdaptiveSpikeEncoder:
    """Keep a reading when a sensor changes beyond its threshold or time expires."""
    def __init__(self, thresholds=None, max_interval: int = 3):
        self.thresholds = thresholds or {
            "soil_moisture": 5.0, "temperature": 2.0,
            "humidity": 5.0, "rainfall": 3.0
        }
        self.max_interval = max_interval
        self.last_kept: Optional[Reading] = None
        self.skipped_since_keep = 0

    def should_encode(self, current: Reading) -> bool:
        if self.last_kept is None:
            return True
        changed = any(
            abs(getattr(current, key) - getattr(self.last_kept, key)) >= limit
            for key, limit in self.thresholds.items()
        )
        return changed or self.skipped_since_keep >= self.max_interval

    def encode(self, current: Reading) -> Optional[dict]:
        if self.should_encode(current):
            result = asdict(current)
            result["priority"] = "HIGH" if current.is_abnormal() else "NORMAL"
            self.last_kept = current
            self.skipped_since_keep = 0
            return result
        self.skipped_since_keep += 1
        return None

def load_readings(path: Path) -> list[Reading]:
    readings = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            readings.append(Reading(
                timestamp=row["timestamp"],
                soil_moisture=float(row["soil_moisture"]),
                temperature=float(row["temperature"]),
                humidity=float(row["humidity"]),
                rainfall=float(row["rainfall"]),
            ))
    return readings

def prioritize(records: list[dict]) -> list[dict]:
    """Return HIGH-priority records first, preserving order within each group."""
    return sorted(records, key=lambda x: 0 if x["priority"] == "HIGH" else 1)

def simulate(readings: list[Reading], offline_every: int = 4) -> dict:
    encoder = AdaptiveSpikeEncoder()
    local_queue = []
    encoded = []
    synced = []
    for index, reading in enumerate(readings):
        item = encoder.encode(reading)
        if item:
            encoded.append(item)
            local_queue.append(item)  # local-first queue, including while offline
        is_online = offline_every <= 0 or (index + 1) % offline_every != 0
        if is_online and local_queue:
            # High-priority alerts first; stable order within each priority.
            local_queue[:] = prioritize(local_queue)
            synced.extend(local_queue)
            local_queue.clear()
    # Remaining records stay locally queued if the simulated run ends offline.
    return {"encoded": encoded, "synced": synced, "queued": local_queue}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="data/sample_sensor_readings.csv")
    parser.add_argument("--offline-every", type=int, default=4,
                        help="Treat every Nth sample as offline; use 0 for always online.")
    args = parser.parse_args()
    result = simulate(load_readings(Path(args.input)), args.offline_every)
    print("=== NeuroGrid Simulation ===")
    print(f"Encoded records: {len(result['encoded'])}")
    print(f"Synced records:  {len(result['synced'])}")
    print(f"Still queued:    {len(result['queued'])}")
    print("\nEncoded records:")
    print(json.dumps(result["encoded"], indent=2))
    print("\nSync order:")
    print(json.dumps(result["synced"], indent=2))
    if result["queued"]:
        print("\nRecords retained locally:")
        print(json.dumps(result["queued"], indent=2))

if __name__ == "__main__":
    main()
