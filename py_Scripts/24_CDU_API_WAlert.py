# Every (hour) generate result to one Excel report
# Send Alert for exceeding threshold to WhatsAPP for Alert
# No need for SSH or Password authentication
#
# Author: Tom Chen

import requests
import json
import re
from xml.etree import ElementTree

import pandas as pd # Import pandas for Excel support
from datetime import datetime # Import datetime for current date and time

import time
from datetime import datetime
import socket #Timeout Exception
import gc # For garbage collection
import os
import psutil # For checking memory usage
import pywhatkit # For sending WhatsApp messages

# Change Language Input
import win32api
import win32con

### [Variables to configure the script]
###
###
### [result write to ONE Excel file]
result_Excel_Path = r'C:\Users\lucca\Desktop\API_C_Result.xlsx'

### [Container Number Shown]
container = 1

### [Initialize empty list to hold the results, write to Excel file]
all_results = []

### [Define the Number]
phone_number = "+14378781006"  # Replace with your phone number
groupID = "HgJMTs9Kw9MLU1NHETjd3B"  # Replace with your group ID

### [Boundary Values class to store the upper and lower limits for each parameter]
###
###
class BoundaryValues:
    def __init__(self, T2_upper, T2_lower, T1_upper, TempDifference_upper, P5_upper):   # Remove P4_upper, P4_lower
        self.T2_upper = T2_upper
        self.T2_lower = T2_lower
        self.T1_upper = T1_upper
        self.TempDifference_upper = TempDifference_upper
        # self.P4_upper = P4_upper
        # self.P4_lower = P4_lower
        self.P5_upper = P5_upper
# Create an instance of the BoundaryValues class with the desired limits
boundVal = BoundaryValues(
    T2_lower=22.0, # Lower limit for T2
    T2_upper=35.0, # Upper limit for T2
    T1_upper=50.0, # Upper limit for T1
    TempDifference_upper=15.0, # Upper limit for temperature difference
    # P4_lower=0.8, # Lower limit for P4
    # P4_upper=1.5, # Upper limit for P4
    P5_upper=3.5  # Upper limit for P5
)

### [Get the current timestamp in a desired format]
###
###
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Example: 20241220_153045
# Generate the file name with the timestamp
# output_file_name  = f"S_{current_timestamp}.xlsx"


### [Variables to configure the script]
###
###
# Time interval in seconds to wait between each query (5 min = 300 seconds) (10 min = 600 seconds)
interval = 600
# Time interval in seconds for generating Excel reports every hour
excel_interval = 600 * 6


### [Variables to track time for garbage collection]
###
###
# Start time of the script # Start time for Excel report generation
s_start = time.time()
start_time = s_start  
excel_time = s_start
gc_interval = 48 * 60 * 60  # Garbage collection interval in seconds: 48 hours


### [List of CDU API to connect to (add more as needed)]
###
###
url_container = [
"http://10.1.7.159:8600/DataService.asmx",
"http://10.2.7.252:8600/DataService.asmx",
"http://10.3.7.252:8600/DataService.asmx",
"http://10.4.7.252:8600/DataService.asmx",
"http://10.5.7.252:8600/DataService.asmx",
"http://10.6.7.252:8600/DataService.asmx",
"http://10.7.7.252:8600/DataService.asmx",
"http://10.8.7.252:8600/DataService.asmx",
"http://10.9.7.252:8600/DataService.asmx",
"http://10.10.7.253:8600/DataService.asmx",
"http://10.11.7.252:8600/DataService.asmx",
"http://10.12.7.252:8600/DataService.asmx",
"http://10.13.7.253:8600/DataService.asmx",
"http://10.14.7.252:8600/DataService.asmx",
"http://10.15.7.253:8600/DataService.asmx",
"http://10.16.7.253:8600/DataService.asmx",
"http://10.17.7.253:8600/DataService.asmx",
"http://10.18.7.253:8600/DataService.asmx",
"http://10.19.7.253:8600/DataService.asmx",
"http://10.20.7.253:8600/DataService.asmx",
"http://10.21.7.253:8600/DataService.asmx"
]


### [SOAP request body]
###
###
soap_request = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetData xmlns="http://tempuri.org/" />
  </soap:Body>
