# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_matter_status_filter 1'] = {
    'data': {
        'matters': {
            'edges': [
            ]
        }
    }
}

snapshots['test_time_entries_is_billed_filter 1'] = {
    'data': {
        'timeEntries': {
            'edges': [
            ],
            'pageInfo': {
                'endCursor': None,
                'hasNextPage': False
            },
            'totalPages': 0
        }
    }
}

snapshots['test_matters_client_name_filter 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo4OA==',
                            'name': 'organisation - first contact'
                        },
                        'id': 'TWF0dGVyVHlwZToxNQ==',
                        'name': 'Matter 14'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo4OA==',
                            'name': 'organisation - first contact'
                        },
                        'id': 'TWF0dGVyVHlwZToxNg==',
                        'name': 'Matter 15'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo4OA==',
                            'name': 'organisation - first contact'
                        },
                        'id': 'TWF0dGVyVHlwZToxNw==',
                        'name': 'Matter 16'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_client_name_filter_with_not_full_client_name 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo4OQ==',
                            'name': 'first contact'
                        },
                        'id': 'TWF0dGVyVHlwZToyMA==',
                        'name': 'Matter 19'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo4OQ==',
                            'name': 'first contact'
                        },
                        'id': 'TWF0dGVyVHlwZToyMQ==',
                        'name': 'Matter 20'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo4OQ==',
                            'name': 'first contact'
                        },
                        'id': 'TWF0dGVyVHlwZToyMg==',
                        'name': 'Matter 21'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_client_name_filter_with_value_error 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo5MA==',
                            'name': 'name name'
                        },
                        'id': 'TWF0dGVyVHlwZToyNQ==',
                        'name': 'Matter 24'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo5MA==',
                            'name': 'name name'
                        },
                        'id': 'TWF0dGVyVHlwZToyNg==',
                        'name': 'Matter 25'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo5MA==',
                            'name': 'name name'
                        },
                        'id': 'TWF0dGVyVHlwZToyNw==',
                        'name': 'Matter 26'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_principal_name_filter 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo5MQ==',
                            'name': 'Organisation 95 - Bob225 Smith225 and Bob226 Smith226'
                        },
                        'id': 'TWF0dGVyVHlwZTozMA==',
                        'name': 'Matter 29'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo5Mg==',
                            'name': 'Organisation 96 - Bob227 Smith227 and Bob228 Smith228'
                        },
                        'id': 'TWF0dGVyVHlwZTozMQ==',
                        'name': 'Matter 30'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo5Mw==',
                            'name': 'Organisation 97 - Bob229 Smith229 and Bob230 Smith230'
                        },
                        'id': 'TWF0dGVyVHlwZTozMg==',
                        'name': 'Matter 31'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_principal_name_filter_with_value_error 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo5Ng==',
                            'name': 'Organisation 100 - Bob235 Smith235 and Bob236 Smith236'
                        },
                        'id': 'TWF0dGVyVHlwZTozNQ==',
                        'name': 'Matter 34'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo5Nw==',
                            'name': 'Organisation 101 - Bob237 Smith237 and Bob238 Smith238'
                        },
                        'id': 'TWF0dGVyVHlwZTozNg==',
                        'name': 'Matter 35'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZTo5OA==',
                            'name': 'Organisation 102 - Bob239 Smith239 and Bob240 Smith240'
                        },
                        'id': 'TWF0dGVyVHlwZTozNw==',
                        'name': 'Matter 36'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_manager_name_filter 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMDE=',
                            'name': 'Organisation 105 - Bob245 Smith245 and Bob246 Smith246'
                        },
                        'id': 'TWF0dGVyVHlwZTo0MA==',
                        'name': 'Matter 39'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMDI=',
                            'name': 'Organisation 106 - Bob247 Smith247 and Bob248 Smith248'
                        },
                        'id': 'TWF0dGVyVHlwZTo0MQ==',
                        'name': 'Matter 40'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMDM=',
                            'name': 'Organisation 107 - Bob249 Smith249 and Bob250 Smith250'
                        },
                        'id': 'TWF0dGVyVHlwZTo0Mg==',
                        'name': 'Matter 41'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_manager_name_filter_with_value_error 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMDY=',
                            'name': 'Organisation 110 - Bob255 Smith255 and Bob256 Smith256'
                        },
                        'id': 'TWF0dGVyVHlwZTo0NQ==',
                        'name': 'Matter 44'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMDc=',
                            'name': 'Organisation 111 - Bob257 Smith257 and Bob258 Smith258'
                        },
                        'id': 'TWF0dGVyVHlwZTo0Ng==',
                        'name': 'Matter 45'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMDg=',
                            'name': 'Organisation 112 - Bob259 Smith259 and Bob260 Smith260'
                        },
                        'id': 'TWF0dGVyVHlwZTo0Nw==',
                        'name': 'Matter 46'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_staff_name_filter 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMTE=',
                            'name': 'Organisation 115 - Bob265 Smith265 and Bob266 Smith266'
                        },
                        'id': 'TWF0dGVyVHlwZTo1MA==',
                        'name': 'Matter 49'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMTI=',
                            'name': 'Organisation 116 - Bob267 Smith267 and Bob268 Smith268'
                        },
                        'id': 'TWF0dGVyVHlwZTo1MQ==',
                        'name': 'Matter 50'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMTM=',
                            'name': 'Organisation 117 - Bob269 Smith269 and Bob270 Smith270'
                        },
                        'id': 'TWF0dGVyVHlwZTo1Mg==',
                        'name': 'Matter 51'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_staff_name_filter_with_value_error 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMTY=',
                            'name': 'Organisation 120 - Bob275 Smith275 and Bob276 Smith276'
                        },
                        'id': 'TWF0dGVyVHlwZTo1NQ==',
                        'name': 'Matter 54'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMTc=',
                            'name': 'Organisation 121 - Bob277 Smith277 and Bob278 Smith278'
                        },
                        'id': 'TWF0dGVyVHlwZTo1Ng==',
                        'name': 'Matter 55'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMTg=',
                            'name': 'Organisation 122 - Bob279 Smith279 and Bob280 Smith280'
                        },
                        'id': 'TWF0dGVyVHlwZTo1Nw==',
                        'name': 'Matter 56'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_assistant_name_filter 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMjE=',
                            'name': 'Organisation 125 - Bob285 Smith285 and Bob286 Smith286'
                        },
                        'id': 'TWF0dGVyVHlwZTo2MA==',
                        'name': 'Matter 59'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMjI=',
                            'name': 'Organisation 126 - Bob287 Smith287 and Bob288 Smith288'
                        },
                        'id': 'TWF0dGVyVHlwZTo2MQ==',
                        'name': 'Matter 60'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMjM=',
                            'name': 'Organisation 127 - Bob289 Smith289 and Bob290 Smith290'
                        },
                        'id': 'TWF0dGVyVHlwZTo2Mg==',
                        'name': 'Matter 61'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_assistant_name_filter_with_value_error 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMjY=',
                            'name': 'Organisation 130 - Bob295 Smith295 and Bob296 Smith296'
                        },
                        'id': 'TWF0dGVyVHlwZTo2NQ==',
                        'name': 'Matter 64'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMjc=',
                            'name': 'Organisation 131 - Bob297 Smith297 and Bob298 Smith298'
                        },
                        'id': 'TWF0dGVyVHlwZTo2Ng==',
                        'name': 'Matter 65'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMjg=',
                            'name': 'Organisation 132 - Bob299 Smith299 and Bob300 Smith300'
                        },
                        'id': 'TWF0dGVyVHlwZTo2Nw==',
                        'name': 'Matter 66'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_is_paid_filter_with_value_false 1'] = {
    'data': {
        'matters': {
            'edges': [
            ]
        }
    }
}

