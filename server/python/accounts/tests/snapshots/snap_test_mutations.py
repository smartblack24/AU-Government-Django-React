# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_login_mutation 1'] = {
    'data': {
        'login': {
            'errors': [
            ],
            'user': {
                'firstName': 'john13',
                'lastName': 'johnson13'
            }
        }
    }
}

snapshots['test_login_mutation_with_incorrect_password 1'] = {
    'data': {
        'login': {
            'errors': [
                'Email or password is invalid'
            ]
        }
    }
}

snapshots['test_login_mutation_with_incorrect_email 1'] = {
    'data': {
        'login': {
            'errors': [
                'Email or password is invalid'
            ]
        }
    }
}

snapshots['test_register_mutation_with_existing_user 1'] = {
    'data': {
        'register': {
            'errors': [
                'User with the email already exists!'
            ]
        }
    }
}

snapshots['test_register_mutation 1'] = {
    'data': {
        'register': {
            'errors': [
            ]
        }
    }
}

snapshots['test_update_organisation_details_mutation 1'] = {
    'data': {
        'updateOrganisationDetails': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 8,
                    'line': 3
                }
            ],
            'message': "'NoneType' object has no attribute 'user'",
            'path': [
                'updateOrganisationDetails'
            ]
        }
    ]
}

snapshots['test_reset_password 1'] = {
    'data': {
        'resetPassword': {
            'error': ''
        }
    }
}

snapshots['test_update_client_mutation 1'] = {
    'data': {
        'updateClientDetails': {
            'client': None,
            'errors': [
                'Client with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_update_client_mutation2 1'] = {
    'data': {
        'updateClientDetails': {
            'client': None,
            'errors': [
                'Client id must be specified'
            ]
        }
    }
}

snapshots['test_remove_client_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Client with the provided id does not exists'
            ]
        }
    }
}

snapshots['test_update_organisation_details_mutation2 1'] = {
    'data': {
        'updateOrganisationDetails': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 9,
                    'line': 3
                }
            ],
            'message': "'NoneType' object has no attribute 'user'",
            'path': [
                'updateOrganisationDetails'
            ]
        }
    ]
}

snapshots['test_update_organisation_details_mutation3 1'] = {
    'data': {
        'updateOrganisationDetails': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 9,
                    'line': 3
                }
            ],
            'message': "'NoneType' object has no attribute 'user'",
            'path': [
                'updateOrganisationDetails'
            ]
        }
    ]
}

snapshots['test_update_organisation_location_mutation 1'] = {
    'data': {
        'updateOrganisationLocation': {
            'errors': [
            ]
        }
    }
}

snapshots['test_update_organisation_location_mutation2 1'] = {
    'data': {
        'updateOrganisationLocation': {
            'errors': [
                'Organisation with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_update_organisation_location_mutation4 1'] = {
    'data': {
        'updateOrganisationLocation': {
            'errors': [
            ]
        }
    }
}

snapshots['test_update_organisation_location_mutation3 1'] = {
    'data': {
        'updateOrganisationLocation': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_contact_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Contact with the provided id does not exists'
            ]
        }
    }
}

snapshots['test_remove_organisation_mutation 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_organisation_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Organisation with the provided id does not exists'
            ]
        }
    }
}

snapshots['test_update_profile_mutation_without_init_data 1'] = {
    'data': {
        'updateUser': {
            'errors': [
            ],
            'user': {
                'email': 'BobGuyForTest@gmail.com',
                'firstName': 'BobGuyForTest',
                'location': {
                    'address1': 'address12',
                    'address2': 'address12'
                },
                'postalLocation': {
                    'address1': 'address13',
                    'address2': 'address13'
                }
            }
        }
    }
}

snapshots['test_update_profile_mutation_with_init_data 1'] = {
    'data': {
        'updateUser': {
            'errors': [
            ],
            'user': {
                'email': 'john28@example.org',
                'firstName': 'john28',
                'location': {
                    'address1': 'address16',
                    'address2': 'address16'
                },
                'postalLocation': {
                    'address1': 'address16',
                    'address2': 'address16'
                }
            }
        }
    }
}

