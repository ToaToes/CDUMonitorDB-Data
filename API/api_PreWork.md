http://[服务器地址(Remote System IP Address)]:[Port]/DataService.asmx/GetData

## To Check the Port for SoapAPI

1. First to check every remote system Firewall Inbound Rule

ssh in to the remote system and perform:
```
netsh advfirewall firewall show rule name="CDU"
```
to check the inbound for get-data from CDU port


on PowerShell
```
Get-NetFirewallRule
```

### API CALL:
P5P1	压力P1	  299 <br/>
P5P2	压力P2	  301 <br/>
P5P3	压力P3	  303 <br/>
P5P4	压力P4	  305 <br/>
P5P5	压力P5	  307 <br/>
P5T1	温度T1	  328 <br/>
P5T2	温度T2	  330 <br/>
P5HZ1	变频器频率	318
<br/>
<img width="542" alt="image" src="https://github.com/user-attachments/assets/21c6a2ba-a6d3-46f7-84af-d876885170ff" />
