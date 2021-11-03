"""
Cerberus specifications for Devbox schema files
"""


PROJECT_FIELD_RULES = {
    'type': {
        'type': 'string'
    },

    'webroot': {
        'type': 'string'
    },

    'php': {
        'type': ['string', 'float']
    },

    'resources': {
        'type': 'list',
        'schema': {
            'type': 'string'
        },
    },
}

INSTANCE_VALUE_RULES = {
    'ssh': {
        'type': 'dict',
        'schema': {
            'host': {
                'type': 'string',
                'required': True,
            },

            'user': {
                'type': 'string',
                'required': True,
            },
        },
    },

    'deployment': {
        'type': 'dict',
        'schema': {
            'method': {
                'type': 'string',
                'required': True,
            },

            'dir': {
                'type': 'string',
                'required': True,
            },
        },
    },
}

SCHEMA_FILE_RULES = {
    'version': {
        'type': ['string', 'integer'],
        'required': True,
    },

    'project': {
        'type': 'dict',
        'required': True,
        'schema': PROJECT_FIELD_RULES,
    },

    'instances': {
        'type': 'dict',
        'required': False,

        'keysrules': {
            'type': 'string',
            'regex': '[A-Za-z0-9-_]+'
        },

        'valuesrules': {
            'type': 'dict',
            'required': True,
            'schema': INSTANCE_VALUE_RULES,
        },
    },
}