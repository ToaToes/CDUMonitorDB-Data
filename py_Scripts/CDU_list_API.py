# Author: Tom Chen

import requests
import json
import re
from xml.etree import ElementTree


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
def process_response(response):
    if response.status_code == 200:
        try:
            # Parse the XML response
            root = ElementTree.fromstring(response.content)

            # Define the namespace to search within the response
            namespace = {"soap": "http://schemas.xmlsoap.org/soap/envelope/", "tempuri": "http://tempuri.org/"}
    
            # Exract the GetDataResult element which contains the data
            get_data_result = root.find(".//tempuri:GetDataResponse/tempuri:GetDataResult", namespace)

            if get_data_result is not None:
                # Get the data content (string or key-value data)
                data = get_data_result.text.strip()

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
                        if item.get("Key") == "P5P5":
                            print(f"P5: {item['ValueShow']}")

                        if item.get("Key") == "P5T1":
                            print(f"T1: {item['ValueShow']}")
                            T1 = float(re.sub(r'[^\d.]+', '', item['ValueShow']))
                        if item.get("Key") == "P5T2":
                            print(f"T2: {item['ValueShow']}")
                            T2 = float(re.sub(r'[^\d.]+', '', item['ValueShow']))

                            # To convert the decimal nums
                            differ = f"{T1-T2: .2f}"
                            print(f"Temprature Difference is {differ}")


                        if item.get("Key") == "P5HZ1":
                            print(f"Pump: {item['ValueShow']}\n")
                            break     # Founded, break
            
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

            else:
                print("No GetDataResult found in the response.")
        except Exception as e:
            print(f"Error processing response: {e}")
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
        process_response(response)

    except requests.exceptions.RequestException as e:
        print(f"\nRequest to C{container} failed: {e}")
    container += 1

