# Autthor: 2021-09-30 Tom Chen

import paramiko
from paramiko.ssh_exception import SSHException, NoValidConnectionsError  # Import the correct SSHException
import time
from datetime import datetime
import socket #Timeout Exception
import gc # For garbage collection
import os
import psutil # For checking memory usage
import pywhatkit # For sending WhatsApp messages



# Container Number Shown
container = 1


# Define the Phone Number
phone_number = "+14378781006"  # Replace with your phone number


# Boundary Values class to store the upper and lower limits for each parameter
class BoundaryValues:
    def __init__(self, T1_upper, T1_lower, T2_upper, TempDifference_upper, P4_upper, P4_lower, P5_upper):
        self.T1_upper = T1_upper
        self.T1_lower = T1_lower
        self.T2_upper = T2_upper
        self.TempDifference_upper = TempDifference_upper
        self.P4_upper = P4_upper
        self.P4_lower = P4_lower
        self.P5_upper = P5_upper
# Create an instance of the BoundaryValues class with the desired limits
boundVal = BoundaryValues(
    T1_lower=15, # Lower limit for T1
    T1_upper=30, # Upper limit for T1
    T2_upper=50, # Upper limit for T2
    TempDifference_upper=15, # Upper limit for temperature difference
    P4_lower=0.8, # Lower limit for P4
    P4_upper=1.5, # Upper limit for P4
    P5_upper=3.5  # Upper limit for P5
)



### [Variables to configure the script]
###
###
# Time interval in seconds to wait between each query (5 min = 300 seconds) (10 min = 600 seconds)
interval = 300
# SQL query to execute (Modify with your actual query)
query = "Select DateTime1, T2, T1, (T1-T2) As TempDifference, P4, P5 from Record ORDER BY DateTime1 DESC LIMIT 1;"  # Change as needed



### [Variables to track time for garbage collection]
###
###
start_time = time.time()  # Start time of the script
gc_interval = 48 * 60 * 60  # Garbage collection interval in seconds: 48 hours



