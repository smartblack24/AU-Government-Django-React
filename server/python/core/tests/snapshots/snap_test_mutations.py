# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_document_mutation_with_section_id 1'] = {
    'data': {
        'createDocument': {
            'document': {
                'section': {
                    'id': '3'
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_create_document_mutation_without_section_id 1'] = {
    'data': {
        'createDocument': {
            'document': {
                'section': {
                    'id': '4'
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_create_document_mutation_with_not_exist_section 1'] = {
    'data': {
        'createDocument': {
            'document': {
                'section': {
                    'id': '6'
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_update_document_mutation 1'] = {
    'data': {
        'updateDocument': {
            'document': {
                'id': 'RG9jdW1lbnRUeXBlOjY=',
                'section': {
                    'id': '8'
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_update_document_mutation_with_not_exist_document 1'] = {
    'data': {
        'updateDocument': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 3
                }
            ],
            'message': "local variable 'document' referenced before assignment",
            'path': [
                'updateDocument'
            ]
        }
    ]
}

snapshots['test_update_section_mutation 1'] = {
    'data': {
        'updateSection': {
            'errors': [
            ]
        }
    }
}

snapshots['test_update_section_mutation_with_incorrect_document_id 1'] = {
    'data': {
        'updateSection': {
            'errors': [
                'Unknown error has occurred'
            ]
        }
    }
}

snapshots['test_remove_instance_mutation_without_data 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Instance id must be specified',
                'Instance type must be specified'
            ]
        }
    }
}
