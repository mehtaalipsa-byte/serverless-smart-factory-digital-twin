
import csv
import json
import os

folder = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(folder, "factory_data.csv")
json_path = os.path.join(folder, "factory_payload.json")

payloads = []

# Read sensor readings from the CSV file
with open(csv_path, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        temperature = float(row["Temperature"])
        vibration = float(row["Vibration"])

        # Prepare one machine reading as structured data
        payload = {
            "timestamp": row["Timestamp"],
            "machine_id": row["Machine"],
            "temperature": temperature,
            "vibration": vibration,
            "status": row["Status"]
        }

        payloads.append(payload)

# Save the readings in JSON format
with open(json_path, "w") as file:
    json.dump(payloads, file, indent=4)

print("SMART FACTORY - CLOUD DATA PREPARATION")
print("--------------------------------------")
print(f"Total readings prepared: {len(payloads)}")
print(f"JSON file saved to: {json_path}")

if payloads:
    print("\nExample payload:")
    print(json.dumps(payloads[0], indent=4))
