import paramiko
from paramiko.ssh_exception import SSHException, NoValidConnectionsError  # Import the correct SSHException
import time
from datetime import datetime

import socket #Timeout Exception
import pandas as pd # Import pandas for Excel support


# IP address:
container_ip = [
    "10.1.7.159", # C1
    "10.2.7.252", # C2
    "10.3.7.252", # C3
    "10.4.7.252", # C4
    "10.5.7.252", # C5
    "10.6.7.252", # C6
    "10.7.7.252", # C7
    "10.8.7.252", # C8
    "10.9.7.252", # C9
    "10.10.7.253", # C10
    "10.11.7.252", # C11
    "10.12.7.252", # C12
    "10.13.7.253", # C13
    "10.14.7.252", # C14
    "10.15.7.253", # C15
    "10.16.7.253", # C16
    "10.17.7.253", # C17
    "10.18.7.253", # C18
    "10.19.7.253", # C19
    "10.20.7.253", # C20
    "10.21.7.253" # C21
]

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

# Function to display data - terminal
# def data_display_terminal():
    # pass

# Function to save data to file
# def data_save_file():
    # pass

# List of Windows machines to connect to (add more as needed)
hosts = [

    #C1 - C21 container CDU
    {"host": container_ip[0], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[1], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[2], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[3], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[4], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[5], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[6], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[7], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[8], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[9], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[10], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[11], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[12], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[13], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[14], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[15], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[16], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[17], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[18], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[19], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},
    {"host": container_ip[20], "port": 22, "username": "Administrator", "password": "admin", "db_path": r"D:\CDUMonitorDB\CDUMonitorDB.db"},


    # Add more host details as needed
]


# Get the current timestamp in a desired format
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Example: 20241220_153045
# Generate the file name with the timestamp
output_file_name  = f"S_{current_timestamp}.xlsx"


# Container Number Shown
container = 1

# SQL query to execute (Modify with your actual query)
query = "Select DateTime1, T2, T1, (T1-T2) As TempDifference, P4, P5 from Record ORDER BY DateTime1 DESC LIMIT 1;"  # Change as needed


# Get the container numbers from the user (terminal input)
selected_containers = input("Enter container number to query (e.g 1, 3, 5) or input '0' to select all containers: ")
selected_containers = [int(c.strip()) for c in selected_containers.split(",")]


# Initialize empty list to hold the results
all_results = []


if 0 in selected_containers: # to select all containers
    selected_containers = list(range(1, 22))


# Loop over the list of hosts and execute the SQLite query on each one
for host_info in hosts:

    # Check if the current container is selected
    if container in selected_containers:

        host = host_info["host"]
        port = host_info["port"]
        username = host_info["username"]
        password = host_info["password"]
        db_path = host_info["db_path"]
    
        # Execute SQLite query on each machine
        print("\n[C" + str(container) + "]")

        ### print(f"Executing query on {host}...")
        output = execute_sqlite_query(host, port, username, password, db_path, query)
    
        # Optionally, you can handle output here, e.g., save it to a file
        if output:

            rows = output.splitlines()
            for row in rows:
                columns = row.split('|')
                # Clean up spaces around columns
                columns = [col.strip() for col in columns]

                # Determine Day or Night based on the time
                datetime_str = columns[0]
                datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                if 6 <= datetime_obj.hour < 18:    # Day from 6:00 - 18:00
                    day_night = "Day"
                else:    # Night from 18:00 - 6:00
                    day_night = "Night"

                columns.insert(1, day_night) # Insert the Shift at the second position

                # Add the container number to each row
                columns.insert(2, f"C{container}") # Insert C# to third position

                # Add Environmnetal Temp to the row
                columns.insert(3, "") # For getting weather


                all_results.append(columns)
        
        else:
            all_results.append([f"No results returned for C{container}", "", "", "", "", ""])

    # Increment the container number as counter
    container += 1

# Convert the results into a pnadas Dataframe
df = pd.DataFrame(all_results, columns=["Date","Night/Day", "Container",  "环境温度", "T2", "T1", "TempDifference", "P4", "P5"])

# Reorder columns to match the desired order
df = df[["Date", "Night/Day", "Container", "环境温度", "T2", "T1", "TempDifference", "P4", "P5"]]

# Ensure the openpyxl engine is specified when saving the Excel file
try:
    # Write the results into a pandas DataFrame
    df.to_excel(output_file_name, index=False, engine='openpyxl')

    # End script
    print(f"Query results saved to {output_file_name}")
except ValueError as e:
    print(f"Error savinf Excel file: {e}")
