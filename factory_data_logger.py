
import random
import time
import csv
import os
from datetime import datetime

machines = ["Machine_01", "Machine_02", "Machine_03"]

TEMP_LIMIT = 80
VIBRATION_LIMIT = 7.0

# Save the CSV file in the same folder as this Python file
folder = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(folder, "factory_data.csv")

# Create the CSV file and write headings
with open(file_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Timestamp",
        "Machine",
        "Temperature",
        "Vibration",
        "Status"
    ])

    print("SMART FACTORY DATA LOGGER")
    print("Recording sensor readings...\n")

    for round_no in range(1, 11):
        for machine in machines:
            temperature = round(random.uniform(50, 95), 2)
            vibration = round(random.uniform(1, 9), 2)

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            if temperature > TEMP_LIMIT or vibration > VIBRATION_LIMIT:
                status = "ALERT"
            else:
                status = "NORMAL"

            writer.writerow([
                timestamp,
                machine,
                temperature,
                vibration,
                status
            ])

            print(
                f"{machine} | Temp: {temperature} C | "
                f"Vibration: {vibration} | Status: {status}"
            )

        file.flush()
        print(f"Round {round_no} saved.")
        time.sleep(1)

print("\nData logging completed.")
print("CSV file saved at:")
print(file_path)
