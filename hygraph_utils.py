import requests
import logging
from gqls.querys  import query_models_and_components_sql, query_model_fields_sql, get_model_by_api_id_sql, get_enumerations_sql, get_components_sql
from gqls.mutations import create_model_gql, create_component_gql, create_simple_field_gql
from gqls.mutations import create_enumeration_gql, create_enumeration_field_gql, create_component_field_gql, create_component_union_field_gql
from utils import get_match_item

def get_models_and_components(projectId, environment, token, managementUrl):
    payload = {
        "query": query_models_and_components_sql,
        'variables': { 'projectId': projectId, 'environment': environment }
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(managementUrl, json=payload, headers=headers).json()

    if r.get('errors'):
        logging.error('Get models and components failed!' + str(r.get('errors')))
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
    if r.get('errors'):
        logging.error('Get environment error \n' + str(r.get('errors')))
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
    r = requests.post(management_url, json=payload, headers=headers).json()
    if r.get('errors'):
        logging.error('Create model error \n' + str(r.get('errors')))
    return r

def create_component(
        token,
        management_url,
        variables
):
    payload = {
        "query": create_component_gql,
        'variables': variables
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(management_url, json=payload, headers=headers).json()
    if r.get('errors'):
        logging.error('Create component error \n' + str(r.get('errors')))
    return r

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
    r = requests.post(management_url, json=payload, headers=headers).json()
    if r.get('errors'):
        logging.error('Get model fields error \n' + str(r.get('errors')))
    return r

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
    r = requests.post(management_url, json=payload, headers=headers).json()
    if r.get('errors'):
        logging.error('Create simple field error \n' + str(r.get('errors')))
    return r

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
    if r.get('errors'):
        logging.error('Get model error \n' + str(r.get('errors')))
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
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(management_url, json=payload, headers=headers).json()
    if r.get('errors'):
            logging.error('Create emunation error \n' + str(r.get('errors')))
    return r

def create_enumeration_field(
    token,
    management_url,
    variables
):
    payload = {
        "query": create_enumeration_field_gql,
        'variables': variables
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(management_url, json=payload, headers=headers).json()
    if r.get('errors'):
            logging.error('Create emunation filed error \n' + str(r.get('errors')))
    return r

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

    if r.get('errors'):
        logging.error('Get emunations error \n' + str(r.get('errors')))

    enumerations = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('enumerations')

    return get_match_item(enumerations, apiId)

def get_component_by_api_id(
    token,
    management_url,
    variables,
    apiId
):
    payload = {
        "query": get_components_sql,
        'variables': variables
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(management_url, json=payload, headers=headers).json()

    if r.get('errors'):
        logging.error('Get components error \n' + str(r.get('errors')))

    compoenents = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('components')

    return get_match_item(compoenents, apiId)

def create_component_field(
    token,
    management_url,
    variables
):
    payload = {
        "query": create_component_field_gql,
        'variables': variables
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(management_url, json=payload, headers=headers).json()
    if r.get('errors'):
            logging.error('Create component filed error \n' + str(r.get('errors')) + '\n' + str(variables))
    return r

def create_component_union_field(
    token,
    management_url,
    variables
):
    payload = {
        "query": create_component_union_field_gql,
        'variables': variables
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(management_url, json=payload, headers=headers).json()
    if r.get('errors'):
            logging.error('Create component union filed error \n' + str(r.get('errors')) + '\n' + str(variables))
    return r