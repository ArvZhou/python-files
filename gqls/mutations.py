create_model_gql = '''
    mutation MutationModel($data: CreateModelInput!) {
        createModel(data: $data) {
            migration {
                createdAt
                errors
                finishedAt
                id
                name
                operationType
                resourceId
                status
            }
        }
    }
'''

create_simple_field_gql = '''
    mutation CreateSimpleField($data: CreateSimpleFieldInput!) {
        createSimpleField(data: $data) {
            migration {
                createdAt
                errors
                finishedAt
                id
                name
                operationType
                resourceId
                status
            }
        }
    }
'''

create_enumeration_gql = '''
    mutation CreateEnumeration($data: CreateEnumerationInput!) {
        createEnumeration(data: $data) {
            migration {
                createdAt
                errors
                finishedAt
                id
                name
                operationType
                resourceId
                status
            }
        }
    }
'''

create_enumeration_field_gql = '''
    mutation CreateEnumerableField($data: CreateEnumerableFieldInput!) {
        createEnumerableField(data: $data) {
            migration {
                createdAt
                errors
                finishedAt
                id
                name
                operationType
                resourceId
                status
            }
        }
    }
'''