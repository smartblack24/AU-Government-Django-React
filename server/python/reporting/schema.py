import calendar
from datetime import date, datetime, timedelta
from decimal import Decimal
from functools import reduce

import graphene
from accounts.models import Client, User
from sitename.decorators import login_required
from billing.models import MATTER_STATUSES, HistoricalMatter, Matter, TimeEntry
from core.scalars import Decimal as DecimalType
from dateutil import parser
from django.db.models import Case, IntegerField, Max, Min, Q, Sum, When
from graphql_relay.node.node import from_global_id
from invoicing.models import Invoice


class InvoiceReportType(graphene.ObjectType):
    id = graphene.ID()
    month = graphene.String()
    total_amount = DecimalType()
    total_outstanding = DecimalType()
    average_amount = DecimalType()
    average_outstanding = DecimalType()


class YearMatterType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    count = graphene.Float()


class MatterYearReportType(graphene.ObjectType):
    id = graphene.ID()
    years = graphene.List(YearMatterType)
    month = graphene.String()


class ClientValueReportType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    value = DecimalType()


class WeekendReportType(graphene.ObjectType):
    id = graphene.ID()
    date = graphene.String()
    count = graphene.Int()


class StaffReportType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    count = graphene.Int()


class ByStaffReportType(graphene.ObjectType):
    id = graphene.ID()
    date = graphene.String()
    staff_members = graphene.List(StaffReportType)


class MatterStatusReportType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    count = graphene.Int()


class OpenMattersReportType(graphene.ObjectType):
    id = graphene.ID()
    staff_member = graphene.String()
    matter_statuses = graphene.List(MatterStatusReportType)


class EffectiveRateReportType(graphene.ObjectType):
    id = graphene.ID()
    date = graphene.String()
    value = graphene.Float()


