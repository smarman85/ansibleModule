# ansibleModule

## Set up
```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip && pip initall -r reqs.txt
```

## Run/test
```
(venv) $ ansible-playbook testbook.yml -e "colo=testcolo short_code=tst user=vaultDBUser pass='vaultDB_userPassword' dbhost=databasehost01.fqdn.com api='https://api_url.fqdn.com'"
```
