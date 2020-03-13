from datetime import datetime
from functools import reduce

from accounts.models import User
from sitename.utils import render_to_pdf
from billing.models import Matter
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from graphql_relay.node.node import from_global_id


class MatterReportPDF(View):
    def get(self, request, *args, **kwargs):
        user_id = from_global_id(kwargs.get('user_id'))[1]
        billable_status = kwargs.get('billable_status')
        user = get_object_or_404(User, pk=user_id)
        matters = []

        if not billable_status:
            matters = Matter.objects.filter(
                Q(manager=user) |
                Q(assistant=user)
            ).order_by('matter_status', 'client')
        elif billable_status:
            matters = Matter.objects.filter(
                Q(manager=user) |
                Q(assistant=user),
                billable_status=billable_status
            ).order_by('matter_status', 'client')

        total_time_invoiced = reduce(
            (lambda x, y: x + y.total_time_invoiced()), matters, 0)

        total_time_value = reduce(
            (lambda x, y: x + y.total_time_value), matters, 0)

        total_wip = reduce((lambda x, y: x + y.wip), matters, 0)

        if not billable_status:
            billable_status = 'All'
        elif int(billable_status) == 1:
            billable_status = 'Open'
        elif int(billable_status) == 2:
            billable_status = 'Suspended'
        elif int(billable_status) == 3:
            billable_status = 'Closed'

        data = {
            'matters': matters,
            'staff': user.full_name,
            'date': datetime.now(),
            'total_time_invoiced': total_time_invoiced,
            'total_time_value': total_time_value,
            'total_wip': total_wip,
            'billable_status': billable_status,
        }
        pdf = render_to_pdf('pdf/my_matter_report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class PrincipalReportPDF(View):
    def get(self, request, *args, **kwargs):
        user_id = from_global_id(kwargs.get('user_id'))[1]
        billable_status = kwargs.get('billable_status')
        user = get_object_or_404(User, pk=user_id)
        matters = []

        if not billable_status:
            matters = Matter.objects.filter(
                principal=user
            ).order_by('matter_status', 'client')
        elif billable_status:
            matters = Matter.objects.filter(
                principal=user,
                billable_status=billable_status
            ).order_by('matter_status', 'client')

        total_time_invoiced = reduce(
            (lambda x, y: x + y.total_time_invoiced()), matters, 0)

        total_time_value = reduce(
            (lambda x, y: x + y.total_time_value), matters, 0)

        total_wip = reduce((lambda x, y: x + y.wip), matters, 0)

        if not billable_status:
            billable_status = 'All'
        elif int(billable_status) == 1:
            billable_status = 'Open'
        elif int(billable_status) == 2:
            billable_status = 'Suspended'
        elif int(billable_status) == 3:
            billable_status = 'Closed'

        data = {
            'matters': matters,
            'staff': user.full_name,
            'date': datetime.now(),
            'total_time_invoiced': total_time_invoiced,
            'total_time_value': total_time_value,
            'total_wip': total_wip,
            'billable_status': billable_status,
        }
        pdf = render_to_pdf('pdf/my_matter_report.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
