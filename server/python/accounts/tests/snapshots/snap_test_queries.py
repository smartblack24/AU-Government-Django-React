# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_users_query 1'] = {
    'data': {
        'users': {
            'edges': [
                {
                    'node': {
                        'addressesAreEquals': True,
                        'fullName': 'john47 johnson47',
                        'groups': [
                        ],
                        'hasGmailAccount': False,
                        'location': {
                            'country': None,
                            'state': None,
                            'stateDisplay': None
                        },
                        'photo': None,
                        'pointer': 0,
                        'postalLocation': None,
                        'rate': '0.00',
                        'salutation': 1
                    }
                },
                {
                    'node': {
                        'addressesAreEquals': True,
                        'fullName': 'john48 johnson48',
                        'groups': [
                        ],
                        'hasGmailAccount': False,
                        'location': {
                            'country': None,
                            'state': None,
                            'stateDisplay': None
                        },
                        'photo': None,
                        'pointer': 0,
                        'postalLocation': None,
                        'rate': '0.00',
                        'salutation': 1
                    }
                },
                {
                    'node': {
                        'addressesAreEquals': True,
                        'fullName': 'john49 johnson49',
                        'groups': [
                        ],
                        'hasGmailAccount': False,
                        'location': {
                            'country': None,
                            'state': None,
                            'stateDisplay': None
                        },
                        'photo': None,
                        'pointer': 0,
                        'postalLocation': None,
                        'rate': '0.00',
                        'salutation': 1
                    }
                }
            ]
        }
    }
}

snapshots['test_get_me_query 1'] = {
    'data': {
        'me': {
            'fullName': 'john51 johnson51',
            'id': 'VXNlclR5cGU6MQ=='
        }
    }
}

snapshots['test_get_legal_query 1'] = {
    'data': {
        'legal': {
            'edges': [
                {
                    'node': {
                        'id': 'VXNlclR5cGU6NzA='
                    }
                },
                {
                    'node': {
                        'id': 'VXNlclR5cGU6NzE='
                    }
                }
            ]
        }
    }
}

snapshots['test_get_organisation_detail_query 1'] = {
    'data': {
        'legal': {
            'edges': [
                {
                    'node': {
                        'id': 'VXNlclR5cGU6Mzg='
                    }
                },
                {
                    'node': {
                        'id': 'VXNlclR5cGU6Mzk='
                    }
                }
            ]
        }
    }
}

snapshots['test_staff_query 1'] = {
    'data': {
        'users': {
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                    'node': {
                        'fullName': 'john91 johnson91',
                        'id': 'VXNlclR5cGU6NzI='
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjE=',
                    'node': {
                        'fullName': 'john92 johnson92',
                        'id': 'VXNlclR5cGU6NzM='
                    }
                }
            ]
        }
    }
}

snapshots['test_get_organisations_query 1'] = {
    'data': {
        'organisation': {
            'addressesAreEquals': False,
            'businessSearchWords': None,
            'contacts': {
                'edges': [
                ]
            },
            'groupParent': None,
            'groupStatus': 1,
            'id': 'T3JnYW5pc2F0aW9uVHlwZTo4NQ==',
            'industry': {
                'id': '82',
                'name': 'Industry 83'
            },
            'location': {
                'address1': 'address101',
                'address2': 'address101',
                'country': 'Australia',
                'id': '112',
                'postCode': '12345',
                'state': 1,
                'stateDisplay': 'SA',
                'suburb': 'suburb101'
            },
            'mainLine': None,
            'name': 'Organisation 83',
            'postalLocation': None,
            'website': None
        }
    }
}

snapshots['test_clients_query 1'] = {
    'data': {
        'clients': {
            'edges': [
                {
                    'node': {
                        'invoicingAddress': None,
                        'matters': {
                            'edges': [
                            ]
                        },
                        'mattersCount': 0,
                        'name': 'Organisation 77 - Bob149 Smith149 and Bob150 Smith150',
                        'organisation': {
                            'name': 'Organisation 77'
                        },
                        'secondContact': {
                            'fullName': 'Bob150 Smith150'
                        },
                        'streetAddress': '''address95
address95
suburb95 SA 12345'''
                    }
                },
                {
                    'node': {
                        'invoicingAddress': None,
                        'matters': {
                            'edges': [
                            ]
                        },
                        'mattersCount': 0,
                        'name': 'Organisation 78 - Bob151 Smith151 and Bob152 Smith152',
                        'organisation': {
                            'name': 'Organisation 78'
                        },
                        'secondContact': {
                            'fullName': 'Bob152 Smith152'
                        },
                        'streetAddress': '''address96
address96
suburb96 SA 12345'''
                    }
                },
                {
                    'node': {
                        'invoicingAddress': None,
                        'matters': {
                            'edges': [
                            ]
                        },
                        'mattersCount': 0,
                        'name': 'Organisation 79 - Bob153 Smith153 and Bob154 Smith154',
                        'organisation': {
                            'name': 'Organisation 79'
                        },
                        'secondContact': {
                            'fullName': 'Bob154 Smith154'
                        },
                        'streetAddress': '''address97
address97
suburb97 SA 12345'''
                    }
                }
            ]
        }
    }
}

