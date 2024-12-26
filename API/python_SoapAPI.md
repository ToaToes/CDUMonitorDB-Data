# Option 1: Using requests Library
The requests library is commonly used for making HTTP requests. To interact with a SOAP API, you need to send a POST request with the SOAP XML payload as the body. Here’s how you can do it:

Install requests library (if you haven't already):
```
pip install requests
```
Python Code to call the SOAP API:
```
import requests
```

### Define the SOAP endpoint
```
url = "http://10.1.7.159:8001/DataService.asmx/GetData"
```

### SOAP request body (change this according to the API documentation)
```
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
```

### Send the POST request with the SOAP XML payload
```
response = requests.post(url, data=soap_body, headers=headers)
```

### Check the response status and content
```
if response.status_code == 200:
    print("Response received:")
    print(response.text)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```
Key Points:
SOAP Envelope: The request body must include the SOAP XML envelope, which is required by most SOAP services. The envelope typically contains the header and body with the actual request.
SOAPAction Header: The SOAPAction header identifies the action being invoked on the SOAP service. This should be specified in the service’s documentation. If the API doesn’t require a SOAPAction header, you can omit it, but most services do.




# Option 2: Using zeep Library (Python SOAP Client)
The zeep library is a modern and easy-to-use SOAP client for Python. It provides a more structured approach to interact with SOAP services.

Install zeep library (if you haven’t installed it yet):
```
pip install zeep
```
Python Code to call the SOAP API using zeep:
```
from zeep import Client
```

### Define the WSDL URL
```
wsdl = "http://10.1.7.159:8001/DataService.asmx?wsdl"
```

### Create a zeep Client instance
```
client = Client(wsdl)
```

### Call the SOAP method (replace 'GetData' with the actual method in the WSDL)
```
try:
    response = client.service.GetData()
    print("Response received:")
    print(response)
except Exception as e:
    print(f"Error: {e}")

```
    
## Key Points for zeep:
WSDL (Web Service Definition Language): SOAP services usually provide a WSDL that describes the available methods and their parameters. In this case, we’re assuming that http://10.1.7.159:8001/DataService.asmx?wsdl is the WSDL endpoint for your SOAP service.
Automatic Parsing: zeep automatically handles the SOAP request and response parsing, which makes it easier to work with SOAP services than manually creating the XML requests.

### Understanding SOAP with zeep:
WSDL: A WSDL (Web Service Definition Language) file is an XML document that defines the operations and parameters that can be invoked on the SOAP service. By passing the WSDL URL to zeep, it allows you to easily interact with the SOAP service using a Python object-oriented interface.
Service Method Invocation: Once you create a zeep client, you can call the service methods directly using client.service.MethodName(). The arguments passed to the method will be automatically converted into the required XML format for the SOAP request.

### Which Approach Should You Use?
If you prefer simplicity and manual control over the SOAP request and response, use the requests library.
If you want a more automated and object-oriented way to interact with the SOAP service, use the zeep library. It is especially useful if the service has a WSDL.

### Troubleshooting:
Check SOAPAction Header: Some SOAP APIs require specific SOAPAction headers. Make sure you get the correct value from the service documentation.
WSDL Availability: If the service does not expose a WSDL at http://10.1.7.159:8001/DataService.asmx?wsdl, the zeep method will fail. In that case, you may need to manually construct the SOAP request (as in the requests example).
Check Response: The response might be in XML format, and you will need to parse it accordingly. If you’re using requests, you can use libraries like xml.etree.ElementTree or lxml to process the XML response.

## Conclusion:
If the service exposes a WSDL, using zeep is a convenient and structured way to interact with SOAP APIs.
If you're handling raw SOAP requests, requests will give you full control, though it requires manually creating the XML request.
