To have a persistent SSH connection, you can use a few different methods, 
depending on the context in which you need the connection to stay open. 
This is particularly useful when you need to maintain long-lived connections, 
avoid re-authentication, and reduce the overhead of reconnecting to the server.


## 1. Using ControlMaster and ControlPath in SSH Config
The most commonly used method for persistent SSH connections in the context of multiple SSH connections to the same server is the 
ControlMaster and ControlPath options in the SSH configuration. This allows you to reuse an existing connection, 
which is much more efficient than opening a new connection every time you run a command or interact with the server.


Edit Your SSH Config File: Open or create the ~/.ssh/config file on your local machine.
```
nano ~/.ssh/config
```
Add the Configuration for Persistent Connection: Add the following configuration to enable persistent connections for a specific host or for all hosts:
```
Host *
    ControlMaster auto
    ControlPath ~/.ssh/%r@%h:%p
    ControlPersist 10m
```
Explanation:

ControlMaster auto: Enables the master connection to be established automatically when needed.
ControlPath ~/.ssh/%r@%h:%p: Specifies the path to the control socket. The %r, %h, and %p placeholders refer to the SSH user, host, and port.
ControlPersist 10m: Specifies how long the master connection should stay open after the initial session ends (e.g., 10 minutes). If you don’t specify ControlPersist, 
the connection will remain open as long as there are any active sessions.
You can also apply the configuration to a specific host by changing Host * to the hostname or IP address of the remote server.

Use SSH Normally: Now, when you connect to the same server again within 10 minutes (or the configured time), the SSH connection will reuse the master connection, saving time and resources:
```
ssh username@hostname
```
Testing the Connection: You can run multiple SSH commands to check if the persistent connection works. 
The second (and subsequent) SSH commands should establish much faster because they are using the existing connection.
```
ssh username@hostname
```
Then run another SSH command:
```
ssh username@hostname
```
The second connection should be faster, as it reuses the connection established previously.