snapshots['test_matters_is_paid_filter_with_value_true 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMzY=',
                            'name': 'Organisation 140 - Bob315 Smith315 and Bob316 Smith316'
                        },
                        'id': 'TWF0dGVyVHlwZTo3NQ==',
                        'name': 'Matter 74'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMzc=',
                            'name': 'Organisation 141 - Bob317 Smith317 and Bob318 Smith318'
                        },
                        'id': 'TWF0dGVyVHlwZTo3Ng==',
                        'name': 'Matter 75'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxMzg=',
                            'name': 'Organisation 142 - Bob319 Smith319 and Bob320 Smith320'
                        },
                        'id': 'TWF0dGVyVHlwZTo3Nw==',
                        'name': 'Matter 76'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_billable_status_exclude_filter 1'] = {
    'data': {
        'matters': {
            'edges': [
            ]
        }
    }
}

snapshots['test_matter_report_filter_name_filter 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNDY=',
                            'name': 'Organisation 150 - Bob335 Smith335 and Bob336 Smith336'
                        },
                        'id': 'TWF0dGVyVHlwZTo4NQ==',
                        'name': 'Matter 84'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNDc=',
                            'name': 'Organisation 151 - Bob337 Smith337 and Bob338 Smith338'
                        },
                        'id': 'TWF0dGVyVHlwZTo4Ng==',
                        'name': 'Matter 85'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNDg=',
                            'name': 'Organisation 152 - Bob339 Smith339 and Bob340 Smith340'
                        },
                        'id': 'TWF0dGVyVHlwZTo4Nw==',
                        'name': 'Matter 86'
                    }
                }
            ]
        }
    }
}

