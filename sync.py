# -*- coding: UTF-8 -*-
__author__ = 'arvin.zhou'

import re
import time
from hygraph_utils import get_models_and_components, get_env_id_by_env_name, create_model, create_simple_field

def start_sync(info):
    models_and_components = get_models_and_components(
        projectId = info['share']['PROJECT_ID'],
        environment = info['share']['ENVIRONMENT'],
        token = info['share']['TOKEN'],
        managementUrl = info['share']['MANAGEMENT_URL']
    )

    share_model_name = info['share']['MODEL_NAME']

    environment_id = get_env_id_by_env_name(
        projectId = info['target']['PROJECT_ID'],
        environment = info['target']['ENVIRONMENT'],
        token = info['target']['TOKEN'],
        managementUrl = info['target']['MANAGEMENT_URL']
    )

    for model in models_and_components['models']:
        if re.match(share_model_name, model['displayName']):
            create_model_reslut = create_model(
                environment_id = environment_id,
                token = info['target']['TOKEN'],
                management_url = info['target']['MANAGEMENT_URL'],
                apiId = model['apiId'],
                apiIdPlural = model['apiIdPlural'],
                displayName = model['displayName']
            )
            time.sleep(3)
            print(create_model_reslut)

            for field in model['fields']:
                if(not(field['isSystem'])):
                    if (field.get('stype')):
                        print('Start to create SimpleField!')
                        create_field_result = create_simple_field(
                            token = info['target']['TOKEN'],
                            management_url = info['target']['MANAGEMENT_URL'],
                            field_info= field,
                            model_id=create_model_reslut.get('data').get('createModel').get('migration').get('id')
                        )
                        print(create_field_result)
                        if create_field_result:
                            print('Create simple field successfully!')
                    if (field.get('etype')):
                        print('This is EnumerableField!')
                    if (field.get('rtype')):
                        print('This is RelationalField!')
                    if (field.get('udrtype')):
                        print('This is UniDirectionalRelationalField!')
                    if (field.get('ctype')):
                        print('This is ComponentField!')
                    if (field.get('utype')):
                        print('This is UnionField!')
                    if (field.get('cutype')):
                        print('This is ComponentUnionField!')