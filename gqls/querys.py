fields = '''
    fragment fields on IField {
        id
        apiId
        isSystem
        isList
        displayName
        parent {
            apiId
            displayName
        }
        ... on ComponentUnionField {
            apiId
            cutype: type
            components {
            apiId
            }
        }
        ... on UnionField {
            apiId
            displayName
            union {
                memberTypes {
                    parent {
                    apiId
                    }
                }
            }
            utype: type
        }
        ... on ComponentField {
            apiId
            ctype: type
            component {
                apiId
            }
        }
        ... on UniDirectionalRelationalField {
            apiId
            udrtype: type
        }
        ... on RelationalField {
            apiId
            rtype: type
            relatedField {
                apiId
                displayName
            }
        }
        ... on EnumerableField {
            apiId
            etype: type
            enumeration {
                apiId
            }
        }
        ... on SimpleField {
            apiId
            stype: type
            isLocalized
            formConfig {
                id
                renderer
                config
                extension {
                    id
                    name
                    apiId
                }
                appElement {
                    id
                    name
                    apiId
                    config
                    src
                    features
                }
            }
            tableConfig {
                id
                renderer
            }
        }
        ... on RemoteField {
            apiId
        }
        isSystem
    }
'''

query_models_and_components_sql = '''
    query QueryModels($projectId: ID!, $environment: String!) {
        viewer {
            id
            project(id: $projectId) {
                environment(name: $environment) {
                    id
                    name
                    displayName
                    contentModel {
                        models(includeSystemModels: false) {
                            id
                            apiId
                            apiIdPlural
                            displayName
                            fields(includeApiOnlyFields: false, includeHiddenFields: false) {
                            ...fields
                            }
                        }
                        components(includeSystemComponents: false) {
                            id
                            apiId
                            apiIdPlural
                            displayName
                            fields(includeApiOnlyFields: false, includeHiddenFields: false) {
                                ...fields
                            }
                        }
                        enumerations {
                            id
                            apiId
                            displayName
                            values {
                                id
                                apiId
                                displayName
                            }
                            isSystem
                        }
                    }
                }
            }
        }
    }
''' + fields

# Do not know, why not work
query_model_fields_sql = '''
    query QueryModelfields($projectId: ID!, $environment: String!, $appId: String!) {
        viewer {
            project(id: $projectId) {
                environment(name: $environment) {
                    contentModel {
                        model(apiId: $appId) {
                            fields(includeApiOnlyFields: false, includeHiddenFields: false) {
                                ...fields
                            }
                        }
                    }
                }
            }
        }
    }
'''

get_model_by_api_id_sql = '''
    query QueryModel($projectId: ID!, $environment: String!, $apiId: String!) {
        viewer {
            project(id: $projectId) {
            environment(name: $environment) {
                contentModel {
                    model(apiId: $apiId) {
                        id
                        apiId
                        apiIdPlural
                        createdAt
                        description
                        displayName
                        isSystem
                        isLocalized
                        fields(includeApiOnlyFields: false, includeHiddenFields: false) {
                            ...fields
                        }
                    }
                }
            }
            }
        }
    }
''' + fields

get_enumerations_sql = '''
    query QueryEnumerations($projectId: ID!, $environment: String!) {
        viewer {
            project(id: $projectId) {
            environment(name: $environment) {
                contentModel {
                    enumerations {
                        id
                        apiId
                    }
                }
            }
            }
        }
    }
'''

# get_component_by_api_id_sql = '''
#     query QueryComponent($projectId: ID!, $environment: String!, $apiId: String!) {
#         viewer {
#             project(id: $projectId) {
#                 environment(name: $environment) {
#                     contentModel {
#                         component(apiId: $apiId) {
#                             id
#                             apiId
#                             apiIdPlural
#                             createdAt
#                             description
#                             displayName
#                             isSystem
#                             isLocalized
#                             fields(includeApiOnlyFields: false, includeHiddenFields: false) {
#                                 ...fields
#                             }
#                         }
#                     }
#                 }
#             }
#         }
#     }
# ''' + fields

get_components_sql = '''
    query QueryComponents($projectId: ID!, $environment: String!) {
        viewer {
            project(id: $projectId) {
            environment(name: $environment) {
                contentModel {
                    components(includeSystemComponents: false) {
                        id
                        apiId
                        apiIdPlural
                        displayName
                        fields(includeApiOnlyFields: false, includeHiddenFields: false) {
                            ...fields
                        }
                    }
                }
            }
            }
        }
    }
''' + fields