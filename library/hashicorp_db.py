#!/usr/bin/python
import os
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

class Database(object):
    def __init__(self, module, vault_token):
        self.module          = module
        self.vault_user_pass = module.params['vault_user_pass']
        self.database_host   = module.params['database_host']
        self.vault_plugin    = module.params['vault_plugin']
        self.short_code      = module.params['short_code']
        self.vault_user      = module.params['vault_user']
        self.api_url         = module.params['api_url']
        self.colo            = module.params['colo']
        self.env             = module.params['env']
        self.vault_token     = vault_token

        self.db_uri          = "{0}/v1/database/config/{1}_{2}".format(self.api_url, self.short_code, self.env)
        self.role_uri        = "{0}/v1/database/roles/readonly-{1}-{2}".format(self.api_url, self.env, self.short_code)
        self.headers         = {
                                  'X-Vault-Token': self.vault_token, 
                                  'Content-Type': 'application/json' 
                               }

    def configure_payload(self):
        payload = {
            "plugin_name": self.vault_plugin,
            "connection_url": "{{username}}:{{password}}@tcp(" + self.database_host + ".:3306)/",
            "allowed_roles": "readonly-" + self.env + "-" + self.short_code + ",db-readonly",
            "username": self.vault_user,
            "password": self.vault_user_pass
        }
        return payload

    def configuration_exists(self, payload):
        # check if zone exitst
        resp, info = fetch_url(
                self.module,
                self.db_uri,
                method='GET',
                headers=self.headers)

        if 200 <= info['status'] <= 300:
            return True
        else:
            return False

    def configure_new_db(self, payload):
        resp, info = fetch_url(
                self.module,
                url=self.db_uri,
                headers=self.headers,
                data=json.dumps(payload),
                method='POST',
                )
        return info

    def db_role_payload(self):
        payload = {
                    "db_name": self.short_code + "_" + self.env,
                    "creation_statements": ["CREATE USER '{{name}}'@'10.%%' IDENTIFIED BY '{{password}}'; GRANT SELECT ON " + self.short_code + "_" + self.env + ".* TO '{{name}}'@'10.%%';"],
                    "default_ttl": "1h",
                    "max_ttl": "24h"
                  }
        return payload

    def configure_role(self, payload):
        resp, info = fetch_url(
                self.module,
                method='POST',
                url=self.role_uri,
                headers=self.headers,
                data=json.dumps(payload),
                )
        return info

def main():

    try:
        arguments = dict(
            vault_user_pass=dict(required=True, type='str', no_log=True),
            vault_plugin=dict(required=True, type='str'),
            vault_user=dict(required=True, type='str'),
            database_host=dict(required=True, type='str'),
            short_code=dict(required=True, type='str'),
            colo=dict(required=True, type='str'),
            env=dict(required=True, type='str'),
            api_url=dict(required=True, type='str'),
        )
    except TypeError as e:
        arguments = dict(errors="{0}".format(e))

    if 'errors' not in arguments:
        module = AnsibleModule(
            argument_spec=arguments,
            supports_check_mode=False
        )

        # Vault token set up as env var from inital roleId login 
        vault_token = os.getenv('VAULT_TOKEN')
        db          = Database(module, vault_token)
        db_config   = db.configure_payload()
        exists      = db.configuration_exists(db_config)

        if exists == False:
            db_payload   = db.configure_new_db(db_config)
            role_payload = db.db_role_payload()
            payload      = db.configure_role(role_payload)
        else:
            payload = dict(
                        config_status='Configuration exists'
                      )
    else:
        payload = arguments

    module.exit_json(**payload)

if __name__ == '__main__':
    main()
