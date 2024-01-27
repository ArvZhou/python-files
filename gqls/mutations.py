create_model_gql = '''
    mutation MutationModel($environmentId: ID!, $apiId: String!, $apiIdPlural: String!, $displayName: String!) {
        createModel(
            data: {
                environmentId: $environmentId,
                apiId: $apiId,
                apiIdPlural: $apiIdPlural,
                displayName: $displayName
            }
        ) {
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
    mutation CreateSimpleField(
        $apiId: String!,
        $type: SimpleFieldType!,
        $displayName: String!,
        $isRequired: Boolean!,
        $isUnique: Boolean!,
        $isList: Boolean!,
        $isLocalized: Boolean!,
        $description: String!,
        $modelId: ID!,
    ) {
        createSimpleField(
            data: {
                apiId: $apiId,
                type: $type,
                displayName: $displayName,
                isRequired: $isRequired,
                isUnique: $isUnique,
                isList: $isList,
                isLocalized: $isLocalized,
                description: $description,
                modelId: $modelId
            }
        ) {
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