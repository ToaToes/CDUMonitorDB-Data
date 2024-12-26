# Author: Tom Chen

import requests
import json
import re
from xml.etree import ElementTree


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
url = "http://10.11.7.252:8600/DataService.asmx"

# Headers including the SOAPAction
headers = {
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": "http://tempuri.org/GetData",
}

# Send the SOAP request
response = requests.post(url, data=soap_request, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the XML response
    root = ElementTree.fromstring(response.content)

    # Extract the GetDataResult element
    namespace = {"soap": "http://schemas.xmlsoap.org/soap/envelope/", "tempuri": "http://tempuri.org/"}
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

                    differ = f"{T1-T2: .2f}"
                    print(f"Temprature Difference is {differ}")


                if item.get("Key") == "P5HZ1":
                    print(f"Pump: {item['ValueShow']}")


                    break     # Founded, break
            
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    else:
        print("No GetDataResult found in the response.")
else:
    print(f"Error: {response.status_code}")
