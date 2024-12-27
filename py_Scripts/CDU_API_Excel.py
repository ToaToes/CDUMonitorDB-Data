# Author: Tom Chen

import requests
import json
import re
from xml.etree import ElementTree

import pandas as pd # Import pandas for Excel support
from datetime import datetime # Import datetime for current date and time


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


# Get the current timestamp in a desired format
current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Example: 20241220_153045
# Generate the file name with the timestamp
output_file_name  = f"S_{current_timestamp}.xlsx"



# Initialize empty list to hold the results
all_results = []


# SOAP request body
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
                columns = []

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
                columns.insert(0, datetime_str) # insert date
                columns.insert(1, day_night) # insert day/night
                columns.insert(2, f"C{container}") # insert container #
                columns.insert(3, "") # to add temperature

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
                        if item.get("Key") == "P5P4":
                            print(f"P4: {item['ValueShow']}")
                            columns.insert(7, item['ValueShow'])
                        if item.get("Key") == "P5P5":
                            print(f"P5: {item['ValueShow']}")
                            columns.insert(8, item['ValueShow'])

                        if item.get("Key") == "P5T1":
                            print(f"T1: {item['ValueShow']}")
                            T1 = float(re.sub(r'[^\d.]+', '', item['ValueShow']))
                            columns.insert(5, T1)
                        if item.get("Key") == "P5T2":
                            print(f"T2: {item['ValueShow']}")
                            T2 = float(re.sub(r'[^\d.]+', '', item['ValueShow']))
                            columns.insert(4, T2)

                            # To convert the decimal nums
                            differ = f"{T1-T2: .2f}"
                            print(f"Temprature Difference is {differ}")
                            columns.insert(6, differ)


                        if item.get("Key") == "P5HZ1":
                            print(f"Pump: {item['ValueShow']}\n")
                            columns.insert(9, item['ValueShow'])
                            break     # Founded, break

                    all_results.append(columns)
            
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


# Send SOAP requests to each URL in the list
container = 1
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


# Convert the results into a pnadas Dataframe
df = pd.DataFrame(all_results, columns=["Date","Night/Day", "Container",  "环境温度", "T2", "T1", "TempDifference", "P4", "P5", "Pump"])

# Reorder columns to match the desired order
df = df[["Date", "Night/Day", "Container", "环境温度", "T2", "T1", "TempDifference", "P4", "P5", "Pump"]]

# Ensure the openpyxl engine is specified when saving the Excel file
try:
    # Write the results into a pandas DataFrame
    df.to_excel(output_file_name, index=False, engine='openpyxl')

    # End script
    print(f"Query results saved to {output_file_name}")
except ValueError as e:
    print(f"Error savinf Excel file: {e}")

