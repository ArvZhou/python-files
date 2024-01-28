# -*- coding: UTF-8 -*-
__author__ = 'arvin.zhou'

import re
import time
import logging
from hygraph_utils import get_models_and_components, get_env_id_by_env_name, create_model
from hygraph_utils import create_simple_field, get_model_by_api_id, create_enumeration
from hygraph_utils import create_enumeration_field, get_enumeration_by_api_id

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def get_match_item(items, apiId):
    for item in items:
        if item['apiId'] == apiId:
            return item
        
    return None

def start_sync(info):
    models_and_components = get_models_and_components(
        projectId = info['share']['PROJECT_ID'],
        environment = info['share']['ENVIRONMENT'],
        token = info['share']['TOKEN'],
        managementUrl = info['share']['MANAGEMENT_URL']
    )
    share_models = models_and_components['models']
    share_components = models_and_components['components']
    share_enumerations = models_and_components['enumerations']

    target_models_and_components = get_models_and_components(
        projectId = info['target']['PROJECT_ID'],
        environment = info['target']['ENVIRONMENT'],
        token = info['target']['TOKEN'],
        managementUrl = info['target']['MANAGEMENT_URL']
    )
    target_models = target_models_and_components['models']
    target_components = target_models_and_components['components']
    target_enumerations = target_models_and_components['enumerations']

    share_model_name = info['share']['MODEL_NAME']

    environment_id = get_env_id_by_env_name(
        projectId = info['target']['PROJECT_ID'],
        environment = info['target']['ENVIRONMENT'],
        token = info['target']['TOKEN'],
        managementUrl = info['target']['MANAGEMENT_URL']
    )

    for model in share_models:
        if re.match(share_model_name, model['displayName']):
            target_model = get_match_item(target_models, model['apiId'])
            if not(target_model):
                logging.info('Start to create model!' + model['displayName'])

                create_model(
                    environment_id = environment_id,
                    token = info['target']['TOKEN'],
                    management_url = info['target']['MANAGEMENT_URL'],
                    apiId = model['apiId'],
                    apiIdPlural = model['apiIdPlural'],
                    displayName = model['displayName']
                )

                time.sleep(5)
                target_model = get_model_by_api_id(
                    token = info['target']['TOKEN'],
                    management_url = info['target']['MANAGEMENT_URL'],
                    variables = {
                        'projectId': info['target']['PROJECT_ID'],
                        'environment': info['target']['ENVIRONMENT'],
                        'apiId': model['apiId'],
                    }
                ).get('data').get('viewer').get('project').get('environment').get('contentModel').get('model')
            print(target_model)

            for field in model['fields']:
                if(not(field['isSystem'])):
                    target_field = get_match_item(target_model['fields'], field['apiId'])
                    if target_field:
                        logging.info('This field already exists!' + field.get('displayName'))
                        continue
                    if (field.get('stype')):
                        logging.info('Start to create SimpleField!' + field.get('displayName'))
                        variables={
                            'data': {
                                'modelId': target_model['id'],
                                'apiId': field.get('apiId'),
                                'type': field.get('stype'),
                                'displayName': field.get('displayName'),
                                'description': field.get('description') if field.get('description') is not None else ''
                            }
                        }

                        for key in ['isRequired', 'isUnique', 'isList', 'isLocalized']:
                            variables['data'][key] = field.get(key) if field.get(key) is not None else False

                        create_field_result = create_simple_field(
                            token = info['target']['TOKEN'],
                            management_url = info['target']['MANAGEMENT_URL'],
                            variables = variables
                        )
                        time.sleep(3)

                        if create_field_result and not(create_field_result.get('errors')):
                            logging.info('Create simple field successfully!' + field.get('displayName'))
                    if (field.get('etype')):
                        target_enumeration = get_match_item(target_enumerations, field['enumeration']['apiId'])
                        if not(target_enumeration):
                            share_enumeration = get_match_item(share_enumerations, field['enumeration']['apiId'])
                            if not(share_enumeration):
                                logging.error('Enumeration not found!' + field.get('displayName'))
                                continue
                            logging.info('Start to create Enumeration!' + field['enumeration']['apiId'])
                            share_enumeration_values = share_enumeration["values"]
                            def getValues(value):
                                return {
                                    "apiId": value["apiId"],
                                    "displayName": value["displayName"]
                                }
                            create_enumeration_reslut = create_enumeration(
                                token = info['target']['TOKEN'],
                                management_url = info['target']['MANAGEMENT_URL'],
                                variables = {
                                    "data": {
                                        "environmentId": environment_id,
                                        "apiId": share_enumeration["apiId"],
                                        "displayName": share_enumeration["displayName"],
                                        "values": list(map(getValues, share_enumeration_values))
                                    }
                                }
                            )
                            print(create_enumeration_reslut)
                            time.sleep(5)
                            target_enumeration = get_enumeration_by_api_id(
                                token = info['target']['TOKEN'],
                                management_url = info['target']['MANAGEMENT_URL'],
                                variables = {
                                    'projectId': info['target']['PROJECT_ID'],
                                    'environment': info['target']['ENVIRONMENT'],
                                },
                                apiId = share_enumeration['apiId'],
                            )

                        enumVariables = {
                            "data": {
                                'modelId': target_model['id'],
                                "enumerationId": target_enumeration.get('id'),
                                "type": "ENUMERATION",
                                "apiId": field.get('apiId'),
                                "displayName": field.get('displayName'),
                                "description": field.get('description') if field.get('description') is not None else '',
                            }
                        }
                        for key in ['isRequired', 'isUnique', 'isList']:
                            enumVariables['data'][key] = field.get(key) if field.get(key) is not None else False

                        logging.info('Start to create EnumerableField!' + field.get('displayName'))
                        create_field_result = create_enumeration_field(
                            token = info['target']['TOKEN'],
                            management_url = info['target']['MANAGEMENT_URL'],
                            variables = enumVariables
                        )
                        print(create_field_result)
                        time.sleep(5)
                        if create_field_result and not(create_field_result.get('errors')):
                            logging.info('Create enumerable field successfully!' + field.get('displayName'))
                    if (field.get('utype')):
                        logging.info('This is UnionField!')
                    if (field.get('rtype')):
                        logging.info('This is RelationalField!')
                    if (field.get('udrtype')):
                        logging.info('This is UniDirectionalRelationalField!')
                    if (field.get('ctype')):
                        logging.info('This is ComponentField!')
                    if (field.get('cutype')):
                        logging.info('This is ComponentUnionField!')