http://[服务器地址(Remote System IP Address)]:[Port]/DataService.asmx/GetData

## To Check the Port for SoapAPI

1. First to check every remote system Firewall Inbound Rule

ssh in to the remote system and perform:
```
netsh advfirewall firewall show rule name="CDU"
```
to check the inbound for get-data from CDU port
