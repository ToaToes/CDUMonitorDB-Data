# Option 1: Using requests Library
The requests library is commonly used for making HTTP requests. To interact with a SOAP API, you need to send a POST request with the SOAP XML payload as the body. Here’s how you can do it:

Install requests library (if you haven't already):
pip install requests
Python Code to call the SOAP API:
import requests

### Define the SOAP endpoint
url = "http://10.1.7.159:8001/DataService.asmx/GetData"

### SOAP request body (change this according to the API documentation)
soap_body = '''<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://www.example.com/webservice">
   <soapenv:Header/>
   <soapenv:Body>
      <web:GetData>
         <!-- Add your parameters here -->
      </web:GetData>
   </soapenv:Body>
</soapenv:Envelope>'''

# Set the headers for SOAP request
headers = {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': 'http://www.example.com/webservice/GetData'  # Change the SOAPAction if needed
}

# Send the POST request with the SOAP XML payload
response = requests.post(url, data=soap_body, headers=headers)

# Check the response status and content
if response.status_code == 200:
    print("Response received:")
    print(response.text)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
Key Points:
SOAP Envelope: The request body must include the SOAP XML envelope, which is required by most SOAP services. The envelope typically contains the header and body with the actual request.
SOAPAction Header: The SOAPAction header identifies the action being invoked on the SOAP service. This should be specified in the service’s documentation. If the API doesn’t require a SOAPAction header, you can omit it, but most services do.
