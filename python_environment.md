https://medium.com/marvelous-mlops/the-rightway-to-install-python-on-a-mac-f3146d9d9a32



On Mac: hitting externally managed environment <br/>
https://discuss.python.org/t/on-macos-14-pip-install-throws-error-externally-managed-environment/50352/9

https://stackoverflow.com/questions/60309393/how-to-install-python-requests-on-macos

https://www.youtube.com/watch?v=JazffJZexzs


Have to create an virtual environment for the Python to run
```
python3 -m venv task

source task/bin/activate

pip install requests
pip install paramiko
......

deactivate

```
