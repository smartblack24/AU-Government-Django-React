# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_user_filters 1'] = {
    'data': {
        'users': {
            'edges': [
                {
                    'node': {
                        'fullName': 'first last',
                        'id': 'VXNlclR5cGU6MQ==',
                        'rate': '0.00'
                    }
                }
            ]
        }
    }
}

snapshots['test_user_filters_with_value_error 1'] = {
    'data': {
        'users': {
            'edges': [
            ]
        }
    }
}

snapshots['test_contacts_filters 1'] = {
    'data': {
        'contacts': {
            'edges': [
                {
                    'node': {
                        'fullName': 'first last',
                        'id': 'Q29udGFjdFR5cGU6MQ==',
                        'mobile': '1231231'
                    }
                }
            ]
        }
    }
}

snapshots['test_contacts_filters_with_value_error 1'] = {
    'data': {
        'contacts': {
            'edges': [
                {
                    'node': {
                        'fullName': 'last last',
                        'id': 'Q29udGFjdFR5cGU6Mg==',
                        'mobile': '1231231'
                    }
                }
            ]
        }
    }
}

snapshots['test_client_filters 1'] = {
    'data': {
        'clients': {
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                    'node': {
                        'contact': {
                            'fullName': 'first contact',
                            'id': 'Q29udGFjdFR5cGU6Mw==',
                            'mobile': '1231231'
                        },
                        'mattersCount': 0,
                        'name': 'organisation - first contact',
                        'organisation': {
                            'id': 'T3JnYW5pc2F0aW9uVHlwZTox',
                            'mainLine': None,
                            'name': 'organisation'
                        },
                        'secondContact': None
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjE=',
                    'node': {
                        'contact': {
                            'fullName': 'first contact',
                            'id': 'Q29udGFjdFR5cGU6Mw==',
                            'mobile': '1231231'
                        },
                        'mattersCount': 0,
                        'name': 'organisation - first contact',
                        'organisation': {
                            'id': 'T3JnYW5pc2F0aW9uVHlwZTox',
                            'mainLine': None,
                            'name': 'organisation'
                        },
                        'secondContact': None
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                    'node': {
                        'contact': {
                            'fullName': 'first contact',
                            'id': 'Q29udGFjdFR5cGU6Mw==',
                            'mobile': '1231231'
                        },
                        'mattersCount': 0,
                        'name': 'organisation - first contact',
                        'organisation': {
                            'id': 'T3JnYW5pc2F0aW9uVHlwZTox',
                            'mainLine': None,
                            'name': 'organisation'
                        },
                        'secondContact': None
                    }
                }
            ],
            'totalPages': 1
        }
    }
}

snapshots['test_client_filters_with_value_error 1'] = {
    'data': {
        'clients': {
            'edges': [
            ],
            'totalPages': 0
        }
    }
}

snapshots['test_clients_matter_filter_with_true 1'] = {
    'data': {
        'clients': {
            'edges': [
            ],
            'totalPages': 0
        }
    }
}

snapshots['test_clients_matter_filter_with_false 1'] = {
    'data': {
        'clients': {
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                    'node': {
                        'id': 'Q2xpZW50VHlwZToxMg==',
                        'mattersCount': 0,
                        'name': 'Organisation 3 - Bob19 Smith19 and Bob20 Smith20'
                    }
                }
            ],
            'totalPages': 1
        }
    }
}