</soap:Envelope>"""

# URL of the SOAP API endpoint
# url = "http://10.11.7.252:8600/DataService.asmx"

# Headers including the SOAPAction
headers = {
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": "http://tempuri.org/GetData",
}


### [Function Define]
###
###
# Function to check memory usage and trigger garbage collection
def memory_garbageCollection(start_time, gc_interval):
    #process = psutil.Process(os.getpid())
    #memory_info = process.memory_info()
    ### print(f"Memory usage before GC: {memory_info.rss / 1024 ** 2:.2f} MB")

    elapsed_time = time.time() - start_time
    if elapsed_time > gc_interval:  
        print("48 hours have passed. Triggering garbage collection.")
        # gc.collect()  # Perform garbage collection
        os.system('clear')  # clear terminal buffer
        start_time = time.time()  # Reset the timer after garbage collection

    # Check memory usage after GC
    #memory_info = process.memory_info() 
    ### print(f"Memory usage after GC: {memory_info.rss / 1024 ** 2:.2f} MB")


# Alert the Data
def alert_Data(col, boundVal):   #col[2, 4, 5, 6, 7, 8, 9] ->Container#, T2, T1, T2-T1, P4, P5, pump
    # T2 Alert -> col[4]
    if float(col[4]) >= boundVal.T2_upper or float(col[4]) <= boundVal.T2_lower:
        message = f"[{col[2]} Alert]:\nTemperature T2 is out of range: {col[4]}°C\nT1: {col[5]}°C,\nT2: {col[4]}°C,\nP4: {col[7]},\nP5: {col[8]}"
        # print("[T2] Temperature exceeds limit. Sending an alert...")
        # Send an email, SMS, or perform any other action to alert the team
        # Sending the WhatsApp Message
        pywhatkit.sendwhatmsg_to_group_instantly(groupID, message)
        # Displaying a Success Message
        print("WhatsApp message sent!")

    # T1 Alert -> col[5]
    if float(col[5]) >= boundVal.T1_upper:
        message = f"[{col[2]} Alert]:\nTemperature T1 is too high: {col[5]}°C\nT1: {col[5]}°C,\nT2: {col[4]}°C,\nP4: {col[7]},\nP5: {col[8]}"
        # print("[T2] Temperature is too high. Sending an alert...")
        # Send an email, SMS, or perform any other action to alert the team
        # Sending the WhatsApp Message
        pywhatkit.sendwhatmsg_to_group_instantly(groupID, message)
        # Displaying a Success Message
        print("WhatsApp message sent!")

    # T2-T1 Alert -> col[6]
    if float(col[6]) >= boundVal.TempDifference_upper:
        message = f"[{col[2]} Alert]:\nTemperature difference is too high: {col[6]}°C\nT1: {col[5]}°C,\nT2: {col[4]}°C,\nP4: {col[7]},\nP5: {col[8]}"
        # print("Temperature difference is too high. Sending an alert...")
        # Send an email, SMS, or perform any other action to alert the team
        # Sending the WhatsApp Message
        pywhatkit.sendwhatmsg_to_group_instantly(groupID, message)
        # Displaying a Success Message
        print("WhatsApp message sent!")

    # P4 Alert -> col[7]
    # if float(col[7]) >= boundVal.P4_upper or float(col[7]) <= boundVal.P4_lower:
        # message = f"[{col[2]} Alert]:\nPressure P4 is out of range: {col[7]}\nT1: {col[5]}°C,\nT2: {col[4]}°C,\nP4: {col[7]},\nP5: {col[8]}"
        ### print("[P4] Pressure exceeds limit. Sending an alert...")
        ### Send an email, SMS, or perform any other action to alert the team
        ### Sending the WhatsApp Message
        # pywhatkit.sendwhatmsg_to_group_instantly(groupID, message)
        ### Displaying a Success Message
        # print("WhatsApp message sent!")

    # P5 Alert -> col[8]
    if float(col[8]) >= boundVal.P5_upper:
        message = f"[{col[2]} Alert]:\n Pressure P5 is too high: {col[8]}\nT1: {col[5]}°C,\nT2: {col[4]}°C,\nP4: {col[7]},\nP5: {col[8]}"
        # print("[P5] Pressure is too high. Sending an alert...")
        # Send an email, SMS, or perform any other action to alert the team
        # Sending the WhatsApp Message
        pywhatkit.sendwhatmsg_to_group_instantly(groupID, message)
        # Displaying a Success Message
        print("WhatsApp message sent!")

    # Close the browser for selenium


# Function to process the response
def process_response(response, container):

    # To handle time slot when data is not available
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datetime_NA = datetime.strptime(datetime_now, '%Y-%m-%d %H:%M:%S')
    day_night = "Day" if 8 <= datetime_NA.hour < 20 else "Night"

    if response.status_code == 200:
        try:
            # Parse the XML response
            root = ElementTree.fromstring(response.content)

            # Define the namespace to search within the response
            namespace = {"soap": "http://schemas.xmlsoap.org/soap/envelope/", "tempuri": "http://tempuri.org/"}
    
            # Exract the GetDataResult element which contains the data
            get_data_result = root.find(".//tempuri:GetDataResponse/tempuri:GetDataResult", namespace)


            if get_data_result is not None:
                columns = [''] * 10

                # Get the data content (string or key-value data)
                data = get_data_result.text.strip()

                # Split the data using '&&&' to get the date time from the JSON data
                datetime_str = data.split("&&&")[0].strip()    # get the first part before &&& for the time
                datetime_obj = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M:%S')
                

                ####
                day_night = "Day" if 8 <= datetime_obj.hour < 20 else "Night"    # Day from 8:00 - 20:00
                ####
                print(f"{datetime_str}")

                ####
                # columns.insert(0, datetime_str) # insert date
                columns[0] = datetime_str
                # columns.insert(1, day_night) # insert day/night
                columns[1] = day_night
                # columns.insert(2, f"C{container}") # insert container #
                columns[2] = f"C{container}"
                # columns.insert(3, "") # to add temperature
                

                # split the data using '&&&' this separates it into a JSON string
                data_json_str = data.split("&&&")[1]

                # Clean the JSON string by removing invalid characters like control characters
                cleaned_data_json_str = re.sub(r'[\x00-\x1F\x7F]', '', data_json_str)  # Remove control characters

                try:
                    # Parse the JSON data
                    data_json = json.loads(cleaned_data_json_str)

                    # Now filter for the key
                    for item in data_json:
                        # print(item)
                        #if item.get("Key") == "P3Temp":
                        #    print(f"Temp: {item['ValueShow']}")
                        #    columns.insert(3, item['ValueShow']) # to add temperature
                        if item.get("Key") == "P5T1":
                            # print(f"T1: {item['ValueShow']}")
                            T1 = float(re.sub(r'[^\d.]+', '', item['ValueShow']))
                            # columns.insert(5, T1)
                            columns[5] = str(T1)
                        if item.get("Key") == "P5T2":
                            # print(f"T2: {item['ValueShow']}")
                            T2 = float(re.sub(r'[^\d.]+', '', item['ValueShow']))
                            # columns.insert(4, T2)
                            columns[4] = str(T2)

                            # To convert the decimal nums
                            differ = f"{T1-T2: .2f}"
                            # print(f"Temprature Difference is {differ}")
                            # columns.insert(6, differ)
                            columns[6] = str(differ)

                        if item.get("Key") == "P5P4":
                            # print(f"P4: {item['ValueShow']}")
                            P4 = float(re.sub(r'[^\d.]+', '', item['ValueShow']))
                            # columns.insert(7, P4)
                            columns[7] = P4
                        if item.get("Key") == "P5P5":
                            # print(f"P5: {item['ValueShow']}")
                            P5 = float(re.sub(r'[^\d.]+', '', item['ValueShow']))
                            # columns.insert(8, P5)
                            columns[8] = P5

                        if item.get("Key") == "P5HZ1":
                            # print(f"Pump: {item['ValueShow']}\n")
                            pump = float(re.sub(r'[^\d.]+', '', item['ValueShow']))
                            # columns.insert(9, pump)
                            columns[9] = pump
                            break     # Founded, break

                    all_results.append(columns)

                    # Alert Function
                    alert_Data(columns, boundVal)
            
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

            else:
                all_results.append([datetime_now, day_night, f"C{container}", "", "", "", "", ""])
                print("No GetDataResult found in the response.")

        except Exception as e:
            all_results.append([datetime_now, day_night, f"C{container}", "", "", "", "", ""])
            print(f"Error processing response: {e}\n")
    else:
        print(f"Error: {response.status_code}")



### Main Logic
###
###
while True:

    # Send SOAP requests to each URL in the list
    for url in url_container:
        # print(f"Sending request to {url}")
        try:
            # Send the SOAP request
            response = requests.post(url, data=soap_request, headers=headers)

            # Process the response
            print(f"\n[C{container}]:")
            process_response(response, container)

        except requests.exceptions.RequestException as e:
            print(f"\nRequest to C{container} failed: {e}")
        container += 1

    # Re-define container number shown
    container = 1


    # every 1 hour, generate the result to one Excel report
    elapsed_excel_time = excel_time - time.time()
    if elapsed_excel_time > excel_interval or excel_time == start_time: # every 1 hour generate the Excel report || first time 

        # Convert the results into a pnadas Dataframe
        df = pd.DataFrame(all_results, columns=["Date","Night/Day", "Container",  "环境温度", "T2", "T1", "TempDifference", "P4", "P5", "Pump"])
        # Reorder columns to match the desired order
        df = df[["Date", "Night/Day", "Container", "环境温度", "T2", "T1", "TempDifference", "P4", "P5", "Pump"]]

        # Check if the file already exists
        if os.path.exists(result_Excel_Path):
            # If it exists, read the existing file and append new data
            try:
                # Read the existsing file
                existing_df = pd.read_excel(result_Excel_Path, engine = 'openpyxl')

                # Append the new data to the existing DataFrame
                updated_df = pd.concat([existing_df, df], ignore_index = True)

                # Write the updated DataFrame back to the Excel file
                updated_df.to_excel(result_Excel_Path, index = False, engine = 'openpyxl')

                print(f"Query results appended to {result_Excel_Path}")
        
            except Exception as e:
                print(f"Error reading or writing to the Excel file: {e}")

        else:
            # If the file doesnt exist, create a new one
            try:
                df.to_excel(result_Excel_Path, index = False, engine = 'openpyxl')
                print(f"Query results saved to {result_Excel_Path}")
            except Exception as e:
                print(f"Error saving the new Excel file: {e}")

        # Reset the timer for Excel report generation
        excel_time = time.time()



    # End of the script
    print("\n\n---------------------------------------------------\n\n")

    #!!! Check memory usage and trigger garbage collection
    memory_garbageCollection(start_time, gc_interval)

    # Sleep for the specified interval 5 min before running the script again
    time.sleep(interval)
