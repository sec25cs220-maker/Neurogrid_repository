import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "simulator"))
from neurogrid import Reading, AdaptiveSpikeEncoder, simulate, prioritize

class NeuroGridTests(unittest.TestCase):
    def test_first_reading_is_encoded(self):
        encoder = AdaptiveSpikeEncoder()
        reading = Reading("t1", 50, 30, 60, 0)
        self.assertIsNotNone(encoder.encode(reading))

    def test_abnormal_soil_moisture_is_high_priority(self):
        reading = Reading("t2", 15, 30, 60, 0)
        self.assertTrue(reading.is_abnormal())

    def test_small_change_is_skipped_until_max_interval(self):
        encoder = AdaptiveSpikeEncoder(max_interval=1)
        self.assertIsNotNone(encoder.encode(Reading("t1", 50, 30, 60, 0)))
        self.assertIsNone(encoder.encode(Reading("t2", 51, 30, 61, 0)))
        self.assertIsNotNone(encoder.encode(Reading("t3", 51, 30, 61, 0)))

    def test_high_priority_synced_before_normal(self):
        records = [
            {"priority": "NORMAL", "timestamp": "t1"},
            {"priority": "HIGH", "timestamp": "t2"},
        ]
        ordered = prioritize(records)
        self.assertEqual([x["priority"] for x in ordered], ["HIGH", "NORMAL"])

if __name__ == "__main__":
    unittest.main()
