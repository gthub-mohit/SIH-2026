"""
SIH 2026 Presentation Dataset Generator - 5x5 Grid Edition (25 Readings)
Problem Statement ID: 26064 (NCPOR / Ministry of Earth Sciences)
"Low-Cost Deployable Seafloor Metal Detection Sensor for Ocean Resource Exploration"

Generates exactly 25 discrete survey readings corresponding 1:1 to the 5x5 survey grid:
- Grid: 5 columns x 5 rows = 25 cells (0 to 50 on X & Y, centered at 5, 15, 25, 35, 45)
- Normal: 14 readings (56% ~ approx 55%)
- Weak Anomaly: 6 readings (24% - Polymetallic Nodule Bed & Halos)
- Strong Anomaly: 5 readings (20% - Hydrothermal Massive Sulfide Chimney)
- Total Readings = 25

Updates:
- src/data/mockSensorData.json (for frontend mock mode)
- seafloor.db (for live backend demonstrations)
"""

import json
import sqlite3
import os
from datetime import datetime, timezone, timedelta

def generate_25_cell_dataset():
    sensor_id = "SFS-001"
    start_time = datetime(2026, 9, 5, 10, 0, 0, tzinfo=timezone.utc)

    # 5x5 Discrete Grid Coordinates (5.0, 15.0, 25.0, 35.0, 45.0)
    # 14 Normal (56%), 6 Weak Anomaly (24%), 5 Strong Anomaly (20%)
    cells_spec = [
        # Row 0 (Y = 5.0) - Quiet Geomagnetic Seafloor Baseline
        {"x": 5.0,  "y": 5.0, "classification": "normal",         "anomaly_score": 0.08, "bx": 0.18, "by": 0.20, "bz": 0.23, "mag": 0.35},
        {"x": 15.0, "y": 5.0, "classification": "normal",         "anomaly_score": 0.09, "bx": 0.18, "by": 0.21, "bz": 0.24, "mag": 0.36},
        {"x": 25.0, "y": 5.0, "classification": "normal",         "anomaly_score": 0.07, "bx": 0.17, "by": 0.20, "bz": 0.22, "mag": 0.34},
        {"x": 35.0, "y": 5.0, "classification": "normal",         "anomaly_score": 0.11, "bx": 0.19, "by": 0.20, "bz": 0.24, "mag": 0.37},
        {"x": 45.0, "y": 5.0, "classification": "normal",         "anomaly_score": 0.08, "bx": 0.17, "by": 0.19, "bz": 0.24, "mag": 0.35},

        # Row 1 (Y = 15.0) - Polymetallic Nodule Deposit Field (Weak Anomalies)
        {"x": 5.0,  "y": 15.0, "classification": "normal",        "anomaly_score": 0.10, "bx": 0.18, "by": 0.20, "bz": 0.24, "mag": 0.36},
        {"x": 15.0, "y": 15.0, "classification": "weak_anomaly",  "anomaly_score": 0.58, "bx": 0.38, "by": 0.42, "bz": 0.44, "mag": 0.72},
        {"x": 25.0, "y": 15.0, "classification": "weak_anomaly",  "anomaly_score": 0.68, "bx": 0.45, "by": 0.48, "bz": 0.55, "mag": 0.86},
        {"x": 35.0, "y": 15.0, "classification": "weak_anomaly",  "anomaly_score": 0.55, "bx": 0.36, "by": 0.39, "bz": 0.43, "mag": 0.69},
        {"x": 45.0, "y": 15.0, "classification": "normal",        "anomaly_score": 0.12, "bx": 0.19, "by": 0.21, "bz": 0.25, "mag": 0.38},

        # Row 2 (Y = 25.0) - Hydrothermal Massive Sulfide Transition & High Anomaly
        {"x": 5.0,  "y": 25.0, "classification": "normal",         "anomaly_score": 0.07, "bx": 0.17, "by": 0.20, "bz": 0.22, "mag": 0.34},
        {"x": 15.0, "y": 25.0, "classification": "weak_anomaly",   "anomaly_score": 0.52, "bx": 0.34, "by": 0.38, "bz": 0.40, "mag": 0.65},
        {"x": 25.0, "y": 25.0, "classification": "strong_anomaly", "anomaly_score": 0.84, "bx": 0.62, "by": 0.75, "bz": 0.95, "mag": 1.35},
        {"x": 35.0, "y": 25.0, "classification": "strong_anomaly", "anomaly_score": 0.96, "bx": 0.85, "by": 1.05, "bz": 1.30, "mag": 1.88},
        {"x": 45.0, "y": 25.0, "classification": "weak_anomaly",   "anomaly_score": 0.62, "bx": 0.40, "by": 0.45, "bz": 0.49, "mag": 0.78},

        # Row 3 (Y = 35.0) - Ore Chimney Peak & Active Sulfide Mound
        {"x": 5.0,  "y": 35.0, "classification": "normal",         "anomaly_score": 0.09, "bx": 0.18, "by": 0.20, "bz": 0.23, "mag": 0.35},
        {"x": 15.0, "y": 35.0, "classification": "normal",         "anomaly_score": 0.12, "bx": 0.19, "by": 0.21, "bz": 0.24, "mag": 0.37},
        {"x": 25.0, "y": 35.0, "classification": "strong_anomaly", "anomaly_score": 0.92, "bx": 0.80, "by": 0.98, "bz": 1.20, "mag": 1.74},
        {"x": 35.0, "y": 35.0, "classification": "strong_anomaly", "anomaly_score": 0.98, "bx": 0.95, "by": 1.18, "bz": 1.45, "mag": 2.10},
        {"x": 45.0, "y": 35.0, "classification": "strong_anomaly", "anomaly_score": 0.86, "bx": 0.65, "by": 0.80, "bz": 1.00, "mag": 1.42},

        # Row 4 (Y = 45.0) - Southern Boundary Recovery
        {"x": 5.0,  "y": 45.0, "classification": "normal",         "anomaly_score": 0.08, "bx": 0.17, "by": 0.20, "bz": 0.23, "mag": 0.35},
        {"x": 15.0, "y": 45.0, "classification": "normal",         "anomaly_score": 0.10, "bx": 0.18, "by": 0.21, "bz": 0.24, "mag": 0.36},
        {"x": 25.0, "y": 45.0, "classification": "weak_anomaly",   "anomaly_score": 0.49, "bx": 0.32, "by": 0.35, "bz": 0.38, "mag": 0.60},
        {"x": 35.0, "y": 45.0, "classification": "normal",         "anomaly_score": 0.14, "bx": 0.20, "by": 0.22, "bz": 0.25, "mag": 0.39},
        {"x": 45.0, "y": 45.0, "classification": "normal",         "anomaly_score": 0.08, "bx": 0.18, "by": 0.20, "bz": 0.23, "mag": 0.35},
    ]

    readings = []
    for idx, cell in enumerate(cells_spec):
        t = start_time + timedelta(seconds=idx * 10)
        record = {
            "sensor_id": sensor_id,
            "timestamp": t.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "x": float(cell["x"]),
            "y": float(cell["y"]),
            "bx": float(cell["bx"]),
            "by": float(cell["by"]),
            "bz": float(cell["bz"]),
            "magnetic_signal": float(cell["mag"]),
            "anomaly_score": float(cell["anomaly_score"]),
            "classification": cell["classification"],
        }
        readings.append(record)

    return readings

