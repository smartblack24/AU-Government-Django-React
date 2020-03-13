# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_create_matter_mutation 1'] = {
    'data': {
        'createMatter': {
            'errors': [
            ],
            'matter': {
                'name': 'Matter 20'
            }
        }
    }
}

snapshots['test_update_matter_mutation 1'] = {
    'data': {
        'updateMatter': {
            'errors': [
            ],
            'matter': {
                'description': 'New matter description',
                'name': 'New matter name'
            }
        }
    }
}

snapshots['test_create_time_entry_mutation 1'] = {
    'data': {
        'createTimeEntry': {
            'errors': [
            ],
            'timeEntry': {
                'client': {
                    'name': 'Organisation 158 - Bob300 Smith300 and Bob301 Smith301'
                },
                'description': 'Time Entry description',
                'matter': {
                    'name': 'Matter 53'
                },
                'rate': '300.00',
                'staffMember': {
                    'fullName': 'john182 johnson182'
                },
                'units': 20.0,
                'unitsToBill': 20.0
            }
        }
    }
}

snapshots['test_update_time_entry_mutation 1'] = {
    'data': {
        'updateTimeEntry': {
            'errors': [
            ],
            'timeEntry': {
                'client': {
                    'name': 'Organisation 167 - Bob318 Smith318 and Bob319 Smith319'
                },
                'description': 'New Time Entry description',
                'matter': {
                    'name': 'Matter 57'
                },
                'rate': '125.00',
                'staffMember': {
                    'fullName': 'john194 johnson194'
                },
                'units': 1243.0,
                'unitsToBill': 1243.0
            }
        }
    }
}

snapshots['test_create_time_entry_mutation2 1'] = {
    'data': {
        'createTimeEntry': {
            'errors': [
            ],
            'timeEntry': {
                'client': {
                    'name': 'Organisation 162 - Bob308 Smith308 and Bob309 Smith309'
                },
                'description': 'Time Entry description',
                'matter': {
                    'name': 'Matter 55'
                },
                'rate': '300.00',
                'staffMember': {
                    'fullName': 'john188 johnson188'
                },
                'units': 20.0,
                'unitsToBill': 0.0
            }
        }
    }
}

snapshots['test_update_time_entry_mutation2 1'] = {
    'data': {
        'updateTimeEntry': {
            'errors': [
            ],
            'timeEntry': {
                'client': {
                    'name': 'Organisation 169 - Bob322 Smith322 and Bob323 Smith323'
                },
                'description': 'New Time Entry description',
                'matter': {
                    'name': 'Matter 58'
                },
                'rate': '125.00',
                'staffMember': {
                    'fullName': 'john197 johnson197'
                },
                'units': 1243.0,
                'unitsToBill': 0.0
            }
        }
    }
}

snapshots['test_create_matter_mutation2 1'] = {
    'data': {
        'createMatter': {
            'errors': [
                'Client with the provided id does not exist'
            ],
            'matter': None
        }
    }
}

snapshots['test_create_matter_mutation3 1'] = {
    'data': {
        'createMatter': {
            'errors': [
            ],
            'matter': {
                'name': 'Matter 22'
            }
        }
    }
}

snapshots['test_create_matter_mutation4 1'] = {
    'data': {
        'createMatter': {
            'errors': [
            ],
            'matter': {
                'name': 'Matter 23'
            }
        }
    }
}

snapshots['test_update_matter_mutation2 1'] = {
    'data': {
        'updateMatter': {
            'errors': [
            ],
            'matter': {
                'description': 'New matter description',
                'name': 'New matter name'
            }
        }
    }
}

snapshots['test_update_matter_mutation3 1'] = {
    'data': {
        'updateMatter': {
            'errors': [
                'Matter with the provided id does not exist'
            ],
            'matter': None
        }
    }
}

snapshots['test_update_matter_mutation4 1'] = {
    'data': {
        'updateMatter': {
            'errors': [
            ],
            'matter': {
                'description': 'New matter description',
                'name': 'New matter name'
            }
        }
    }
}

snapshots['test_update_matter_mutation5 1'] = {
    'data': {
        'updateMatter': {
            'errors': [
            ],
            'matter': {
                'description': 'New matter description',
                'name': 'New matter name'
            }
        }
    }
}

snapshots['test_update_note_mutation 1'] = {
    'data': {
        'updateNote': {
            'errors': [
            ],
            'note': {
                'text': 'note',
                'user': {
                    'fullName': 'john223 johnson223',
                    'id': 'VXNlclR5cGU6MjA0'
                }
            }
        }
    }
}

snapshots['test_update_note_mutation2 1'] = {
    'data': {
        'updateNote': {
            'errors': [
                'User does not exist!'
            ],
            'note': None
        }
    }
}

snapshots['test_update_note_mutation3 1'] = {
    'data': {
        'updateNote': {
            'errors': [
                'Note id must be specified'
            ],
            'note': None
        }
    }
}

snapshots['test_update_note_mutation4 1'] = {
    'data': {
        'updateNote': {
            'errors': [
                'Note with the provided id does not exist'
            ],
            'note': None
        }
    }
}

snapshots['test_update_create_matter_note_mutation 1'] = {
    'data': {
        'createNote': {
            'errors': [
            ],
            'note': {
                'id': '2'
            }
        }
    }
}

snapshots['test_update_create_matter_note_mutation2 1'] = {
    'data': {
        'createNote': None
    }
}

snapshots['test_update_create_contact_note_mutation 1'] = {
    'data': {
        'createNote': {
            'errors': [
            ],
            'note': {
                'id': '4'
            }
        }
    }
}

snapshots['test_update_create_contact_note_mutation2 1'] = {
    'data': {
        'createNote': {
            'errors': [
                'Contact with the provided id does not exist'
            ],
            'note': None
        }
    }
}

snapshots['test_update_matter_mutation6 1'] = {
    'data': {
        'updateMatter': {
            'errors': [
            ],
            'matter': {
                'description': 'New matter description',
                'name': 'New matter name'
            }
        }
    }
}

snapshots['test_update_matter_mutation7 1'] = {
    'data': {
        'updateMatter': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 3
                }
            ],
            'message': 'day is out of range for month',
            'path': [
                'updateMatter'
            ]
        }
    ]
}

snapshots['test_update_matter_mutation8 1'] = {
    'data': {
        'updateMatter': {
            'errors': [
                'The matter cannot be closed!'
            ],
            'matter': {
                'description': 'New matter description',
                'name': 'New matter name'
            }
        }
    }
}

snapshots['test_create_time_entry_mutation3 1'] = {
    'data': {
        'createTimeEntry': {
            'errors': [
                'Client with the provided id does not exist'
            ],
            'timeEntry': None
        }
    }
}

snapshots['test_update_time_entry_mutation3 1'] = {
    'data': {
        'updateTimeEntry': {
            'errors': [
                'Client with the provided id does not exist'
            ],
            'timeEntry': None
        }
    }
}

snapshots['test_remove_matter_mutation 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_matter_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Matter with the provided id does not exists'
            ]
        }
    }
}

snapshots['test_remove_matter_mutation3 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'The Matter cannot be deleted because it has a recorded time'
            ]
        }
    }
}

snapshots['test_remove_time_entry_mutation 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_time_entry_mutation3 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'TimeEntry with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_remove_disbursement_mutation 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_disbursement_mutation3 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Disbursement with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_remove_time_entry_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                "You can't delete a billed time entry!"
            ]
        }
    }
}

snapshots['test_remove_disbursement_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                "You can't delete a billed disbursement!"
            ]
        }
    }
}