snapshots['test_clients_query_with_address_data 1'] = {
    'data': {
        'clients': {
            'edges': [
                {
                    'node': {
                        'invoicingAddress': None,
                        'name': 'Organisation 80 - Bob155 Smith155 and Bob156 Smith156',
                        'streetAddress': '''address98
address98
suburb98 SA 12345'''
                    }
                },
                {
                    'node': {
                        'invoicingAddress': None,
                        'name': 'Organisation 81 - Bob157 Smith157 and Bob158 Smith158',
                        'streetAddress': '''address99
address99
suburb99 SA 12345'''
                    }
                },
                {
                    'node': {
                        'invoicingAddress': None,
                        'name': 'Organisation 82 - Bob159 Smith159 and Bob160 Smith160',
                        'streetAddress': '''address100
address100
suburb100 SA 12345'''
                    }
                }
            ]
        }
    }
}

snapshots['test_get_contacts_query 1'] = {
    'data': {
        'contacts': {
            'edges': [
                {
                    'node': {
                        'children': [
                        ],
                        'fullName': 'Bob161 Smith161',
                        'lastNote': None,
                        'notes': [
                        ],
                        'occupation': 160,
                        'salutation': None,
                        'secondContact': None,
                        'spouse': None
                    }
                },
                {
                    'node': {
                        'children': [
                        ],
                        'fullName': 'Bob162 Smith162',
                        'lastNote': None,
                        'notes': [
                        ],
                        'occupation': 161,
                        'salutation': None,
                        'secondContact': None,
                        'spouse': None
                    }
                },
                {
                    'node': {
                        'children': [
                        ],
                        'fullName': 'Bob163 Smith163',
                        'lastNote': None,
                        'notes': [
                        ],
                        'occupation': 162,
                        'salutation': None,
                        'secondContact': None,
                        'spouse': None
                    }
                }
            ]
        }
    }
}

snapshots['test_get_contacts_query_with_all_flag 1'] = {
    'data': {
        'contacts': {
            'edges': [
                {
                    'node': {
                        'id': 'Q29udGFjdFR5cGU6MTYy'
                    }
                },
                {
                    'node': {
                        'id': 'Q29udGFjdFR5cGU6MTYz'
                    }
                },
                {
                    'node': {
                        'id': 'Q29udGFjdFR5cGU6MTY0'
                    }
                }
            ]
        }
    }
}

snapshots['test_get_contacts_query_with_all_extra_data 1'] = {
    'data': {
        'contacts': {
            'edges': [
                {
                    'node': {
                        'id': 'Q29udGFjdFR5cGU6MTcz'
                    }
                },
                {
                    'node': {
                        'id': 'Q29udGFjdFR5cGU6MTc0'
                    }
                },
                {
                    'node': {
                        'id': 'Q29udGFjdFR5cGU6MTc1'
                    }
                }
            ]
        }
    }
}

snapshots['test_get_contacts_query_with_exclude 1'] = {
    'data': {
        'contacts': {
            'edges': [
                {
                    'node': {
                        'id': 'Q29udGFjdFR5cGU6MTgz'
                    }
                },
                {
                    'node': {
                        'id': 'Q29udGFjdFR5cGU6MTg0'
                    }
                },
                {
                    'node': {
                        'id': 'Q29udGFjdFR5cGU6MTg1'
                    }
                }
            ]
        }
    }
}

snapshots['test_get_notes_query 1'] = {
    'data': {
        'notes': [
            {
                'id': '1',
                'text': 'Note text'
            },
            {
                'id': '2',
                'text': 'Note text'
            },
            {
                'id': '3',
                'text': 'Note text'
            },
            {
                'id': '4',
                'text': 'Note text'
            },
            {
                'id': '5',
                'text': 'Note text'
            },
            {
                'id': '6',
                'text': 'Note text'
            },
            {
                'id': '7',
                'text': 'Note text'
            },
            {
                'id': '8',
                'text': 'Note text'
            },
            {
                'id': '9',
                'text': 'Note text'
            },
            {
                'id': '10',
                'text': 'Note text'
            }
        ]
    }
}
