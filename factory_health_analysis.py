
import csv
import os

TEMP_LIMIT = 80
VIBRATION_LIMIT = 7.0

folder = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(folder, "factory_data.csv")

machine_data = {}

# Read the saved sensor data
with open(file_path, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        machine = row["Machine"]
        temperature = float(row["Temperature"])
        vibration = float(row["Vibration"])

        if machine not in machine_data:
            machine_data[machine] = {
                "total_temperature": 0,
                "readings": 0,
                "alerts": 0
            }

        machine_data[machine]["total_temperature"] += temperature
        machine_data[machine]["readings"] += 1

        if temperature > TEMP_LIMIT or vibration > VIBRATION_LIMIT:
            machine_data[machine]["alerts"] += 1

# Generate the health report
print("SMART FACTORY - MACHINE HEALTH REPORT")
print("=" * 45)

for machine, data in machine_data.items():
    average_temperature = (
        data["total_temperature"] / data["readings"]
    )

    print(f"\nMachine: {machine}")
    print(f"Total readings: {data['readings']}")
    print(f"Average temperature: {average_temperature:.2f} C")
    print(f"Abnormal readings: {data['alerts']}")

    if data["alerts"] > 0:
        print("Health status: NEEDS ATTENTION")
    else:
        print("Health status: NO ALERTS RECORDED")

print("\nAnalysis completed.")
