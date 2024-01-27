import requests
from gqls.querys  import query_models_and_components, query_model_fields
from gqls.mutations import create_model_gql, create_simple_field_gql

def get_models_and_components(projectId, environment, token, managementUrl):
    payload = {
        "query": query_models_and_components,
        'variables': { 'projectId': projectId, 'environment': environment }
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(managementUrl, json=payload, headers=headers).json()

    if(r != None):
        print('Get models and components over!')
    models = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('models')
    components = r.get('data').get('viewer').get('project').get('environment').get('contentModel').get('components')

    return { 'models': models, 'components': components }

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
            'environmentId': environment_id,
            'apiId': apiId,
            'apiIdPlural': apiIdPlural,
            'displayName': displayName
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
        "query": query_model_fields,
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
        field_info,
        model_id
):
    field_info['type'] = field_info['stype']
    field_info['modelId'] = model_id
    payload = {
        "query": create_simple_field_gql,
        'variables': field_info
    }
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(management_url, json=payload, headers=headers).json()