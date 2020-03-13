import decimal

from graphene.types import Scalar
from graphql.language import ast


class Decimal(Scalar):
    """
    The `Decimal` scalar type represents a python Decimal.
    """
    @staticmethod
    def serialize(dec):
        dec = decimal.Decimal(dec)
        assert isinstance(dec, decimal.Decimal), (
            'Received not compatible Decimal "{}"'.format(repr(dec))
        )
        return format(dec, '.2f')

    @staticmethod
    def parse_value(value):
        return decimal.Decimal(value)

    @classmethod
    def parse_literal(cls, node):
        if isinstance(node, ast.StringValue):
            return cls.parse_value(node.value)
