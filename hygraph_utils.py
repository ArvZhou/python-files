import requests
import logging
from gqls.querys  import query_models_and_components_sql, query_model_fields_sql, get_model_by_api_id_sql, get_enumerations_sql
from gqls.mutations import create_model_gql, create_simple_field_gql, create_enumeration_gql, create_enumeration_field_gql
from utils import get_match_item

def get_models_and_components(projectId, environment, token, managementUrl):
    payload = {
        "query": query_models_and_components_sql,
        'variables': { 'projectId': projectId, 'environment': environment }
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(managementUrl, json=payload, headers=headers).json()

    if(r == None):
        logging.error('Get models and components failed!' + r)
    models = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('models')
    components = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('components')
    enumerations = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('enumerations')

    return { 'models': models, 'components': components, 'enumerations': enumerations }

def get_env_id_by_env_name(projectId, environment, token, managementUrl):
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
        "query": create_model_gql,
        'variables': {
            'data':
                {
                    'environmentId': environment_id,
                    'apiId': apiId,
                    'apiIdPlural': apiIdPlural,
                    'displayName': displayName
                }
        }
    }
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(management_url, json=payload, headers=headers).json()

def get_model_fields(
    projectId,
    environment,
    token,
    management_url,
    apiId,
):
    payload = {
        "query": query_model_fields_sql,
        'variables': {
            'projectId': projectId, 
            'environment': environment,
            'apiId': apiId,
        }
    }
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(management_url, json=payload, headers=headers).json()

def create_simple_field(
    token,
    management_url,
    variables
):
    payload = {
        "query": create_simple_field_gql,
        'variables': variables
    }
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(management_url, json=payload, headers=headers).json()

def get_model_by_api_id(
    token,
    management_url,
    variables
):
    payload = {
        "query": get_model_by_api_id_sql,
        'variables': variables
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(management_url, json=payload, headers=headers).json()

    print(r)

    return r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('model')

def create_enumeration(
    token,
    management_url,
    variables
):
    payload = {
        "query": create_enumeration_gql,
        'variables': variables
    }
    print(variables)
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(management_url, json=payload, headers=headers).json()

def create_enumeration_field(
    token,
    management_url,
    variables
):
    print(variables)
    payload = {
        "query": create_enumeration_field_gql,
        'variables': variables
    }
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(management_url, json=payload, headers=headers).json()

def get_enumeration_by_api_id(
    token,
    management_url,
    variables,
    apiId
):
    payload = {
        "query": get_enumerations_sql,
        'variables': variables
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(management_url, json=payload, headers=headers).json()

    if(r == None):
        logging.error('Get enumerations failed!' + r)

    enumerations = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('enumerations')

    return get_match_item(enumerations, apiId)