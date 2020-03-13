# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_invoices_query 1'] = {
    'data': {
        'invoices': {
            'edges': [
                {
                    'node': {
                        'billingMethod': 1,
                        'canSendXero': False,
                        'dueDate': '2019-01-31',
                        'firstReminder': False,
                        'fixedPriceValue': '0.00',
                        'friendlyReminder': False,
                        'history': [
                            {
                                'changeReason': 'Invoice was created',
                                'date': '2019-01-17',
                                'id': 'invoice-109',
                                'user': ''
                            }
                        ],
                        'isInXero': False,
                        'isPaid': True,
                        'netOutstanding': '0.00',
                        'number': '12310',
                        'receivedPayments': '0.00',
                        'secondReminder': False,
                        'statusDisplay': 'Invoice status 53',
                        'timeEntries': {
                            'edges': [
                            ]
                        },
                        'timeEntryValue': '0.00',
                        'totalBilledValue': '0.00',
                        'valueExGst': '0.00',
                        'valueInclGst': '0.00'
                    }
                },
                {
                    'node': {
                        'billingMethod': 1,
                        'canSendXero': False,
                        'dueDate': '2019-01-31',
                        'firstReminder': False,
                        'fixedPriceValue': '0.00',
                        'friendlyReminder': False,
                        'history': [
                            {
                                'changeReason': 'Invoice was created',
                                'date': '2019-01-17',
                                'id': 'invoice-110',
                                'user': ''
                            }
                        ],
                        'isInXero': False,
                        'isPaid': True,
                        'netOutstanding': '0.00',
                        'number': '43224',
                        'receivedPayments': '0.00',
                        'secondReminder': False,
                        'statusDisplay': 'Invoice status 54',
                        'timeEntries': {
                            'edges': [
                            ]
                        },
                        'timeEntryValue': '0.00',
                        'totalBilledValue': '0.00',
                        'valueExGst': '0.00',
                        'valueInclGst': '0.00'
                    }
                },
                {
                    'node': {
                        'billingMethod': 1,
                        'canSendXero': False,
                        'dueDate': '2019-01-31',
                        'firstReminder': False,
                        'fixedPriceValue': '0.00',
                        'friendlyReminder': False,
                        'history': [
                            {
                                'changeReason': 'Invoice was created',
                                'date': '2019-01-17',
                                'id': 'invoice-111',
                                'user': ''
                            }
                        ],
                        'isInXero': False,
                        'isPaid': True,
                        'netOutstanding': '0.00',
                        'number': '32334',
                        'receivedPayments': '0.00',
                        'secondReminder': False,
                        'statusDisplay': 'Invoice status 55',
                        'timeEntries': {
                            'edges': [
                            ]
                        },
                        'timeEntryValue': '0.00',
                        'totalBilledValue': '0.00',
                        'valueExGst': '0.00',
                        'valueInclGst': '0.00'
                    }
                }
            ]
        }
    }
}

snapshots['test_invoices_query_with_incorrect_due_date 1'] = {
    'data': {
        'invoices': {
            'edges': [
                {
                    'node': {
                        'firstReminder': False,
                        'friendlyReminder': False,
                        'secondReminder': False
                    }
                },
                {
                    'node': {
                        'firstReminder': False,
                        'friendlyReminder': False,
                        'secondReminder': False
                    }
                }
            ]
        }
    }
}
