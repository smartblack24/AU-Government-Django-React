import decimal

from graphene.types import Scalar
from graphql.language import ast


class HistoricalRecord(Scalar):
    @staticmethod
    def serialize(history):
        try:
            user = history.history_user.full_name
        except AttributeError:
            user = ''

        return {
            'id': "{}-{}".format(
                history.history_object._meta.model_name,
                history.pk
            ),
            'date': str(history.history_date.date()),
            'changeReason': history.history_change_reason,
            'user': user,
        }


class Currency(Scalar):
    '''Currency Scalar Description'''

    @staticmethod
    def serialize(value):
        return decimal.Decimal(value)

    @staticmethod
    def parse_value(value):
        if '$' in str(value):
            return decimal.Decimal(str(value).split('$')[-1])

        return decimal.Decimal(value)

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValue):
            return cls.parse_value(node.value)
