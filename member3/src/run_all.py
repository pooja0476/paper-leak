import subprocess
import sys

scripts = [
    "member3/src/data_cleaning.py",
    "member3/src/feature_engineering.py",
    "member3/src/anomaly_detection.py",
    "member3/src/historical_analysis.py"
]

for script in scripts:
    print(f"\nRunning {script}...")
    subprocess.run([sys.executable, script], check=True)

print("\nAll Member 3 analysis tasks completed successfully!")