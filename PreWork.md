SQLITE 3 Setup
1. Remote Windows, Download sqlite3 file:
```https://www.sqlite.org/download.html```
choose sqlite-tools-win-x64-3470200.zip
2. Create new file in Program Files, name as "sqlite"
3. Extract the download sqlite file to the new create file
4. Follow the instruction, from Adding path for sqlite binary to the rest 
```https://dev.to/dendihandian/installing-sqlite3-in-windows-44eb```


SSH Setup
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
