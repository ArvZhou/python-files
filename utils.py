import os
import json

def save_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
        file.close()

def get_gql(gql_path):
    if os.path.exists(gql_path):    
        with open(gql_path, 'r') as file:
            content = file.read()
            file.close()
            return content
    else:
        raise Exception(f'gql file not found: {gql_path}')

def get_json(json_path):
    if os.path.exists(json_path):    
        with open(json_path, 'r') as file:
            content = file.read()
            file.close()
            return json.loads(content)
    else:
        raise Exception(f'json file not found: {json_path}')

def get_match_item(items, apiId):
    for item in items:
        if item['apiId'] == apiId:
            return item
        
    return None