"""
To handle real-time data, calculate differences, and trigger alerts when thresholds are breached



Explanation:
Real-Time Data Fetching:

The script uses a loop to fetch real-time data periodically (e.g., every 5 seconds) from the SSH session.
Replace some_command_to_fetch_real_time_data with the actual command that provides live data.
Data Parsing:

The example assumes the output format is Value1=100, Value2=80. Adjust parsing logic for your specific data format.
Difference Calculation:

Calculates the absolute difference between Value1 and Value2.
Alerting:

Triggers an alert (print statement) if the difference exceeds the defined THRESHOLD.
Real-Time Monitoring:

Continuously fetches data, calculates the difference, and checks thresholds.


1. will the real time data crash the ssh connection? how is the garbage collection working

2. how should I run the python script 24 hours all the time, do I have to shut down the ssh connection often?

"""

import paramiko
from concurrent.futures import ThreadPoolExecutor
import time

# Define the Windows systems to connect to
systems = [
    {"host": "192.168.1.10", "username": "admin", "password": "password"},
    {"host": "192.168.1.11", "username": "admin", "password": "password"},
    # Add more systems as needed
]

# Threshold for the difference to trigger an alert
THRESHOLD = 50  # Adjust this value as needed

# Function to SSH and fetch real-time data
def monitor_system(system):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(system["host"], username=system["username"], password=system["password"])

        # Simulate real-time monitoring (replace with your real command)
        command = "some_command_to_fetch_real_time_data"  # Replace with your actual command
        while True:
            stdin, stdout, stderr = client.exec_command(command)

            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if error:
                print(f"{system['host']} - Error: {error}")
                break

            # Example: Parse output (adjust parsing logic based on real output)
            # Assume output is: "Value1=100, Value2=80"
            data = dict(item.split('=') for item in output.split(', '))
            value1 = int(data.get("Value1", 0))
            value2 = int(data.get("Value2", 0))
            difference = abs(value1 - value2)

            print(f"{system['host']} - Value1: {value1}, Value2: {value2}, Difference: {difference}")

            # Check if the difference exceeds the threshold
            if difference > THRESHOLD:
                print(f"ALERT: {system['host']} - Difference {difference} exceeded threshold {THRESHOLD}!")

            # Sleep for a defined interval (e.g., 5 seconds) for real-time monitoring
            time.sleep(5)

        client.close()

    except Exception as e:
        print(f"{system['host']} - Connection failed: {e}")

# Run the monitoring in parallel for all systems
with ThreadPoolExecutor(max_workers=len(systems)) as executor:
    executor.map(monitor_system, systems)
