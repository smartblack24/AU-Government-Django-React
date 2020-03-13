import math

from django.conf import settings

from graphene import Connection, Int


class Connection(Connection):
    total_pages = Int()

    class Meta:
        abstract = True

    def resolve_total_pages(self, info):
        return math.ceil(self.length / settings.GRAPHENE_DEFAULT_PAGE_SIZE)