snapshots['test_update_profile_mutation_with_no_existing_user 1'] = {
    'data': {
        'updateUser': {
            'errors': [
                'User with the provided id does not exist'
            ],
            'user': None
        }
    }
}

snapshots['test_update_contact_mutation_without_contact_id 1'] = {
    'data': {
        'updateContact': {
            'contact': None,
            'errors': [
                'Contact id must be specified'
            ]
        }
    }
}

snapshots['test_login_mutation_with_remember_me_flag 1'] = {
    'data': {
        'login': {
            'errors': [
            ]
        }
    }
}

snapshots['test_register_mutation_without_data 1'] = {
    'data': {
        'register': {
            'errors': [
                'Email must be specified',
                'Password must be specified',
                'First name must be specified',
                'Last name must be specified'
            ]
        }
    }
}

snapshots['test_update_organisations_mutation_without_contact_id 1'] = {
    'data': {
        'updateOrganisations': {
            'errors': [
                'Contact id must be specified'
            ]
        }
    }
}

snapshots['test_update_ralationships_mutation_without_contact_id 1'] = {
    'data': {
        'updateReferrer': {
            'contact': None,
            'errors': [
                'Contact id must be specified'
            ]
        }
    }
}

snapshots['test_reset_password_with_no_exist_user 1'] = {
    'data': {
        'resetPassword': {
            'error': 'User cannot be find!'
        }
    }
}

snapshots['test_check_reset_password 1'] = {
    'data': {
        'checkResetPasswordToken': {
            'error': ''
        }
    }
}

snapshots['test_check_reset_password_with_incorrect_token 1'] = {
    'data': {
        'checkResetPasswordToken': {
            'error': 'Invalid token!'
        }
    }
}

snapshots['test_check_reset_password_with_no_exist_user 1'] = {
    'data': {
        'checkResetPasswordToken': {
            'error': 'User cannot be find!'
        }
    }
}

snapshots['test_update_organisation_location_mutation_without_id 1'] = {
    'data': {
        'updateOrganisationLocation': {
            'errors': [
                'Instance id must be specified'
            ]
        }
    }
}

snapshots['test_send_reset_password_email_with_incorrect_email 1'] = {
    'data': {
        'sendResetPasswordEmail': {
            'error': 'Cannot find user with the provided email!'
        }
    }
}

snapshots['test_send_reset_password_email 1'] = {
    'data': {
        'sendResetPasswordEmail': {
            'error': ''
        }
    }
}

snapshots['test_create_organisation_mutation2 1'] = {
    'data': {
        'createOrganisation': {
            'errors': [
            ],
            'organisation': {
                'clients': {
                    'edges': [
                    ]
                },
                'groupParent': {
                    'id': 'T3JnYW5pc2F0aW9uVHlwZToyNA=='
                },
                'location': {
                    'address1': 'address36',
                    'address2': 'address36',
                    'country': 'Australia',
                    'postCode': '12345',
                    'state': 1,
                    'suburb': 'suburb36'
                },
                'name': 'New Organisation',
                'postalLocation': {
                    'postalAddress1': 'address36',
                    'postalAddress2': 'address36',
                    'postalCountry': 'Australia',
                    'postalPostCode': '12345',
                    'postalState': 1,
                    'postalSuburb': 'suburb36'
                }
            }
        }
    }
}

