# -*- coding: UTF-8 -*-
__author__ = 'arvin.zhou'

import requests
from constants import SHARE_PROJECT, QUERY_MODELS_GQL, MUTSTION_MODEL_GQL
from utils import get_gql
import time

def get_schema(projectId, environment, token, managementUrl):
    payload = {
        "query": get_gql(QUERY_MODELS_GQL),
        'variables': { 'projectId': projectId, 'environment': environment }
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(managementUrl, json=payload, headers=headers).json()
    models = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('models')
    components = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('components')
    enumerations = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('enumerations')

    return { 'models': models, 'components': components, 'enumerations': enumerations }

def get_env_id(projectId, environment, token, managementUrl):
    payload = { "query": '''
                    query environment ($projectId: ID!, $environment: String!) {
                        viewer {
                            project(id: $projectId) {
                                environment(name: $environment) { id }
                            }
                        }
                    }
                    ''',
               'variables': { 'projectId': projectId, 'environment': environment } }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(managementUrl, json=payload, headers=headers).json()
    return r.get('data').get('viewer').get('project').get('environment').get('id')

def create_model(
        environment_id,
        token,
        management_url,
        apiId,
        apiIdPlural,
        displayName
):
    payload = {
        "query": get_gql(MUTSTION_MODEL_GQL),
        'variables': {
            'environmentId': environment_id,
            'apiId': apiId,
            'apiIdPlural': apiIdPlural,
            'displayName': displayName
        }
    }
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(management_url, json=payload, headers=headers).json()

def create_component():
    payload = { "query": get_gql(MUTSTION_MODEL_GQL) }
    headers = {"Authorization": f"Bearer {SHARE_PROJECT['TOKEN']}"}
    r = requests.post(SHARE_PROJECT['MANAGEMENT_URL'], json=payload, headers=headers).json()
    print(r)

def create_field():
    payload = { "query": get_gql(MUTSTION_MODEL_GQL) }
    headers = {"Authorization": f"Bearer {SHARE_PROJECT['TOKEN']}"}
    r = requests.post(SHARE_PROJECT['MANAGEMENT_URL'], json=payload, headers=headers).json()
    print(r)

def start_sync(info):
    schema = get_schema(
        projectId = info['share']['PROJECT_ID'],
        environment = info['share']['ENVIRONMENT'],
        token = info['share']['TOKEN'],
        managementUrl = info['share']['MANAGEMENT_URL']
    )

    #share_name = info['share']['MODEL_NAME']

    environment_id = get_env_id(
        projectId = info['target']['PROJECT_ID'],
        environment = info['target']['ENVIRONMENT'],
        token = info['target']['TOKEN'],
        managementUrl = info['target']['MANAGEMENT_URL']
    )

    print(info['target']['PROJECT_ID'])
    print(environment_id)

    for model in schema['models']:
        time.sleep(3)
        create_model_reslut = create_model(
            environment_id = environment_id,
            token = info['target']['TOKEN'],
            management_url = info['target']['MANAGEMENT_URL'],
            apiId = model['apiId'],
            apiIdPlural = model['apiIdPlural'],
            displayName = model['displayName']
        )
        print(create_model_reslut)
        # for field in model['fields']:
        #     if(not(field['isSystem'])):
        #         print(field['displayName'])