CDUMonitorDB Data retrive (terminal)

1. Windows: OpenSSH Client, OpenSSH Server
```
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH'

Start-Service sshd

Set-Service -Name sshd -StartupType 'Automatic'
```
automatically open ssh server when reboot


set ssh password for remote windows for first time (usually Administrator)
```
net user Administrator admin
```
means to set the password as admin


2. Install sqlite3 on both monitor system and remote system
3. check sqlite version, make sure sqlite already installed
4. Command Line + Sqlite statement: 
```
sqlite3 CDUMonitorDB.db "Select T1, T2, P4, P5, DateTime1 from Record ORDER BY DateTime1 DESC LIMIT 1;"
```
