# -*- coding: UTF-8 -*-
__author__ = 'arvin.zhou'

import re
import time
import logging
from hygraph_utils import get_models_and_components, get_env_id_by_env_name
from hygraph_utils import create_model, get_model_by_api_id
from hygraph_utils import create_component, get_component_by_api_id
from hygraph_utils import create_enumeration, create_enumeration_field, get_enumeration_by_api_id
from hygraph_utils import create_simple_field
from utils import get_match_item

class SyncSchema():
    def __init__(self, project_info) -> None:
        self.p_info=project_info
        self.setShareInfo()
        self.setTargetInfo()
        self.start_sync()
    def setShareInfo(self):
        self.s_p_id = self.p_info['share']['PROJECT_ID']
        self.s_p_environment = self.p_info['share']['ENVIRONMENT']
        self.s_p_token = self.p_info['share']['TOKEN']
        self.s_p_management_url = self.p_info['share']['MANAGEMENT_URL']
        self.s_p_model_name = self.p_info['share']['MODEL_NAME']

        m_a_c = get_models_and_components(projectId=self.s_p_id, environment=self.s_p_environment, token= self.s_p_token,managementUrl = self.s_p_management_url)
        self.s_p_models=m_a_c['models']
        self.s_p_components=m_a_c['components']
        self.s_p_enumerations=m_a_c['enumerations']
    def setTargetInfo(self):
        self.t_p_id = self.p_info['target']['PROJECT_ID']
        self.t_p_environment = self.p_info['target']['ENVIRONMENT']
        self.t_p_token = self.p_info['target']['TOKEN']
        self.t_p_management_url = self.p_info['target']['MANAGEMENT_URL']

        self.t_p_env_id = get_env_id_by_env_name(
            projectId = self.t_p_id,
            environment = self.t_p_environment,
            token = self.t_p_token,
            managementUrl = self.t_p_management_url
        )
        self.set_target_models_and_components()
    def set_target_models_and_components(self):
        logging.info('Get target models and components')
        m_a_c = get_models_and_components(projectId=self.t_p_id, environment=self.t_p_environment, token= self.t_p_token,managementUrl = self.t_p_management_url)
        self.t_p_models=m_a_c['models']
        self.t_p_components=m_a_c['components']
        self.t_p_enumerations=m_a_c['enumerations']
        logging.info('Get target models and components successfully')

    def start_sync(self):
        for model in self.s_p_models:
             if re.match(self.s_p_model_name, model['displayName']):
                 self.clone_model(model)
        for component in self.s_p_components:
             if re.match(self.s_p_model_name, component['displayName']):
                 self.clone_component(component)
    
    def clone_model(self, share_model):
        self.set_target_models_and_components()
        target_model = get_match_item(self.t_p_models, share_model['apiId'])

        if not(target_model):
            logging.info('Start to create model!' + share_model['displayName'])

            create_model(
                environment_id = self.t_p_env_id,
                token = self.t_p_token,
                management_url = self.t_p_management_url,
                apiId = share_model['apiId'],
                apiIdPlural = share_model['apiIdPlural'],
                displayName = share_model['displayName']
            )
            time.sleep(5)
            target_model = get_model_by_api_id(
                token = self.t_p_token,
                management_url = self.t_p_management_url,
                variables = {
                    'projectId': self.t_p_id,
                    'environment': self.t_p_environment,
                    'apiId': share_model['apiId'],
                }
            )
            
        self.clone_all_fields(share_model['fields'], target_model)

    def clone_component(self, share_component):
        self.set_target_models_and_components()
        target_component = get_match_item(self.t_p_components, share_component['apiId'])
        if not(target_component):
            logging.info('Start to create Component!' + share_component['displayName'])
            create_component(
                management_url = self.t_p_management_url,
                token = self.t_p_token,
                variables = {
                    "data": {
                        "environmentId": self.t_p_env_id,
                        "apiId": share_component['apiId'],
                        "apiIdPlural": share_component['apiIdPlural'],
                        "displayName": share_component['displayName']
                    }
                }
            )
            time.sleep(5)
            target_component = get_component_by_api_id(
                token = self.t_p_token,
                management_url = self.t_p_management_url,
                variables = {
                    'projectId': self.t_p_id,
                    'environment': self.t_p_environment 
                },
                apiId = share_component['apiId'],
            )
        self.clone_all_fields(share_component['fields'], target_component)

    def clone_all_fields(self, allFields, parent):
        for field in allFields:
            if(not(field['isSystem'])):
                target_field = get_match_item(parent['fields'], field['apiId'])
                if target_field:
                    logging.info('This field already exists!' + field.get('displayName'))
                    continue
                if (field.get('stype')):
                    self.clone_simple_field(field, parent)
                if (field.get('etype')):
                    self.clone_enumeration_field(field, parent)
                if (field.get('ctype')):
                    self.clone_component_field(field, parent)
                    logging.info('This is ComponentField!')
                if (field.get('utype')):
                    logging.info('This is UnionField!')
                if (field.get('rtype')):
                    logging.info('This is RelationalField!')
                if (field.get('udrtype')):
                    logging.info('This is UniDirectionalRelationalField!')
                if (field.get('cutype')):
                    logging.info('This is ComponentUnionField!')

    
    def clone_simple_field(self, field, parent):
        logging.info('Start to create SimpleField!' + field.get('displayName'))
        variables={
            'data': {
                'parentId': parent['id'],
                'apiId': field.get('apiId'),
                'type': field.get('stype'),
                'displayName': field.get('displayName'),
                'description': field.get('description') if field.get('description') is not None else ''
            }
        }

        for key in ['isRequired', 'isUnique', 'isList', 'isLocalized']:
            variables['data'][key] = field.get(key) if field.get(key) is not None else False

        create_field_result = create_simple_field(
            token = self.t_p_token,
            management_url = self.t_p_management_url,
            variables = variables
        )
        time.sleep(3)

        if create_field_result and not(create_field_result.get('errors')):
            logging.info('Create simple field successfully!' + field.get('displayName'))
    
    def clone_enumeration_field(self, field, parent):
        logging.info('Start to create EnumerationField!' + field.get('displayName'))
        target_enumeration = get_match_item(self.t_p_enumerations, field['enumeration']['apiId'])
        if not(target_enumeration):
            share_enumeration = get_match_item(self.s_p_enumerations, field['enumeration']['apiId'])
            if not(share_enumeration):
                logging.error('Enumeration not found!' + field.get('displayName'))
                return
            logging.info('Start to create Enumeration!' + field['enumeration']['apiId'])
            share_enumeration_values = share_enumeration["values"]
            create_enumeration_reslut = create_enumeration(
                token = self.t_p_token,
                management_url = self.t_p_management_url,
                variables = {
                    "data": {
                        "environmentId": self.t_p_env_id,
                        "apiId": share_enumeration["apiId"],
                        "displayName": share_enumeration["displayName"],
                        "values": list(map(lambda value: {"apiId": value["apiId"], "displayName": value["displayName"]}, share_enumeration_values))
                    }
                }
            )
            if create_enumeration_reslut and not(create_enumeration_reslut.get('errors')):
                logging.info('Create Enumeration successfully!')

            time.sleep(5)
            target_enumeration = get_enumeration_by_api_id(
                token = self.t_p_token,
                management_url = self.t_p_management_url,
                variables = {
                    'projectId': self.t_p_id,
                    'environment': self.t_p_environment,
                },
                apiId = share_enumeration['apiId'],
            )

        enumVariables = {
            "data": {
                'parentId': parent['id'],
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
            token = self.t_p_token,
            management_url = self.t_p_management_url,
            variables = enumVariables
        )

        time.sleep(5)
        if create_field_result and not(create_field_result.get('errors')):
            logging.info('Create enumerable field successfully!' + field.get('displayName'))
    
    def clone_component_field(self, field, target_field):
        logging.info('Start to create ComponentField!' + field.get('displayName'))