snapshots['test_matter_report_filter_with_value_error 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNTE=',
                            'name': 'Organisation 155 - Bob345 Smith345 and Bob346 Smith346'
                        },
                        'id': 'TWF0dGVyVHlwZTo5MA==',
                        'name': 'Matter 89'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNTI=',
                            'name': 'Organisation 156 - Bob347 Smith347 and Bob348 Smith348'
                        },
                        'id': 'TWF0dGVyVHlwZTo5MQ==',
                        'name': 'Matter 90'
                    }
                },
                {
                    'node': {
                        'billableStatus': 1,
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNTM=',
                            'name': 'Organisation 157 - Bob349 Smith349 and Bob350 Smith350'
                        },
                        'id': 'TWF0dGVyVHlwZTo5Mg==',
                        'name': 'Matter 91'
                    }
                }
            ]
        }
    }
}

snapshots['test_time_entries_client_name_filter 1'] = {
    'data': {
        'timeEntries': {
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNTY=',
                            'name': 'name name'
                        },
                        'date': '2017-10-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZTox',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZTo5NQ==',
                            'name': 'Matter 94'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjE=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNTY=',
                            'name': 'name name'
                        },
                        'date': '2017-10-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZToy',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZTo5Ng==',
                            'name': 'Matter 95'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNTY=',
                            'name': 'name name'
                        },
                        'date': '2017-10-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZToz',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZTo5Nw==',
                            'name': 'Matter 96'
                        }
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                'hasNextPage': True
            },
            'totalPages': 1
        }
    }
}

snapshots['test_time_entrie_clients_name_filter_with_value_error 1'] = {
    'data': {
        'timeEntries': {
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNjI=',
                            'name': 'name name'
                        },
                        'date': '2017-10-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZTo2',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZToxMDA=',
                            'name': 'Matter 99'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjE=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNjI=',
                            'name': 'name name'
                        },
                        'date': '2017-10-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZTo3',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZToxMDE=',
                            'name': 'Matter 100'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNjI=',
                            'name': 'name name'
                        },
                        'date': '2017-10-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZTo4',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZToxMDI=',
                            'name': 'Matter 101'
                        }
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                'hasNextPage': True
            },
            'totalPages': 1
        }
    }
}

snapshots['test_time_entries_staff_name_filter 1'] = {
    'data': {
        'timeEntries': {
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNjk=',
                            'name': 'Organisation 171 - Bob379 Smith379 and Bob380 Smith380'
                        },
                        'date': '2017-10-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZToxMQ==',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZToxMDU=',
                            'name': 'Matter 104'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjE=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNzE=',
                            'name': 'Organisation 173 - Bob383 Smith383 and Bob384 Smith384'
                        },
                        'date': '2017-10-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZToxMg==',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZToxMDY=',
                            'name': 'Matter 105'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxNzM=',
                            'name': 'Organisation 175 - Bob387 Smith387 and Bob388 Smith388'
                        },
                        'date': '2017-10-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZToxMw==',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZToxMDc=',
                            'name': 'Matter 106'
                        }
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                'hasNextPage': True
            },
            'totalPages': 1
        }
    }
}

snapshots['test_time_entries_staff_name_filter_with_value_error 1'] = {
    'data': {
        'timeEntries': {
            'edges': [
            ],
            'pageInfo': {
                'endCursor': None,
                'hasNextPage': False
            },
            'totalPages': 0
        }
    }
}

snapshots['test_time_entries_date_filter 1'] = {
    'data': {
        'timeEntries': {
            'edges': [
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjA=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxODk=',
                            'name': 'Organisation 191 - Bob419 Smith419 and Bob420 Smith420'
                        },
                        'date': '2012-02-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZToyMQ==',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZToxMTU=',
                            'name': 'Matter 114'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjE=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxOTE=',
                            'name': 'Organisation 193 - Bob423 Smith423 and Bob424 Smith424'
                        },
                        'date': '2012-02-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZToyMg==',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZToxMTY=',
                            'name': 'Matter 115'
                        }
                    }
                },
                {
                    'cursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                    'node': {
                        'client': {
                            'id': 'Q2xpZW50VHlwZToxOTM=',
                            'name': 'Organisation 195 - Bob427 Smith427 and Bob428 Smith428'
                        },
                        'date': '2012-02-20T00:00:00',
                        'description': 'Time Entry description',
                        'id': 'VGltZUVudHJ5VHlwZToyMw==',
                        'matter': {
                            'id': 'TWF0dGVyVHlwZToxMTc=',
                            'name': 'Matter 116'
                        }
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'YXJyYXljb25uZWN0aW9uOjI=',
                'hasNextPage': True
            },
            'totalPages': 1
        }
    }
}

snapshots['test_time_entries_date_filter_with_value_error 1'] = {
    'data': {
        'timeEntries': {
            'edges': [
            ],
            'pageInfo': {
                'endCursor': None,
                'hasNextPage': False
            },
            'totalPages': 0
        }
    }
}
