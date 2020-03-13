# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_invoices_status_filter_with_null_value 1'] = {
    'data': {
        'invoices': {
            'edges': [
            ]
        }
    }
}

snapshots['test_invoices_number_or_client_name_filter_with_str 1'] = {
    'data': {
        'invoices': {
            'edges': [
                {
                    'node': {
                        'id': 'SW52b2ljZVR5cGU6OTk2NQ==',
                        'matter': {
                            'client': {
                                'id': 'Q2xpZW50VHlwZTozODU=',
                                'name': 'first last'
                            },
                            'id': 'TWF0dGVyVHlwZToyMzQ=',
                            'name': 'Matter 237'
                        }
                    }
                },
                {
                    'node': {
                        'id': 'SW52b2ljZVR5cGU6Nzg0NQ==',
                        'matter': {
                            'client': {
                                'id': 'Q2xpZW50VHlwZTozODU=',
                                'name': 'first last'
                            },
                            'id': 'TWF0dGVyVHlwZToyMzQ=',
                            'name': 'Matter 237'
                        }
                    }
                },
                {
                    'node': {
                        'id': 'SW52b2ljZVR5cGU6NjczNQ==',
                        'matter': {
                            'client': {
                                'id': 'Q2xpZW50VHlwZTozODU=',
                                'name': 'first last'
                            },
                            'id': 'TWF0dGVyVHlwZToyMzQ=',
                            'name': 'Matter 237'
                        }
                    }
                }
            ]
        }
    }
}

snapshots['test_invoices_number_or_client_name_filter_with_value_error 1'] = {
    'data': {
        'invoices': {
            'edges': [
                {
                    'node': {
                        'id': 'SW52b2ljZVR5cGU6Mw==',
                        'matter': {
                            'client': {
                                'id': 'Q2xpZW50VHlwZTozODY=',
                                'name': 'name name'
                            },
                            'id': 'TWF0dGVyVHlwZToyMzU=',
                            'name': 'Matter 238'
                        }
                    }
                }
            ]
        }
    }
}

snapshots['test_invoices_number_or_client_name_filter_with_int 1'] = {
    'data': {
        'invoices': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 3
                }
            ],
            'message': '''invalid input syntax for integer: ""
''',
            'path': [
                'invoices'
            ]
        }
    ]
}

snapshots['test_invoices_is_paid_filter_with_true 1'] = {
    'data': {
        'invoices': {
            'edges': [
                {
                    'node': {
                        'id': 'SW52b2ljZVR5cGU6Nw==',
                        'matter': {
                            'client': {
                                'id': 'Q2xpZW50VHlwZTozODg=',
                                'name': 'Organisation 404 - Bob846 Smith846 and Bob847 Smith847'
                            },
                            'id': 'TWF0dGVyVHlwZToyMzc=',
                            'name': 'Matter 240'
                        }
                    }
                },
                {
                    'node': {
                        'id': 'SW52b2ljZVR5cGU6OA==',
                        'matter': {
                            'client': {
                                'id': 'Q2xpZW50VHlwZTozODk=',
                                'name': 'Organisation 405 - Bob848 Smith848 and Bob849 Smith849'
                            },
                            'id': 'TWF0dGVyVHlwZToyMzg=',
                            'name': 'Matter 241'
                        }
                    }
                },
                {
                    'node': {
                        'id': 'SW52b2ljZVR5cGU6OQ==',
                        'matter': {
                            'client': {
                                'id': 'Q2xpZW50VHlwZTozOTA=',
                                'name': 'Organisation 406 - Bob850 Smith850 and Bob851 Smith851'
                            },
                            'id': 'TWF0dGVyVHlwZToyMzk=',
                            'name': 'Matter 242'
                        }
                    }
                }
            ]
        }
    }
}

snapshots['test_invoices_is_paid_filter_with_false 1'] = {
    'data': {
        'invoices': {
            'edges': [
            ]
        }
    }
}

snapshots['test_invoices_status_filter 1'] = {
    'data': {
        'invoices': {
            'edges': [
                {
                    'node': {
                        'id': 'SW52b2ljZVR5cGU6MTU=',
                        'matter': {
                            'client': {
                                'id': 'Q2xpZW50VHlwZTozOTY=',
                                'name': 'Organisation 412 - Bob862 Smith862 and Bob863 Smith863'
                            },
                            'id': 'TWF0dGVyVHlwZToyNDU=',
                            'name': 'Matter 248'
                        }
                    }
                },
                {
                    'node': {
                        'id': 'SW52b2ljZVR5cGU6MTQ=',
                        'matter': {
                            'client': {
                                'id': 'Q2xpZW50VHlwZTozOTU=',
                                'name': 'Organisation 411 - Bob860 Smith860 and Bob861 Smith861'
                            },
                            'id': 'TWF0dGVyVHlwZToyNDQ=',
                            'name': 'Matter 247'
                        }
                    }
                },
                {
                    'node': {
                        'id': 'SW52b2ljZVR5cGU6MTM=',
                        'matter': {
                            'client': {
                                'id': 'Q2xpZW50VHlwZTozOTQ=',
                                'name': 'Organisation 410 - Bob858 Smith858 and Bob859 Smith859'
                            },
                            'id': 'TWF0dGVyVHlwZToyNDM=',
                            'name': 'Matter 246'
                        }
                    }
                }
            ]
        }
    }
}
