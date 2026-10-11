
import random
import time
import json
import boto3
from datetime import datetime

# AWS Lambda configuration
AWS_REGION = "us-east-1"
LAMBDA_FUNCTION = "SmartFactoryProcessor"

# Connect to AWS Lambda using your configured AWS credentials
lambda_client = boto3.client(
    "lambda",
    region_name=AWS_REGION
)

# Factory machines
machines = ["Machine_01", "Machine_02", "Machine_03"]

print("SMART FACTORY DIGITAL TWIN")
print("Monitoring machines using AWS Lambda")
print("=" * 45)

# Generate 10 rounds of sensor readings
for round_no in range(1, 11):
    print(f"\n--- Reading Round {round_no} ---")

    for machine in machines:
        temperature = round(random.uniform(50, 95), 2)
        vibration = round(random.uniform(1, 9), 2)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare sensor data for AWS Lambda
        payload = {
            "machine_id": machine,
            "temperature": temperature,
            "vibration": vibration
        }

        print(f"\nTime: {timestamp}")
        print(f"Machine: {machine}")
        print(f"Temperature: {temperature} °C")
        print(f"Vibration: {vibration}")

        try:
            # Send readings to AWS Lambda
            response = lambda_client.invoke(
                FunctionName=LAMBDA_FUNCTION,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload)
            )

            # Read the response from Lambda
            result = json.loads(response["Payload"].read())

            if response.get("FunctionError"):
                print("AWS Lambda execution failed:", result)
            else:
                body = json.loads(result["body"])
                status = body["status"]

                print(f"Cloud Status: {status}")

                if status == "ALERT":
                    print("WARNING: Abnormal machine readings detected!")

        except Exception as error:
            print("AWS connection/invocation error:", error)

        print("-" * 45)

    time.sleep(1)

print("\nFactory monitoring completed.");