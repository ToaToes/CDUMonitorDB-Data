Verify Active Network Adapter:

You may have multiple network adapters (e.g., Wi-Fi, Ethernet, virtual adapters). The IP address displayed in ipconfig might belong to a different adapter.
To confirm:
powershell
Copy code
Get-NetIPAddress
This will show all active network interfaces and their IP addresses.


Change IP Address:
Open Network Connection and open the property of the tartget network, mannually change the ip address


Creating the config file in .ssh (on Windows) <\br>
https://stackoverflow.com/questions/45446285/creating-new-file-through-windows-powershell
```
New-Item config

notepad config

type config
```


solve sshd SHA problem:
https://unix.stackexchange.com/questions/340844/how-to-enable-diffie-hellman-group1-sha1-key-exchange-on-debian-8-0


