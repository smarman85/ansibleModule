#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

class Database(object):
    def __init__(self, module):
        self.module = module
        self.vault_user_pass = module.params['vault_user_pass']
        self.database_host   = module.params['database_host']
        self.short_code      = module.params['short_code']
        self.vault_user      = module.params['vault_user']
        self.colo            = module.params['colo']
        self.env             = module.params['env']

    def return_info(self):
        payload = {
            "plugin_name": "mysql-database-plugin",
            "connection_url": "{{username}}:{{password}}@tcp(" + self.database_host + ".:3306)/",
            "allowed_roles": "readonly-" + self.env + "-" + self.short_code + ",db-readonly",
            "username": self.vault_user,
            "password": self.vault_user_pass
        }
        #print(payload)
        return payload

def main():

    arguments = dict(
        vault_user_pass=dict(required=True, type='str', no_log=True),
        vault_user=dict(required=True, type='str'),
        database_host=dict(required=True, type='str'),
        short_code=dict(required=True, type='str'),
        colo=dict(required=True, type='str'),
        env=dict(required=True, type='str'),
    )

    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=True
    )

    db = Database(module)
    payload = db.return_info()

    module.exit_json(**payload)

if __name__ == '__main__':
    main()