def main():
    readings = generate_25_cell_dataset()
    print(f"[Dataset Generator] Generated {len(readings)} grid readings for 5x5 survey.")

    normal_count = sum(1 for r in readings if r["classification"] == "normal")
    weak_count = sum(1 for r in readings if r["classification"] == "weak_anomaly")
    strong_count = sum(1 for r in readings if r["classification"] == "strong_anomaly")
    total = len(readings)

    print(f" - Normal Baseline Points: {normal_count} ({normal_count/total*100:.1f}%)")
    print(f" - Weak Anomaly (Nodules): {weak_count} ({weak_count/total*100:.1f}%)")
    print(f" - Strong Anomaly (Sulfides): {strong_count} ({strong_count/total*100:.1f}%)")
    print(f" - Total Survey Readings: {total}")

    # 1. Update frontend mockSensorData.json
    frontend_json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "data", "mockSensorData.json")
    with open(frontend_json_path, "w", encoding="utf-8") as f:
        json.dump(readings, f, indent=2)
    print(f"[Frontend Mock] Successfully saved 25 readings to {frontend_json_path}")

    # 2. Update backend seafloor.db
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "seafloor.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS readings")
    cur.execute("""
        CREATE TABLE readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            x REAL NOT NULL,
            y REAL NOT NULL,
            bx REAL NOT NULL,
            by REAL NOT NULL,
            bz REAL NOT NULL,
            magnetic_signal REAL NOT NULL,
            anomaly_score REAL NOT NULL,
            classification TEXT NOT NULL,
            raw_payload TEXT
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_readings_coords ON readings(x, y)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_readings_timestamp ON readings(timestamp)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_readings_sensor_id ON readings(sensor_id)")

    for r in readings:
        cur.execute(
            """
            INSERT INTO readings (
                sensor_id, timestamp, x, y, bx, by, bz,
                magnetic_signal, anomaly_score, classification, raw_payload
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                r["sensor_id"],
                r["timestamp"],
                r["x"],
                r["y"],
                r["bx"],
                r["by"],
                r["bz"],
                r["magnetic_signal"],
                r["anomaly_score"],
                r["classification"],
                json.dumps({}),
            )
        )
    conn.commit()
    conn.close()
    print(f"[Backend SQLite] Inserted {len(readings)} records into {db_path}")

if __name__ == "__main__":
    main()
