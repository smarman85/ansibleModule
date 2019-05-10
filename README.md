# ansibleModule
```
Quick little ansible module to configure new databases into hashicorp. This module assumes you already have hashicorp vault configured and set up to handle database configurations. The deploy user running this integration handles the authentication with Hashicorp Vault and sets the token as an environment variable. 
```

## Set up
```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip && pip initall -r reqs.txt
```

## Run/test
```
# local testing (variables changed to protect the innocent)
# work in progress

(venv) $ ansible-playbook testbook.yml -e "env=production colo=testcolo short_code=tst user=vaultDBUser pass='vaultDB_userPassword' dbhost=databasehost01.fqdn.com api='https://your_api_url.fqdn.com'"
 [WARNING]: Unable to parse /etc/ansible/hosts as an inventory source

 [WARNING]: No inventory was parsed, only implicit localhost is available

 [WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'


PLAY [test new module] ********************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************
ok: [localhost]

TASK [run the thing] **********************************************************************************************************************
ok: [localhost]

TASK [show info] **************************************************************************************************************************
ok: [localhost] => {
    "msg": {
        "cache-control": "no-store",
        "changed": false,
        "connection": "close",
        "content-type": "application/json",
        "cookies": {},
        "cookies_string": "",
        "date": "Fri, 10 May 2019 21:08:20 GMT",
        "failed": false,
        "msg": "OK (unknown bytes)",
        "status": 204,
        "url": "https://your_api_url.fqdn.com/v1/database/roles/readonly-production-tst"
    }
}

PLAY RECAP ********************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0

```
