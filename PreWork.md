## SQLITE 3 Setup
1. Remote Windows, Download sqlite3 file:
```https://www.sqlite.org/download.html```
choose sqlite-tools-win-x64-3470200.zip
2. Create new file in Program Files, name as "sqlite"
3. Extract the download sqlite file to the new create file
4. Follow the instruction, from Adding path for sqlite binary to the rest 
```https://dev.to/dendihandian/installing-sqlite3-in-windows-44eb```


## SSH Setup
1. 设置 -> 应用 -> 可选功能 -> 搜索SSH并下载
```
Start-Service sshd

Set-Service -Name sshd -StartupType 'Automatic'
```
```
help
Open PowerShell as an administrator 2. Stop the OpenSSH server by running Stop-Service sshd 3. Verify that the service has stopped by running Get-Service sshd 4. Start the OpenSSH server again with Start-Service sshd 5. Confirm that the service is running by re-running Get-Service sshd
```


2. Open PowerShell type:
``` ip config```
write down the 10.xxx ip address on sheet
3. set Adminastrator Password
```net user Administrator admin``` set password as admin

Test SSH connection on monitor system to the remote system, mark the sheets

``` ssh Administrator@[ip address]```
type in password


### For Persisten SSH conneciton
useful when you need to maintain long-lived connections, avoid re-authentication, and reduce the overhead of reconnecting to the server.

4. in .ssh file, create a config file for master ssh, to store the hosts
-> OR download the config file and move to the .ssh file
   
Mac:
```
nano config
```
Windows:
```
notepad config
```


### When Restarting system, since ssh sets the passwords of the remote system, an there is no keyboard
1. ssh to the remote system
2. ```net user Administrator ""``` set the password to empty
3. when remote system log in to see CDU Monitor
4. set the password back to "admin"
5. ssh and ```net user Administrator admin```