snapshots['test_create_contact_mutation 1'] = {
    'data': {
        'createContact': {
            'contact': {
                'email': 'Bob38@gmail.com',
                'father': {
                    'fullName': 'Bob39 Smith39',
                    'id': 'Q29udGFjdFR5cGU6MzE='
                },
                'fullName': 'Bob38 Smith38',
                'location': {
                    'address1': 'address17',
                    'address2': 'address17'
                },
                'mobile': '1231231',
                'mother': {
                    'fullName': 'Bob39 Smith39',
                    'id': 'Q29udGFjdFR5cGU6MzE='
                },
                'occupation': 39,
                'organisations': {
                    'edges': [
                        {
                            'node': {
                                'name': 'Organisation 10'
                            }
                        },
                        {
                            'node': {
                                'name': 'Organisation 11'
                            }
                        },
                        {
                            'node': {
                                'name': 'Organisation 12'
                            }
                        }
                    ]
                },
                'postalLocation': {
                    'postalAddress1': 'address17',
                    'postalAddress2': 'address17'
                },
                'referrer': {
                    'fullName': 'Bob39 Smith39',
                    'id': 'Q29udGFjdFR5cGU6MzE='
                },
                'spouse': {
                    'fullName': 'Bob39 Smith39',
                    'id': 'Q29udGFjdFR5cGU6MzE='
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_create_contact_mutation_without_email 1'] = {
    'data': {
        'createContact': {
            'contact': {
                'email': None,
                'fullName': 'Bob40 Smith40',
                'occupation': 41,
                'organisations': {
                    'edges': [
                        {
                            'node': {
                                'name': 'Organisation 13'
                            }
                        },
                        {
                            'node': {
                                'name': 'Organisation 14'
                            }
                        },
                        {
                            'node': {
                                'name': 'Organisation 15'
                            }
                        }
                    ]
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_create_contact_mutation_with_no_existing_spouse 1'] = {
    'data': {
        'createContact': {
            'contact': {
                'email': 'Bob41@gmail.com',
                'fullName': 'Bob41 Smith41',
                'occupation': 1,
                'spouse': None
            },
            'errors': [
                "Can't find spouse with provided id"
            ]
        }
    }
}

snapshots['test_create_contact_mutation2 1'] = {
    'data': {
        'createContact': {
            'errors': [
                'The email already exists'
            ]
        }
    }
}

snapshots['test_update_contact_mutation_with_no_existing_contact 1'] = {
    'data': {
        'updateContact': {
            'contact': None,
            'errors': [
                'User with the specified id does not exist'
            ]
        }
    }
}

snapshots['test_create_organisation_mutation 1'] = {
    'data': {
        'createOrganisation': {
            'errors': [
            ],
            'organisation': {
                'clients': {
                    'edges': [
                        {
                            'node': {
                                'name': 'New Organisation - Bob52 Smith52'
                            }
                        },
                        {
                            'node': {
                                'name': 'New Organisation - Bob53 Smith53'
                            }
                        },
                        {
                            'node': {
                                'name': 'New Organisation - Bob54 Smith54'
                            }
                        }
                    ]
                },
                'contacts': {
                    'edges': [
                        {
                            'node': {
                                'fullName': 'Bob52 Smith52'
                            }
                        },
                        {
                            'node': {
                                'fullName': 'Bob53 Smith53'
                            }
                        },
                        {
                            'node': {
                                'fullName': 'Bob54 Smith54'
                            }
                        }
                    ]
                },
                'name': 'New Organisation'
            }
        }
    }
}

snapshots['test_create_organisation_mutation3 1'] = {
    'data': {
        'createOrganisation': {
            'errors': [
            ],
            'organisation': {
                'clients': {
                    'edges': [
                        {
                            'node': {
                                'name': 'New Organisation - Bob55 Smith55'
                            }
                        },
                        {
                            'node': {
                                'name': 'New Organisation - Bob56 Smith56'
                            }
                        },
                        {
                            'node': {
                                'name': 'New Organisation - Bob57 Smith57'
                            }
                        }
                    ]
                },
                'contacts': {
                    'edges': [
                        {
                            'node': {
                                'fullName': 'Bob55 Smith55'
                            }
                        },
                        {
                            'node': {
                                'fullName': 'Bob56 Smith56'
                            }
                        },
                        {
                            'node': {
                                'fullName': 'Bob57 Smith57'
                            }
                        }
                    ]
                },
                'groupParent': {
                    'id': 'T3JnYW5pc2F0aW9uVHlwZToyNg=='
                },
                'name': 'New Organisation'
            }
        }
    }
}

snapshots['test_update_organisations_mutation 1'] = {
    'data': {
        'updateOrganisations': {
            'errors': [
            ]
        }
    }
}

snapshots['test_update_organisations_mutation_with_no_existing_user 1'] = {
    'data': {
        'updateOrganisations': {
            'errors': [
                'Contact with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_update_organisations_mutation_with_init_organisations 1'] = {
    'data': {
        'updateOrganisations': {
            'errors': [
            ]
        }
    }
}

snapshots['test_update_organisations_mutation_with_delete_exception 1'] = {
    'data': {
        'updateOrganisations': {
            'errors': [
                'T3JnYW5pc2F0aW9uVHlwZTozNg==',
                'Some Clients cannot be deleted because                         they have a Matter assigned to them'
            ]
        }
    }
}

snapshots['test_update_organisation_details_mutation4 1'] = {
    'data': {
        'updateOrganisationDetails': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 13,
                    'line': 3
                }
            ],
            'message': "'NoneType' object has no attribute 'user'",
            'path': [
                'updateOrganisationDetails'
            ]
        }
    ]
}

snapshots['test_update_ralationships_mutation 1'] = {
    'data': {
        'updateReferrer': {
            'contact': {
                'id': 'Q29udGFjdFR5cGU6NjE='
            },
            'errors': [
            ],
            'father': {
                'id': 'Q29udGFjdFR5cGU6NjA='
            },
            'mother': {
                'id': 'Q29udGFjdFR5cGU6NjA='
            },
            'referrer': {
                'id': 'Q29udGFjdFR5cGU6NjA='
            },
            'spouse': {
                'id': 'Q29udGFjdFR5cGU6NjA='
            }
        }
    }
}

snapshots['test_update_ralationships_mutation_with_init_relations 1'] = {
    'data': {
        'updateReferrer': {
            'contact': {
                'id': 'Q29udGFjdFR5cGU6NjM='
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_update_ralationships_mutation_with_no_exist_contact 1'] = {
    'data': {
        'updateReferrer': {
            'contact': None,
            'errors': [
                'Contact with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_update_ralationships_mutation_with_no_exist_spouse 1'] = {
    'data': {
        'updateReferrer': {
            'contact': None,
            'errors': [
                'Contact with the provided id does not exist'
            ],
            'spouse': None
        }
    }
}

snapshots['test_update_ralationships_mutation_with_no_exist_mother 1'] = {
    'data': {
        'updateReferrer': {
            'contact': None,
            'errors': [
                'Contact with the provided id does not exist'
            ],
            'mother': None,
            'spouse': None
        }
    }
}

snapshots['test_update_ralationships_mutation_with_no_exist_father 1'] = {
    'data': {
        'updateReferrer': {
            'contact': None,
            'errors': [
                'Contact with the provided id does not exist'
            ],
            'father': None,
            'mother': None,
            'spouse': None
        }
    }
}

snapshots['test_update_ralationships_mutation_with_no_exist_referrer 1'] = {
    'data': {
        'updateReferrer': {
            'contact': None,
            'errors': [
                'Contact with the provided id does not exist'
            ],
            'referrer': None
        }
    }
}

snapshots['test_update_organisation_associaton_mutation 1'] = {
    'data': {
        'updateOrganisationAssociation': {
            'errors': [
            ]
        }
    }
}

snapshots['test_update_organisation_associaton_mutation_without_id 1'] = {
    'data': {
        'updateOrganisationAssociation': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 11,
                    'line': 3
                }
            ],
            'message': "local variable 'organisation' referenced before assignment",
            'path': [
                'updateOrganisationAssociation'
            ]
        }
    ]
}

snapshots['test_update_organisation_associaton_mutation2 1'] = {
    'data': {
        'updateOrganisationAssociation': {
            'errors': [
                'Organisation with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_update_organisation_associaton_mutation3 1'] = {
    'data': {
        'updateOrganisationAssociation': {
            'errors': [
            ]
        }
    }
}

snapshots['test_update_organisation_associaton_mutation4 1'] = {
    'data': {
        'updateOrganisationAssociation': {
            'errors': [
            ]
        }
    }
}

snapshots['test_update_organisation_associaton_mutation_with_delete_exception 1'] = {
    'data': {
        'updateOrganisationAssociation': {
            'errors': [
                '86',
                '87',
                'Some Clients cannot be deleted because                         they have a Matter assigned to them'
            ]
        }
    }
}

snapshots['test_create_client_mutation 1'] = {
    'data': {
        'createClient': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6OTM=',
                    'mobile': '1231231'
                },
                'isActive': True,
                'office': {
                    'id': '31'
                },
                'organisation': {
                    'id': 'T3JnYW5pc2F0aW9uVHlwZTo1Ng==',
                    'mainLine': None
                },
                'secondContact': {
                    'id': 'Q29udGFjdFR5cGU6OTQ=',
                    'mobile': ''
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_create_client_mutation2 1'] = {
    'data': {
        'createClient': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6OTk=',
                    'mobile': '1231231'
                },
                'isActive': True,
                'office': {
                    'id': '32'
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_create_client_mutation3 1'] = {
    'data': {
        'createClient': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6MTAw',
                    'mobile': '1231231'
                },
                'isActive': True,
                'office': {
                    'id': '33'
                },
                'secondContact': {
                    'id': 'Q29udGFjdFR5cGU6MTAx',
                    'mobile': '1231231'
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_create_client_mutation4 1'] = {
    'data': {
        'createClient': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6MTA2',
                    'mobile': '1231231'
                },
                'isActive': True,
                'office': {
                    'id': '34'
                },
                'organisation': {
                    'id': 'T3JnYW5pc2F0aW9uVHlwZTo2MQ==',
                    'mainLine': None
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_create_client_mutation5 1'] = {
    'data': {
        'createClient': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6MTA3',
                    'mobile': '1231231'
                },
                'isActive': True,
                'office': {
                    'id': '35'
                },
                'organisation': {
                    'id': 'T3JnYW5pc2F0aW9uVHlwZTotMQ==',
                    'mainLine': None
                },
                'secondContact': None
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_create_client_mutation6 1'] = {
    'data': {
        'createClient': {
            'client': {
                'contact': None,
                'isActive': True,
                'office': None,
                'secondContact': None
            },
            'errors': [
                'Contact with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_create_client_mutation7 1'] = {
    'data': {
        'createClient': {
            'client': None,
            'errors': [
                'Contact id must be specified'
            ]
        }
    }
}

snapshots['test_update_client_mutation3 1'] = {
    'data': {
        'updateClientDetails': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6MTE2',
                    'mobile': '1231231',
                    'role': 'OtherRole'
                },
                'id': 'Q2xpZW50VHlwZTo2MQ==',
                'isActive': True,
                'office': {
                    'id': '38'
                },
                'organisation': {
                    'id': 'T3JnYW5pc2F0aW9uVHlwZTo2NQ==',
                    'mainLine': '2222222222',
                    'website': 'www.hhh.com'
                },
                'secondContact': {
                    'id': 'Q29udGFjdFR5cGU6MTE3',
                    'mobile': '1231231',
                    'role': 'Myrole'
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_update_client_mutation4 1'] = {
    'data': {
        'updateClientDetails': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6MTE4',
                    'mobile': '1231231',
                    'role': None
                },
                'id': 'Q2xpZW50VHlwZTo2Mg==',
                'isActive': True,
                'office': {
                    'id': '39'
                },
                'organisation': {
                    'id': 'T3JnYW5pc2F0aW9uVHlwZTo2Ng==',
                    'mainLine': None,
                    'website': None
                },
                'secondContact': {
                    'id': 'Q29udGFjdFR5cGU6MTE5',
                    'mobile': '1231231',
                    'role': None
                }
            },
            'errors': [
                'Organisation with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_update_client_mutation5 1'] = {
    'data': {
        'updateClientDetails': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6MTIw',
                    'mobile': '1231231',
                    'role': 'OtherRole'
                },
                'id': 'Q2xpZW50VHlwZTo2Mw==',
                'isActive': True,
                'office': {
                    'id': '40'
                },
                'organisation': {
                    'id': 'T3JnYW5pc2F0aW9uVHlwZTo2Nw==',
                    'mainLine': '2222222222',
                    'website': 'www.hhh.com'
                },
                'secondContact': None
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_update_client_mutation6 1'] = {
    'data': {
        'updateClientDetails': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6MTIy',
                    'mobile': '1231231',
                    'role': None
                },
                'id': 'Q2xpZW50VHlwZTo2NA==',
                'isActive': True,
                'office': {
                    'id': '41'
                },
                'organisation': {
                    'id': 'T3JnYW5pc2F0aW9uVHlwZTo2OA==',
                    'mainLine': '2222222222',
                    'website': 'www.hhh.com'
                },
                'secondContact': {
                    'id': 'Q29udGFjdFR5cGU6MTIz',
                    'mobile': '1231231',
                    'role': None
                }
            },
            'errors': [
                'Contact with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_update_client_mutation7 1'] = {
    'data': {
        'updateClientDetails': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6MTI0',
                    'mobile': '1231231',
                    'role': None
                },
                'id': 'Q2xpZW50VHlwZTo2NQ==',
                'isActive': True,
                'office': {
                    'id': '42'
                }
            },
            'errors': [
                'Contact with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_update_client_mutation8 1'] = {
    'data': {
        'updateClientDetails': {
            'client': {
                'contact': {
                    'id': 'Q29udGFjdFR5cGU6MTI2',
                    'mobile': '1231231',
                    'role': None
                },
                'id': 'Q2xpZW50VHlwZTo2Ng==',
                'isActive': True,
                'office': {
                    'id': '43'
                },
                'organisation': {
                    'id': 'T3JnYW5pc2F0aW9uVHlwZTo3MA==',
                    'mainLine': None,
                    'website': None
                }
            },
            'errors': [
                'Contact with the provided id does not exist'
            ]
        }
    }
}

snapshots['test_remove_client_mutation 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_client_mutation3 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'The Client cannot be deleted because it has a Matter assigned to'
            ]
        }
    }
}

snapshots['test_remove_contact_mutation 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_contact_mutation3 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'The Contact cannot be deleted because it has a relation to a             Client'
            ]
        }
    }
}

snapshots['test_remove_organisation_mutation3 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'The Organisation cannot be deleted because it has a relation to a Client'
            ]
        }
    }
}

snapshots['test_create_contact_mutation3 1'] = {
    'data': {
        'createContact': {
            'contact': None,
            'errors': [
                'First name must be specified',
                'Last name must be specified'
            ]
        }
    }
}

snapshots['test_update_contact_mutation 1'] = {
    'data': {
        'updateContact': {
            'contact': {
                'email': 'new@email.com',
                'firstName': 'John',
                'location': {
                    'address1': 'address25',
                    'address2': 'address25'
                },
                'occupation': 47,
                'organisations': {
                    'edges': [
                        {
                            'node': {
                                'name': 'Organisation 17'
                            }
                        },
                        {
                            'node': {
                                'name': 'Organisation 18'
                            }
                        },
                        {
                            'node': {
                                'name': 'Organisation 19'
                            }
                        }
                    ]
                },
                'postalLocation': {
                    'postalAddress1': 'address25',
                    'postalAddress2': 'address25'
                }
            },
            'errors': [
            ]
        }
    }
}

snapshots['test_update_contact_mutation_with_init_location 1'] = {
    'data': {
        'updateContact': {
            'contact': {
                'email': 'new@email.com',
                'firstName': 'John',
                'location': {
                    'address1': 'address32',
                    'address2': 'address32'
                },
                'postalLocation': {
                    'postalAddress1': 'address32',
                    'postalAddress2': 'address32'
                }
            },
            'errors': [
            ]
        }
    }
}
