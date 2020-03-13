# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_get_industries_query 1'] = {
    'data': {
        'industries': [
            {
                'name': 'Industry 403'
            },
            {
                'name': 'Industry 404'
            },
            {
                'name': 'Industry 405'
            },
            {
                'name': 'Industry 406'
            }
        ]
    }
}

snapshots['test_get_matter_types_query 1'] = {
    'data': {
        'matterTypes': [
            {
                'name': 'Matter type 248'
            },
            {
                'name': 'Matter type 249'
            },
            {
                'name': 'Matter type 250'
            },
            {
                'name': 'Matter type 251'
            }
        ]
    }
}

snapshots['test_get_matter_sub_types_query 1'] = {
    'data': {
        'matterSubTypes': [
            {
                'name': 'Matter sub type'
            },
            {
                'name': 'Matter sub type'
            },
            {
                'name': 'Matter sub type'
            },
            {
                'name': 'Matter sub type'
            }
        ]
    }
}

snapshots['test_get_matter_sub_types_query_without_id 1'] = {
    'data': {
        'matterSubTypes': [
            {
                'name': 'Matter sub type'
            },
            {
                'name': 'Matter sub type'
            },
            {
                'name': 'Matter sub type'
            },
            {
                'name': 'Matter sub type'
            }
        ]
    }
}

snapshots['test_get_invoice_statuses_query 1'] = {
    'data': {
        'invoiceStatuses': [
            {
                'name': 'Invoice status 3'
            },
            {
                'name': 'Invoice status 4'
            },
            {
                'name': 'Invoice status 5'
            },
            {
                'name': 'Invoice status 6'
            }
        ]
    }
}

snapshots['test_get_offices_query 1'] = {
    'data': {
        'offices': [
            {
                'name': 'Adelaide',
                'phone': '12345',
                'shortName': 'ADL',
                'suburb': 'Adelaide'
            },
            {
                'name': 'Adelaide',
                'phone': '12345',
                'shortName': 'ADL',
                'suburb': 'Adelaide'
            },
            {
                'name': 'Sydney',
                'phone': '12345',
                'shortName': 'SYD',
                'suburb': 'Sydney'
            },
            {
                'name': 'Sydney',
                'phone': '12345',
                'shortName': 'SYD',
                'suburb': 'Sydney'
            },
            {
                'name': 'UnknowPlace',
                'phone': '12345',
                'shortName': 'Unknown',
                'suburb': 'UnknowPlace'
            },
            {
                'name': 'UnknowPlace',
                'phone': '12345',
                'shortName': 'Unknown',
                'suburb': 'UnknowPlace'
            }
        ]
    }
}

snapshots['test_get_documents_query 1'] = {
    'data': {
        'documents': {
            'edges': [
                {
                    'node': {
                        'chargingClause': None,
                        'chargingClauseDisplay': None,
                        'documentType': None,
                        'nominatedType': None,
                        'nominatedTypeDisplay': None,
                        'status': None,
                        'statusDisplay': None
                    }
                },
                {
                    'node': {
                        'chargingClause': None,
                        'chargingClauseDisplay': None,
                        'documentType': None,
                        'nominatedType': None,
                        'nominatedTypeDisplay': None,
                        'status': None,
                        'statusDisplay': None
                    }
                },
                {
                    'node': {
                        'chargingClause': None,
                        'chargingClauseDisplay': None,
                        'documentType': None,
                        'nominatedType': None,
                        'nominatedTypeDisplay': None,
                        'status': None,
                        'statusDisplay': None
                    }
                }
            ]
        }
    }
}

snapshots['test_get_documents_query_with_organisation_id 1'] = {
    'data': {
        'documents': {
            'edges': [
            ]
        }
    }
}

snapshots['test_get_document_types_query 1'] = {
    'data': {
        'documentTypes': [
            {
                'name': 'PDF'
            },
            {
                'name': 'PDF'
            },
            {
                'name': 'PDF'
            },
            {
                'name': 'PDF'
            }
        ]
    }
}

snapshots['test_get_sections_query 1'] = {
    'data': {
        'sections': [
            {
                'number': '23'
            },
            {
                'number': '24'
            },
            {
                'number': '25'
            },
            {
                'number': '26'
            }
        ]
    }
}

snapshots['test_get_occupations_query 1'] = {
    'data': {
        'occupations': [
            {
                'name': 'Invoice status 849'
            },
            {
                'name': 'Invoice status 850'
            },
            {
                'name': 'Invoice status 851'
            },
            {
                'name': 'Invoice status 852'
            }
        ]
    }
}

snapshots['test_get_occupation_by_id_query 1'] = {
    'data': {
        'occupation': {
            'name': 'Invoice status 853'
        }
    }
}

snapshots['test_get_occupation_by_id_query_without_data 1'] = {
    'data': {
        'occupation': None
    }
}

snapshots['test_get_documents_query_with_contact_id 1'] = {
    'data': {
        'documents': {
            'edges': [
            ]
        }
    }
}