### [List of Windows machines to connect to (add more as needed)]
###
###
hosts = [

    #C1 - C21 container CDU
    {"host": "10.1.7.159", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.2.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.3.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.4.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.5.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.6.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.7.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.8.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.9.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.10.7.253", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.11.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.12.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.13.7.253", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.14.7.252", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.15.7.253", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.16.7.253", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.17.7.253", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.18.7.253", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.19.7.253", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.20.7.253", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": "10.21.7.253", "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},


    # Add more host details as needed
]


# [Function Definitions]

# Function to check memory usage and trigger garbage collection
def memory_garbageCollection(start_time, gc_interval):
    #process = psutil.Process(os.getpid())
    #memory_info = process.memory_info()
    ### print(f"Memory usage before GC: {memory_info.rss / 1024 ** 2:.2f} MB")

    elapsed_time = time.time() - start_time
    if elapsed_time > gc_interval:  
        print("48 hours have passed. Triggering garbage collection.")
        gc.collect()  # Perform garbage collection
        start_time = time.time()  # Reset the timer after garbage collection

    # Check memory usage after GC
    #memory_info = process.memory_info() 
    ### print(f"Memory usage after GC: {memory_info.rss / 1024 ** 2:.2f} MB")


# Function to execute an SQLite query remotely via SSH
def execute_sqlite_query(host, port, username, password, db_path, query, timeout=30):

    try:
        # Create an SSH client instance
        ssh = paramiko.SSHClient()
        # Automatically add the SSH key to the known hosts (this may be insecure for production)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the remote host

        ###print(f"Connecting to {host}...")
        ssh.connect(host, port=port, username=username, password=password, timeout = timeout)
        
        # Format the SQLite query command
        command = f"sqlite3 {db_path} \"{query}\""
        
        # Execute the command remotely via SSH
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Fetch output and error (if any)
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        
        # If there's an error, print it
        if error:
            print(f"Error on {host}: {error}")
            return None
        
        # print(f"Output from {host}: {output}")
        return output  # Print the result of the query

    # Handle SSH-specific connection errors
    except (SSHException, NoValidConnectionsError) as e: 
        print(f"SSH Connection failed to {host}. Error: {str(e)}. Moving to the next host.\n")
        return None

    # In case some CDU is down, conection failed, move to the next CDU
    except socket.timeout as e:  # Handle timeout error for connections
        print(f"Connection to {host} timed out: {str(e)}\n")
        return None

    except TimeoutError as e:  # Catch Windows timeout error specifically
        print(f"TimeoutError for {host}: {str(e)}\n")
        return None
    
    except Exception as e:
        print(f"Error connecting to {host}: {str(e)}\n")
        return None
    
    finally:
        # Close SSH connection
        ssh.close()


# Function to generate a graphic record
def graphic_record(output, boundVal):
    
    result = output.split("|")

    # Extract the values from the output
    if len(result) == 6:
        DateTime1 = result[0].strip()
        T2 = result[1].strip()
        T1 = result[2].strip()
        TempDifference = result[3].strip()
        P4 = result[4].strip()
        P5 = result[5].strip()

        # Alert
        Alert_Data(T2, T1, P4, P5, boundVal)

    # for Debug need, add the following line

    
# Function to generate an alert, send an email, or perform any other action (WhatsApp, SMS, etc.)
def Alert_Data(T1, T2, P4, P5, boundVal):
    if float(T1) >= boundVal.T1_upper or float(T1) <= boundVal.T1_lower:
        message = f"Temperature T1 is out of range: {T1}°C"
        # print("[T1] Temperature exceeds limit. Sending an alert...")
        # Send an email, SMS, or perform any other action to alert the team
        # Sending the WhatsApp Message
        pywhatkit.sendwhatmsg_instantly(phone_number, message)
        # Displaying a Success Message
        print("WhatsApp message sent!")

    if float(T2) >= boundVal.T2_upper:
        message = f"Temperature T2 is too high: {T2}°C"
        # print("[T2] Temperature is too high. Sending an alert...")
        # Send an email, SMS, or perform any other action to alert the team
        # Sending the WhatsApp Message
        pywhatkit.sendwhatmsg_instantly(phone_number, message)
        # Displaying a Success Message
        print("WhatsApp message sent!")

    if float(T2) - float(T1) >= boundVal.TempDifference_upper:
        message = f"Temperature difference is too high: {float(T2) - float(T1)}°C"
        # print("Temperature difference is too high. Sending an alert...")
        # Send an email, SMS, or perform any other action to alert the team
        # Sending the WhatsApp Message
        pywhatkit.sendwhatmsg_instantly(phone_number, message)
        # Displaying a Success Message
        print("WhatsApp message sent!")

    if float(P4) >= boundVal.P4_upper or float(P4) <= boundVal.P4_lower:
        message = f"Pressure P4 is out of range: {P4}"
        print("[P4] Pressure exceeds limit. Sending an alert...")
        # Send an email, SMS, or perform any other action to alert the team
        # Sending the WhatsApp Message
        pywhatkit.sendwhatmsg_instantly(phone_number, message)
        # Displaying a Success Message
        print("WhatsApp message sent!")

    if float(P5) >= boundVal.P5_upper:
        message = f"Pressure P5 is too high: {P5}"
        # print("[P5] Pressure is too high. Sending an alert...")
        # Send an email, SMS, or perform any other action to alert the team
        # Sending the WhatsApp Message
        pywhatkit.sendwhatmsg_instantly(phone_number, message)
        # Displaying a Success Message
        print("WhatsApp message sent!")



# Function to Send WhatsApp Message
def send_whatsapp_message():
    # Use Twilio API to send a WhatsApp message - pay
    pass




### Main script logic
###
###
while True: # Infinite loop to keep running the script

    # Get the current timestamp in a desired format
    current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Example: 20241220_153045

    # Generate the file name with the timestamp
    output_file_name  = f"{current_timestamp}.txt"


    # Open the output file
    with open(output_file_name, "w") as file:
        # Write the header
        file.write("Results:\n")

        # Loop over the list of hosts and execute the SQLite query on each one
        for host_info in hosts:
            host = host_info["host"]
            port = host_info["port"]
            username = host_info["username"]
            password = host_info["password"]
            db_path = host_info["db_path"]
    
            # Execute SQLite query on each machine
            ### print("\n[C" + str(container) + "]")
            file.write(f"\n[C{container}] on Host: {host}\n")

            ### print(f"Executing query on {host}...")
            output = execute_sqlite_query(host, port, username, password, db_path, query)
    
            # Optionally, you can handle output here, e.g., save it to a file
            if output:

                ###print(f"Query result from {host}:")
                ###print("Date               | T2 | T1 |Diff| P4 | P5")
                ###print(output)

                file.write("Date               | T2  | T1  |Diff | P4  | P5\n")
                file.write(output + "\n")

                #!!! Generate a graphic record for continues monitoring
                graphic_record(output, boundVal) 
        
            else:
                file.write("No results returned, due to CDU down, or Data loss\n\n")

            container += 1


    # End script
    print(f"Query results saved to {output_file_name}\n\n")
    print("---------------------------------------------------\n")

    #!!! Check memory usage and trigger garbage collection
    memory_garbageCollection(start_time, gc_interval)

    # Sleep for the specified interval 5 min before running the script again
    time.sleep(interval)
    # reset for container counting
    container = 1





