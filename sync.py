# -*- coding: UTF-8 -*-
__author__ = 'arvin.zhou'

import requests
import json
import os
from constants import SHARE_PROJECT, QUERY_MODELS_GQL, MUTSTION_MODEL_GQL

def get_gql(gql_path):
    if os.path.exists(gql_path):    
        with open(gql_path, 'r') as file:
            content = file.read()
            file.close()
            return content
    else:
        raise Exception(f'gql file not found: {gql_path}')

def save_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
        file.close()

def get_models():
    payload = {
        "query": get_gql(QUERY_MODELS_GQL),
        'variables': {
            'projectId': SHARE_PROJECT['PROJECT_ID'],
            'environment': SHARE_PROJECT['ENVIRONMENT']
        }
    }
    headers = {"Authorization": f"Bearer {SHARE_PROJECT['TOKEN']}"}
    r = requests.post(SHARE_PROJECT['MANAGEMENT_URL'], json=payload, headers=headers).json()
    models = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('models')
    components = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('components')
    enumerations = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('enumerations')

    save_file(f'{os.path.dirname(__file__)}/_temp/models.json', json.dumps(models, indent=4))
    save_file(f'{os.path.dirname(__file__)}/_temp/components.json', json.dumps(components, indent=4))
    save_file(f'{os.path.dirname(__file__)}/_temp/enumerations.json', json.dumps(enumerations, indent=4))

def create_new_model():
    payload = { "query": get_gql(MUTSTION_MODEL_GQL) }
    headers = {"Authorization": f"Bearer {SHARE_PROJECT['TOKEN']}"}
    r = requests.post(SHARE_PROJECT['MANAGEMENT_URL'], json=payload, headers=headers).json()
    print(r)