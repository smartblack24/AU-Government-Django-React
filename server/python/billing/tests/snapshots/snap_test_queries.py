# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_standart_disbursements_query 1'] = {
    'data': {
        'standartDisbursements': {
            'edges': [
                {
                    'node': {
                        'gstStatus': 1
                    }
                },
                {
                    'node': {
                        'gstStatus': 1
                    }
                },
                {
                    'node': {
                        'gstStatus': 1
                    }
                }
            ]
        }
    }
}

snapshots['test_time_entries_query 1'] = {
    'data': {
        'timeEntries': {
            'edges': [
                {
                    'node': {
                        'billedValue': 0.0,
                        'cost': '0.00',
                        'entryType': 1,
                        'gstStatus': 0,
                        'gstStatusDisplay': '0',
                        'isBilled': False,
                        'rate': '0.00',
                        'status': 1,
                        'statusDisplay': 'Billable'
                    }
                },
                {
                    'node': {
                        'billedValue': 0.0,
                        'cost': '0.00',
                        'entryType': 1,
                        'gstStatus': 0,
                        'gstStatusDisplay': '0',
                        'isBilled': False,
                        'rate': '0.00',
                        'status': 1,
                        'statusDisplay': 'Billable'
                    }
                },
                {
                    'node': {
                        'billedValue': 0.0,
                        'cost': '1258.50',
                        'entryType': 1,
                        'gstStatus': 0,
                        'gstStatusDisplay': '0',
                        'isBilled': False,
                        'rate': '503.40',
                        'status': 1,
                        'statusDisplay': 'Billable'
                    }
                }
            ]
        }
    }
}

snapshots['test_matters_query 1'] = {
    'data': {
        'matters': {
            'edges': [
                {
                    'node': {
                        'amountOutstanding': '0.00',
                        'billableStatus': 1,
                        'billableStatusDisplay': 'Open',
                        'billingMethod': 2,
                        'conflictStatus': 1,
                        'daysOpen': 0,
                        'isPaid': True,
                        'lastNote': None,
                        'matterStatus': 224,
                        'matterStatusDisplay': 'Matter status 243',
                        'notes': [
                        ],
                        'totalInvoicedValue': '0.00',
                        'totalTimeInvoiced': '0.00',
                        'totalTimeValue': '0.00',
                        'unbilledTime': [
                        ],
                        'wip': '0.00'
                    }
                },
                {
                    'node': {
                        'amountOutstanding': '0.00',
                        'billableStatus': 1,
                        'billableStatusDisplay': 'Open',
                        'billingMethod': 2,
                        'conflictStatus': 1,
                        'daysOpen': 0,
                        'isPaid': True,
                        'lastNote': None,
                        'matterStatus': 225,
                        'matterStatusDisplay': 'Matter status 244',
                        'notes': [
                        ],
                        'totalInvoicedValue': '0.00',
                        'totalTimeInvoiced': '0.00',
                        'totalTimeValue': '0.00',
                        'unbilledTime': [
                        ],
                        'wip': '0.00'
                    }
                },
                {
                    'node': {
                        'amountOutstanding': '0.00',
                        'billableStatus': 1,
                        'billableStatusDisplay': 'Open',
                        'billingMethod': 2,
                        'conflictStatus': 1,
                        'daysOpen': 0,
                        'isPaid': True,
                        'lastNote': None,
                        'matterStatus': 226,
                        'matterStatusDisplay': 'Matter status 245',
                        'notes': [
                        ],
                        'totalInvoicedValue': '0.00',
                        'totalTimeInvoiced': '0.00',
                        'totalTimeValue': '0.00',
                        'unbilledTime': [
                        ],
                        'wip': '0.00'
                    }
                }
            ]
        }
    }
}