class ClientInvoiceValueType(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    count = graphene.Int()


class Query:
    average_invoice_reports = graphene.List(
        InvoiceReportType,
        from_date=graphene.String(),
        to_date=graphene.String(),
    )
    matters_per_year_reports = graphene.List(MatterYearReportType)
    client_value_reports = graphene.List(
        ClientValueReportType,
        from_date=graphene.String(),
        to_date=graphene.String(),
        clients=graphene.List(graphene.ID)
    )
    active_matters_reports = graphene.List(WeekendReportType)
    new_matters_reports = graphene.List(WeekendReportType)
    new_entities = graphene.List(WeekendReportType)
    billable_units = graphene.List(WeekendReportType)
    open_matters_reports = graphene.List(WeekendReportType)
    units_by_staff_reports = graphene.List(
        ByStaffReportType,
        billed=graphene.Boolean(),
        staff_members=graphene.List(graphene.ID),
        from_date=graphene.String(),
        to_date=graphene.String(),
    )
    open_matters_by_staff_reports = graphene.List(OpenMattersReportType)
    total_of_matters_by_staff_reports = graphene.List(
        ByStaffReportType,
        staff_members=graphene.List(graphene.ID),
        matter_status=graphene.Int(),
    )
    effective_rate_reports = graphene.List(
        EffectiveRateReportType,
        staff_member_id=graphene.ID(),
        from_date=graphene.String(),
        to_date=graphene.String(),
    )
    client_invoice_value = graphene.List(ClientInvoiceValueType)

    @login_required
    def resolve_average_invoice_reports(self, info, from_date, to_date):
        reports = []
        from_date = parser.parse(from_date)
        to_date = parser.parse(to_date)
        of_the_same_year = from_date.year == to_date.year

        def calculate_report(month, year):
            invoices = Invoice.objects.filter(
                created_date__year__gte=year,
                created_date__year__lte=year,
                created_date__month__gte=month,
                created_date__month__lte=month,
            )
            if len(invoices):
                total_amount = reduce(
                    (lambda x, y: x + y.value(gst=True)),
                    invoices,
                    0,
                )
                total_outstanding = reduce(
                    (lambda x, y: x + y.net_outstanding),
                    invoices,
                    0,
                )
                average_amount = total_amount / len(invoices)
                average_outstanding = total_outstanding / len(invoices)
                return InvoiceReportType(
                    invoices[0].id,
                    "{} {}".format(calendar.month_name[month], year),
                    total_amount,
                    total_outstanding,
                    average_amount,
                    average_outstanding
                )
            else:
                return None

        if of_the_same_year:
            for month in range(from_date.month, to_date.month + 1):
                report = calculate_report(month, from_date.year)
                if report:
                    reports.append(report)
        else:
            for month in range(from_date.month, 13):
                report = calculate_report(month, from_date.year)
                if report:
                    reports.append(report)

            for month in range(1, to_date.month + 1):
                report = calculate_report(month, to_date.year)
                if report:
                    reports.append(report)

        return reports

    @login_required
    def resolve_matters_per_year_reports(self, info):
        min_year = Matter.objects.aggregate(
            Min('created_date')
        )['created_date__min'].year
        max_year = Matter.objects.aggregate(
            Max('created_date')
        )['created_date__max'].year

        reports = []
        years_count = len(range(min_year, max_year + 1))
        years_statistic = []

        for month in range(1, 13):
            report = MatterYearReportType()
            report.years = []
            report.month = calendar.month_abbr[month]

            matters_by_month = Matter.objects.filter(
                created_date__month__gte=month,
                created_date__month__lte=month,
            ).count()

            for year in range(min_year, max_year + 1):
                matters_by_month_by_year = Matter.objects.filter(
                    created_date__year__gte=year,
                    created_date__year__lte=year,
                    created_date__month__gte=month,
                    created_date__month__lte=month,
                ).count()

                if matters_by_month_by_year:
                    item_index = next((index for (index, d) in enumerate(
                        years_statistic) if d["year"] == year), None)

                    if item_index is not None:
                        years_statistic[item_index]['months_count'] += 1
                        years_statistic[item_index]['matters_count'] += \
                            matters_by_month_by_year
                    else:
                        years_statistic.append({
                            'year': year,
                            'months_count': 1,
                            'matters_count': matters_by_month_by_year
                        })

                report_id = "{}-{}".format(year, month)
                report.id = month
                report.years.append(YearMatterType(
                    report_id,
                    year,
                    matters_by_month_by_year
                ))

            report.years.append(YearMatterType(
                "{}-average".format(month),
                "Average",
                "{0:.2f}".format(matters_by_month / years_count)
            ))

            reports.append(report)

        for index, month in enumerate(range(1, 13)):
            for stat in years_statistic:
                report_id = "{}-{}".format(stat['year'], month)
                average_by_year = stat['matters_count'] / stat['months_count']
                reports[index].years.append(YearMatterType(
                    "{}-average".format(report_id),
                    "{}-average".format(stat['year']),
                    "{0:.2f}".format(average_by_year),
                ))

        return reports

    @login_required
    def resolve_client_value_reports(self, info, **args):
        reports = []
        clients = args.get('clients')
        current_year = datetime.now().year
        from_date = args.get(
            'from_date',
            Invoice.objects.filter(created_date__year=current_year).aggregate(
                Min('created_date')
            )['created_date__min'])
        to_date = args.get(
            'to_date',
            Invoice.objects.filter(created_date__year=current_year).aggregate(
                Max('created_date')
            )['created_date__max'])

        if not clients:
            clients = [client['pk'] for client in Client.objects.values('pk')]

        for client_id in clients:
            client_id = from_global_id(client_id)[1]
            client = Client.objects.prefetch_related(
                'matters').get(pk=client_id)
            invoice_ids = client.matters.filter(
                invoices__created_date__gte=from_date,
                invoices__created_date__lte=to_date,
            ).values('invoices').distinct()

            client_value = Decimal(
                sum([Invoice.objects.get(pk=inv_id['invoices']).value()
                     for inv_id in invoice_ids])
            )

            report = ClientValueReportType(
                client_id,
                client.name,
                client_value
            )
            reports.append(report)

        return reports

    @login_required
    def resolve_active_matters_reports(self, info):
        reports = []
        today = datetime.now().date()
        last_sunday = today - \
            timedelta(days=today.weekday()) + timedelta(days=6, weeks=-1)

        date = last_sunday + timedelta(weeks=1)

        for week in range(int(last_sunday.strftime("%V")), 0, -1):
            matters_count = Matter.objects.annotate(
                time_entries_count=Sum(Case(
                    When(time_entries__entry_type=1, then=1),
                    default=0,
                    output_field=IntegerField()
                )),
                disbursements_count=Sum(Case(
                    When(time_entries__entry_type=2, then=1),
                    default=0,
                    output_field=IntegerField()
                )),
            ).filter(
                Q(created_date__week=week),
                Q(time_entries_count__gt=0) |
                Q(disbursements_count__gt=0)
            ).count()

            date -= timedelta(weeks=1)

            report = WeekendReportType(
                "active-{}".format(week),
                "w/e {}".format(date.strftime('%d/%m')),
                matters_count
            )
            reports.append(report)

        return reversed(reports)

    @login_required
    def resolve_new_matters_reports(self, info):
        reports = []
        today = datetime.now().date()
        last_sunday = today - \
            timedelta(days=today.weekday()) + timedelta(days=6, weeks=-1)

        date = last_sunday + timedelta(weeks=1)

        for week in range(int(last_sunday.strftime("%V")), 0, -1):
            matters_count = Matter.objects.filter(
                created_date__week=week
            ).count()

            date -= timedelta(weeks=1)

            report = WeekendReportType(
                "open-{}".format(week),
                "w/e {}".format(date.strftime('%d/%m')),
                matters_count
            )
            reports.append(report)

        return reversed(reports)

    @login_required
    def resolve_new_entities(self, info):
        reports = []
        today = datetime.now().date()
        last_sunday = today - \
            timedelta(days=today.weekday()) + timedelta(days=6, weeks=-1)

        date = last_sunday + timedelta(weeks=1)

        for week in range(int(last_sunday.strftime("%V")), 0, -1):

            client_count = Client.objects.filter(
                created_date__week=week
            ).count()

            if client_count == 0:
                continue

            date -= timedelta(weeks=1)

            report = WeekendReportType(
                "new-{}".format(week),
                "w/e {}".format(date.strftime('%d/%m')),
                client_count
            )
            reports.append(report)

        return reversed(reports)

    @login_required
    def resolve_billable_units(self, info):
        reports = []
        today = datetime.now().date()
        last_sunday = today - \
            timedelta(days=today.weekday()) + timedelta(days=6, weeks=-1)

        date = last_sunday + timedelta(weeks=1)

        for week in range(int(last_sunday.strftime("%V")), 0, -1):
            units_count = TimeEntry.objects.filter(
                date__week=week,
                status=1,
            ).aggregate(Sum('units')).get('units__sum')

            date -= timedelta(weeks=1)

            report = WeekendReportType(
                "units-{}".format(week),
                "w/e {}".format(date.strftime('%d/%m')),
                units_count or 0,
            )
            reports.append(report)

        return reversed(reports)

    @login_required
    def resolve_open_matters_reports(self, info):
        reports = []
        today = datetime.now().date()
        last_sunday = today - \
            timedelta(days=today.weekday()) + timedelta(days=6, weeks=-1)

        date = last_sunday + timedelta(weeks=1)

        history = HistoricalMatter.objects.filter(billable_status=3)

        for week in range(int(last_sunday.strftime("%V")), 0, -1):
            matters_count = history.filter(history_date__week=week).count()

            if matters_count == 0:
                continue

            date -= timedelta(weeks=1)

            report = WeekendReportType(
                "open-matter-{}".format(week),
                "w/e {}".format(date.strftime('%d/%m')),
                matters_count,
            )
            reports.append(report)

        return reversed(reports)

    @login_required
    def resolve_units_by_staff_reports(self, info, billed=False, **args):
        reports = []
        staff_members = args.get('staff_members')
        from_date = args.get('from_date')
        to_date = args.get('to_date')

        if not from_date:
            from_date = TimeEntry.objects.filter(
                date__year=datetime.now().year).aggregate(
                Min('date')
            )['date__min']
        elif type(from_date) is str:
            from_date = parser.parse(from_date)

        if not to_date:
            to_date = TimeEntry.objects.filter(
                date__year=datetime.now().year).aggregate(
                Max('date')
            )['date__max']

        elif type(to_date) is str:
            to_date = parser.parse(to_date)

        if not staff_members:
            staff_members = [staff['pk']
                             for staff in User.objects.values('pk')]

        date = from_date

        while date <= to_date:
            week = date.strftime('%V')

            if billed:
                report_id = "billedUnitsByStaff-{}".format(week)
            else:
                report_id = "billableUnitsByStaff-{}".format(week)

            report = ByStaffReportType(
                report_id,
                date.strftime("%d/%m/%y"),
            )
            report.staff_members = []

            date += timedelta(weeks=1)

            for staff_id in staff_members:
                staff_id = from_global_id(staff_id)[1]
                staff = User.objects.get(pk=staff_id)
                if billed:
                    units_count = TimeEntry.objects.filter(
                        date__week=week,
                        date__year=date.year,
                        status=1,
                        staff_member=staff,
                        invoice__isnull=False,
                    ).aggregate(Sum('units')).get('units__sum')
                else:
                    units_count = TimeEntry.objects.filter(
                        date__week=week,
                        date__year=date.year,
                        status=1,
                        staff_member=staff,
                    ).aggregate(Sum('units')).get('units__sum')

                if billed:
                    report_id = "billedUnitsByStaff-{}-{}".format(
                        week, staff.id)
                else:
                    report_id = "billableUnitsByStaff-{}-{}".format(
                        week, staff.id)

                report.staff_members.append(StaffReportType(
                    report_id,
                    staff.full_name,
                    units_count or 0
                ))

            reports.append(report)

        return reports

    @login_required
    def resolve_open_matters_by_staff_reports(self, info):
        reports = []

        for staff in User.objects.all():
            report = OpenMattersReportType(
                staff.id,
                staff.full_name
            )
            report.matter_statuses = []
            for status in MATTER_STATUSES:
                matters_count = Matter.objects.filter(
                    Q(assistant=staff) |
                    Q(principal=staff) |
                    Q(manager=staff),
                    matter_status=status[0],
                ).count()

                report.matter_statuses.append(
                    MatterStatusReportType(
                        "{}-{}".format(staff.id, status[0]),
                        status[1],
                        matters_count
                    )
                )

            reports.append(report)

        return sorted(
            reports,
            key=lambda x: -sum(y.count for y in x.matter_statuses)
        )

    @login_required
    def resolve_total_of_matters_by_staff_reports(self, info, **args):
        reports = []
        staff_members = args.get('staff_members')
        matter_status = args.get('matter_status')

        if not matter_status:
            matter_status = 3

        current_year = datetime.now().year

        from_date = Matter.objects.filter(
            created_date__year=current_year
        ).aggregate(
            Min('created_date')
        )['created_date__min']
        to_date = Matter.objects.filter(
            created_date__year=current_year
        ).aggregate(
            Max('created_date')
        )['created_date__max']

        week_range = range(
            int(from_date.strftime("%V")),
            int(to_date.strftime("%V")) + 1
        )
        date = from_date + timedelta(weeks=1)

        for week in week_range:
            date += timedelta(weeks=1)
            report = ByStaffReportType(
                "totalOfMattersByStaff-{}".format(week),
                date.strftime("%d/%m/%y")
            )
            report.staff_members = []

            for staff_id in staff_members:
                staff_id = from_global_id(staff_id)[1]
                staff = User.objects.get(pk=staff_id)

                matters_count = Matter.objects.filter(
                    Q(assistant=staff) |
                    Q(principal=staff) |
                    Q(manager=staff),
                    created_date__week=week,
                    matter_status=matter_status,
                ).count()

                report.staff_members.append(
                    StaffReportType(
                        "totalOfMattersByStaff-{}-{}".format(week, staff.id),
                        staff.full_name,
                        matters_count
                    )
                )

            reports.append(report)

        return reports

    @login_required
    def resolve_effective_rate_reports(self, info, **args):
        reports = []
        staff_member_id = args.get('staff_member_id')
        from_date = args.get('from_date')
        to_date = args.get('to_date')

        if staff_member_id:
            staff_member_id = from_global_id(staff_member_id)[1]
            staff_member = User.objects.get(pk=staff_member_id)
        else:
            staff_member = info.context.user

        if not from_date or not to_date:
            today = date.today()
            first = today.replace(day=1)
            last_month = first - timedelta(days=1)
            to_date = last_month
            from_date = last_month.replace(day=1)
        else:
            from_date = parser.parse(from_date)
            to_date = parser.parse(to_date)

        while from_date <= to_date:
            month = int(from_date.strftime('%m'))
            day = int(from_date.strftime('%d'))
            time_entries = TimeEntry.objects.filter(
                staff_member=staff_member,
                invoice__isnull=False,
                date__month=int(from_date.strftime('%m')),
                date__day=int(from_date.strftime('%d'))
            )
            total_billed_value = reduce(
                (lambda x, y: x + y.billed_value),
                time_entries,
                0
            )
            total_units = reduce(
                (lambda x, y: x + y.units),
                time_entries,
                0
            )

            try:
                effective_rate = float(total_billed_value) / total_units
            except ZeroDivisionError:
                effective_rate = 0

            reports.append(EffectiveRateReportType(
                '{}-{}'.format(day, month),
                from_date.strftime('%d/%m/%y'),
                effective_rate
            ))
            from_date += timedelta(days=1)

        return reports

    @login_required
    def resolve_client_invoice_value(self, info):
        reports = []
        values = [
            {'more': 0, 'less': 5000},
            {'more': 5000, 'less': 10000},
            {'more': 10000, 'less': 15000},
            {'more': 15000, 'less': 20000},
            {'more': 20000, 'less': 25000},
            {'more': 25000, 'less': 30000},
            {'more': 30000, 'less': 35000},
            {'more': 35000, 'less': 40000},
        ]

        for index, val in enumerate(values):
            count = 0
            for client in Client.objects.values('id'):
                client_id = client.get('id')
                invoices = Invoice.objects.filter(matter__client__id=client_id)

                count += len(
                    [inv for inv in invoices if inv.value() >
                     val['more'] and inv.value() < val['less']]
                )

            reports.append(ClientInvoiceValueType(
                index,
                "more than ${}K, less than ${}K".format(
                    val['more'] / 1000,
                    val['less'] / 1000
                ),
                count
            ))

        # more than 40000
        count = len([inv for inv in invoices if inv.value() > 40000])
        reports.append(ClientInvoiceValueType(
            len(values),  # id
            "more than $40K",
            count
        ))

        return reports
