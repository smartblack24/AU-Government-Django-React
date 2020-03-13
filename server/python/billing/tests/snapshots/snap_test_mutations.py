# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

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

snapshots['test_remove_matter_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Matter with the provided id does not exists'
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

snapshots['test_remove_disbursement_mutation3 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Disbursement with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_create_matter_mutation 1'] = {
    'data': {
        'createMatter': {
            'errors': [
            ],
            'matter': {
                'name': 'Matter 141'
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
                'name': 'Matter 143'
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
                'name': 'Matter 144'
            }
        }
    }
}

snapshots['test_create_time_entry_mutation 1'] = {
    'data': {
        'createTimeEntry': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 3
                }
            ],
            'message': "time data '12:00' does not match format '%I:%M %p'",
            'path': [
                'createTimeEntry'
            ]
        }
    ]
}

snapshots['test_create_time_entry_mutation2 1'] = {
    'data': {
        'createTimeEntry': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 3
                }
            ],
            'message': "time data '12:00' does not match format '%I:%M %p'",
            'path': [
                'createTimeEntry'
            ]
        }
    ]
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

snapshots['test_update_time_entry_mutation 1'] = {
    'data': {
        'updateTimeEntry': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 3
                }
            ],
            'message': "time data '12:00' does not match format '%I:%M %p'",
            'path': [
                'updateTimeEntry'
            ]
        }
    ]
}

snapshots['test_update_time_entry_mutation2 1'] = {
    'data': {
        'updateTimeEntry': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 3
                }
            ],
            'message': "time data '12:00' does not match format '%I:%M %p'",
            'path': [
                'updateTimeEntry'
            ]
        }
    ]
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

snapshots['test_update_create_matter_note_mutation 1'] = {
    'data': {
        'createNote': {
            'errors': [
            ],
            'note': {
                'id': '12'
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
                'id': '14'
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

snapshots['test_update_note_mutation 1'] = {
    'data': {
        'updateNote': {
            'errors': [
            ],
            'note': {
                'text': 'note',
                'user': {
                    'fullName': 'john557 johnson557',
                    'id': 'VXNlclR5cGU6NDg3'
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

snapshots['test_remove_matter_mutation 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
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

snapshots['test_remove_time_entry_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                "You can't delete a billed time entry!"
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

snapshots['test_remove_disbursement_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                "You can't delete a billed disbursement!"
            ]
        }
    }
}

snapshots['test_remove_note_mutation 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_note_mutation_without_permission 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'You do not have a permission to delete a note!'
            ]
        }
    }
}

snapshots['test_remove_note_mutation_with_incorrect_id 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Note with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_create_lead_mutation 1'] = {
    'data': {
        'createMatter': {
            'errors': [
            ],
            'matter': {
                'name': 'lead name'
            }
        }
    }
}

snapshots['test_create_lead_mutation2 1'] = {
    'data': {
        'createMatter': {
            'errors': [
            ],
            'matter': {
                'name': 'lead name 2'
            }
        }
    }
}

snapshots['test_create_lead_mutation3 1'] = {
    'data': {
        'createMatter': {
            'errors': [
            ],
            'matter': {
                'name': 'lead name 3'
            }
        }
    }
}

snapshots['test_create_lead_mutation4 1'] = {
    'data': {
        'createMatter': {
            'errors': [
            ],
            'matter': {
                'name': 'lead name'
            }
        }
    }
}

snapshots['test_update_lead_mutation 1'] = {
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

snapshots['test_create_matter_mutation5 1'] = {
    'data': {
        'createMatter': {
            'errors': [
            ],
            'matter': {
                'name': 'Matter 145'
            }
        }
    }
}

snapshots['test_update_lead_mutation2 1'] = {
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

snapshots['test_update_lead_mutation3 1'] = {
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
            'message': 'Unknown string format',
            'path': [
                'updateMatter'
            ]
        }
    ]
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

snapshots['test_lost 1'] = {
    'data': {
        'lostMatter': {
            'errors': [
            ]
        }
    }
}

snapshots['test_lost2 1'] = {
    'data': {
        'lostMatter': {
            'errors': [
                'Matter matching query does not exist.'
            ]
        }
    }
}

snapshots['test_won 1'] = {
    'data': {
        'winMatter': {
            'errors': [
            ]
        }
    }
}

snapshots['test_won2 1'] = {
    'data': {
        'winMatter': {
            'errors': [
                'Matter matching query does not exist.'
            ]
        }
    }
}
