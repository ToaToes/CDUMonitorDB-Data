Verify Active Network Adapter:

You may have multiple network adapters (e.g., Wi-Fi, Ethernet, virtual adapters). The IP address displayed in ipconfig might belong to a different adapter.
To confirm:
powershell
Copy code
Get-NetIPAddress
This will show all active network interfaces and their IP addresses.


--------

Change IP Address:
Open Network Connection and open the property of the tartget network, mannually change the ip address


--------

Creating the config file in .ssh (on Windows) <\br>
https://stackoverflow.com/questions/45446285/creating-new-file-through-windows-powershell
```
New-Item config

notepad config

type config
```


solve sshd SHA problem:
https://unix.stackexchange.com/questions/340844/how-to-enable-diffie-hellman-group1-sha1-key-exchange-on-debian-8-0


--------
To show all ip address listing, and to find out the ***preferred*** and ***duplicate*** ip AddressState


IPAddress         : 169.254.241.18
InterfaceIndex    : 12
InterfaceAlias    : 以太网 2
AddressFamily     : IPv4
Type              : Unicast
PrefixLength      : 16
PrefixOrigin      : WellKnown
SuffixOrigin      : Link
AddressState      : Preferred  <-
ValidLifetime     : Infinite ([TimeSpan]::MaxValue)
PreferredLifetime : Infinite ([TimeSpan]::MaxValue)
SkipAsSource      : False
PolicyStore       : ActiveStore

IPAddress         : 10.3.7.253
InterfaceIndex    : 12
InterfaceAlias    : 以太网 2
AddressFamily     : IPv4
Type              : Unicast
PrefixLength      : 24
PrefixOrigin      : Manual
SuffixOrigin      : Manual
AddressState      : Duplicate  <-
ValidLifetime     : Infinite ([TimeSpan]::MaxValue)
PreferredLifetime : Infinite ([TimeSpan]::MaxValue)
SkipAsSource      : False
PolicyStore       : ActiveStore

```
Set-NetIPAddress -IPAddress 10.3.7.253 -InterfaceAlias "以太网 2" -PreferredLifetime Infinite -SkipAsSource $false
```

https://superuser.com/questions/1097057/what-does-preferred-tentative-and-duplicate-mean-against-an-ipv4-address


Verify Configuration
Run the following command again to confirm the changes:
```
Get-NetIPAddress -InterfaceAlias "以太网 2"
```


1. Verify Existing IP Addresses
Run the following command to list all IP addresses associated with your network interfaces:

```
Get-NetIPAddress
```
Look for the adapter named 以太网 2 and ensure 10.3.7.253 is listed. If not, you will need to add it.
2. Verify the Network Interface Name
The interface alias may be slightly different (e.g., 以太网 2 vs 以太网2). Use this command to list all network interfaces:

```
Get-NetAdapter
```
Ensure the correct name of the network interface is used in the -InterfaceAlias parameter.


Set the IP Address as Preferred
Open PowerShell as Administrator.
Run the following command to set the preferred IP address:
```
Set-NetIPAddress -IPAddress 10.3.7.253 -InterfaceAlias "以太网 2" -PreferredLifetime Infinite -SkipAsSource $false
```
This command ensures that 10.3.7.253 is used as the preferred source address for outgoing traffic.



Remove Duplicate State
If the Duplicate state persists, it usually indicates a conflict. Resolve it by ensuring no other device on the network uses 10.3.7.253.

Run a ping test:
```
ping 10.3.7.253
```
If there’s a response, identify the conflicting device using:
```
arp -a
```
Log in to your router or the conflicting device and change its IP.
