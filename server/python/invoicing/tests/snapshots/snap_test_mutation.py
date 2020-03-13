# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_check_for_existence_create_invoice_mutation 1'] = {
    'data': {
        'createInvoice': {
            'errors': [
                'Matter with the provided id does not exist'
            ],
            'invoice': None
        }
    }
}

snapshots['test_check_for_existence_update_invoice_info_mutation 1'] = {
    'data': {
        'updateInvoiceInfo': {
            'errors': [
                'Client with the provided id does not exist'
            ],
            'invoice': None
        }
    }
}

snapshots['test_remove_time_record_mutation 1'] = {
    'data': {
        'removeTimeRecord': {
            'errors': [
            ]
        }
    }
}

snapshots['test_check_for_existence_remove_time_record_mutation 1'] = {
    'data': {
        'removeTimeRecord': {
            'errors': [
                "local variable 'time_record_model' referenced before assignment"
            ]
        }
    }
}

snapshots['test_check_for_existence_add_payment_mutation 1'] = {
    'data': {
        'addPayment': {
            'errors': [
                'Invoice with the provided id does not exist'
            ],
            'payment': None
        }
    }
}

snapshots['test_remove_fixed_price_item_mutation 1'] = {
    'data': {
        'removeFixedPriceItem': {
            'errors': [
            ],
            'invoice': None
        }
    }
}

snapshots['test_remove_fixed_price_item_mutation2 1'] = {
    'data': {
        'removeFixedPriceItem': {
            'errors': [
                'Fixed price item with provided id does not exist'
            ],
            'invoice': None
        }
    }
}

snapshots['test_update_fixed_price_item_mutation 1'] = {
    'data': {
        'updateFixedPriceItem': {
            'invoice': None
        }
    }
}

snapshots['test_remove_invoice_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Invoice with the provided id does not exists'
            ]
        }
    }
}

snapshots['test_update_fixed_price_item_mutation2 1'] = {
    'data': {
        'updateFixedPriceItem': {
            'invoice': None
        }
    }
}

snapshots['test_create_fixed_price_item_mutation2 1'] = {
    'data': {
        'createFixedPriceItem': {
            'invoice': None
        }
    }
}

snapshots['test_remove_payment_mutation2 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'Payment with the provided id does not exists'
            ]
        }
    }
}

snapshots['test_create_invoice_mutation 1'] = {
    'data': {
        'createInvoice': {
            'errors': [
            ],
            'invoice': {
                'number': None
            }
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 15,
                    'line': 6
                }
            ],
            'message': 'string index out of range',
            'path': [
                'createInvoice',
                'invoice',
                'number'
            ]
        }
    ]
}

snapshots['test_update_invoice_info_mutation 1'] = {
    'data': {
        'updateInvoiceInfo': {
            'errors': [
            ],
            'invoice': {
                'number': None
            }
        }
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 19,
                    'line': 6
                }
            ],
            'message': 'string index out of range',
            'path': [
                'updateInvoiceInfo',
                'invoice',
                'number'
            ]
        }
    ]
}

snapshots['test_add_payment_mutation 1'] = {
    'data': {
        'addPayment': {
            'errors': [
            ],
            'payment': {
                'id': '3'
            }
        }
    }
}

snapshots['test_create_fixed_price_item_mutation 1'] = {
    'data': {
        'createFixedPriceItem': {
            'invoice': {
                'id': 'SW52b2ljZVR5cGU6MTE='
            }
        }
    }
}

snapshots['test_remove_invoice_mutation 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_invoice_mutation3 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'You do not have a permission to delete an invoice!'
            ]
        }
    }
}

snapshots['test_remove_invoice_mutation4 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_payment_mutation 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
            ]
        }
    }
}

snapshots['test_remove_payment_mutation3 1'] = {
    'data': {
        'removeInstance': {
            'errors': [
                'You do not have a permission to delete a payment!'
            ]
        }
    }
}
