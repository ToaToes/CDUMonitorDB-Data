# Author: Tom Chen

import paramiko
from paramiko.ssh_exception import SSHException, NoValidConnectionsError  # Import the correct SSHException
import time

import socket #Timeout Exception

# Function to execute an SQLite query remotely via SSH
def execute_sqlite_query(host, port, username, password, db_path, query, timeout=30):
    container = 1

    try:
        # Create an SSH client instance
        ssh = paramiko.SSHClient()
        # Automatically add the SSH key to the known hosts (this may be insecure for production)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the remote host
        print(f"Connecting to {host}...")
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

# List of Windows machines to connect to (add more as needed)
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

# SQL query to execute (Modify with your actual query)
query = "Select DateTime1, T1, T2, (T1-T2) As TempDifference, P4, P5 from Record ORDER BY DateTime1 DESC LIMIT 1;"  # Change as needed

# Loop over the list of hosts and execute the SQLite query on each one
for host_info in hosts:
    host = host_info["host"]
    port = host_info["port"]
    username = host_info["username"]
    password = host_info["password"]
    db_path = host_info["db_path"]
    
    # Execute SQLite query on each machine
    print(f"\nExecuting query on {host}...")
    output = execute_sqlite_query(host, port, username, password, db_path, query)
    
    # Optionally, you can handle output here, e.g., save it to a file
    if output:
        print(f"Query result from {host}:")
        print("Date               | T1 | T2 | Diff | P4 | P5")
        print(output)
