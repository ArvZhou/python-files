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

create_component_gql = '''
    mutation MutationComponent($data: CreateComponentInput!) {
        createComponent(data: $data) {
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

create_component_field_gql = '''
    mutation CreateComponentField($data: CreateComponentFieldInput!) {
        createComponentField(data: $data) {
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

create_component_union_field_gql = '''
    mutation CreateComponentUnionField($data: CreateComponentUnionFieldInput!) {
        createComponentUnionField(data: $data) {
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

create_relational_field_gql = '''
    mutation CreateRelationalField($data: CreateRelationalFieldInput!) {
        createRelationalField(data: $data) {
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

create_union_field_gql = '''
    mutation CreateUnionField($data: CreateUnionFieldInput!) {
        createUnionField(data: $data) {
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