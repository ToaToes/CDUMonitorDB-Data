1. download pyton latest version -> https://learn.microsoft.com/en-us/windows/python/beginners
2. ```pip install paramiko``` in powershell for multiple ssh connection
3. cd to the script file
4. run ```python ssh.py``` to get the data

Install:
```
pip install paramiko
```
Error : No module named 'psutil'
```
pip install --upgrade psutil
```
Error : No module named 'psutil'
```
pip install pywhatkit
```


For problem like pywhatkit opens new tab on browser: <br/>
https://stackoverflow.com/questions/63741960/use-pywhatkkit-in-same-tab-instead-of-using-new <br/>
https://pypi.org/project/pywhatkit/


https://docs.python.org/3/library/webbrowser.html#webbrowser.controller.open
```
controller.open(url, new=0, autoraise=True)
Display url using the browser handled by this controller. If new is 1, a new browser window is opened if possible. If new is 2, a new browser page (“tab”) is opened if possible.
```
