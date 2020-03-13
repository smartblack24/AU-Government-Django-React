from decimal import Decimal

from django.db import models
from django.db.models import (Case, DecimalField, ExpressionWrapper, F, Q, Sum,
                              When)
from django.db.models.functions import Coalesce

TWOPLACES = Decimal(10) ** -2


class TimeEntryQuerySet(models.QuerySet):
    def cost(self, gst=False, billable=False):
        if billable:
            units = 'units'
        else:
            units = 'units_to_bill'

        if gst:
            result = self.aggregate(total=Sum(Case(
                When(Q(entry_type=2) | Q(entry_type=3), then=Case(
                    When(gst_status=1, then=ExpressionWrapper(Coalesce(
                        F('rate'), F('staff_member__rate')) * F(units) + Coalesce(
                        F('rate'), F('staff_member__rate')) * F(units) / 10,
                        output_field=DecimalField())),
                    When(Q(gst_status=2) | Q(gst_status=3), then=ExpressionWrapper(Coalesce(
                        F('rate'), F('staff_member__rate')) * F(units),
                        output_field=DecimalField()))
                )),
                When(entry_type=1, then=Case(
                    When(gst_status=1, then=ExpressionWrapper(Coalesce(
                        F('rate'), F('staff_member__rate')) * F(units) / 10 + (Coalesce(
                            F('rate'), F('staff_member__rate')) * F(units) / 10) / 10,
                        output_field=DecimalField())),
                    When(Q(gst_status=2) | Q(gst_status=3), then=ExpressionWrapper((Coalesce(
                        F('rate'), F('staff_member__rate')) * F(units)) / 10,
                        output_field=DecimalField()))
                ))
            )))
        else:
            result = self.aggregate(total=Sum(Case(
                When(Q(entry_type=2) | Q(entry_type=3), then=ExpressionWrapper(
                    Coalesce(F('rate'), F('staff_member__rate')) *
                    F(units),
                    output_field=DecimalField())),
                When(entry_type=1, then=ExpressionWrapper(Coalesce(
                    F('rate'), F('staff_member__rate')) * F(units) / 10,
                    output_field=DecimalField()))
            )))

        if result['total']:
            return result['total'].quantize(TWOPLACES)

        return Decimal(0)
