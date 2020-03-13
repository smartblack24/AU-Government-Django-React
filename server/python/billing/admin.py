from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from sitename.admin import admin as sitename_admin
from rangefilter.filter import DateRangeFilter

from .models import Matter, Note, StandartDisbursement, TimeEntry, EntryType


class UnbilledTimeEntryFilter(SimpleListFilter):
    title = 'unbilled status'
    parameter_name = 'unbilled'

    def lookups(self, request, model_admin):
        return (('True', 'Unbilled'), ('False', 'Billed'))

    def queryset(self, request, queryset):
        if self.value() == 'True':
            return queryset.filter(invoice__isnull=True)
        if self.value() == 'False':
            return queryset.filter(invoice__isnull=False)

        return queryset.all()


class MatterAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'name', 'billable_status')
    list_display_links = ('client_name', 'name')
    readonly_fields = ('id', 'client_id')
    fieldsets = (
        (None,
            {'fields': (
                'id', 'name', 'client_id', 'client', 'description',
                'matter_type', 'matter_sub_type', 'principal',
                'manager', 'assistant', 'conflict_status',
                'conflict_parties', 'created_date', 'closed_date',
                'budget', 'billing_method', 'billable_status',
                'funds_in_trust', 'matter_status', 'file_path',
                'conflict_check_sent', 'is_conflict_check_sent',
                'standard_terms_sent', 'is_standard_terms_sent',
                'referrer_thanked', 'is_referrer_thanked', 'lead_date',
                'lead_status', 'entry_type')},
         ),
    )

    def client_name(self, obj):
        return obj.client.name

    def client_id(self, obj):
        return obj.client.id


class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'client_name', 'matter_name')
    list_display_links = ('date_time', 'client_name', 'matter_name')
    search_fields = ('matter__name',)
    list_filter = ('entry_type', UnbilledTimeEntryFilter)
    readonly_fields = ('id', 'matter_id', 'client_id')
    fieldsets = (
        (None,
            {'fields': (
                'id', 'description', 'client_id', 'client', 'staff_member',
                'matter_id', 'matter', 'invoice', 'date', 'units',
                'units_to_bill', 'status', 'gst_status', 'rate',
                'entry_type', 'time_entry_type')},
         ),
    )

    def date_time(self, obj):
        return '{}'.format(obj.date.strftime('%Y-%m-%d %H:%M %p'))

    def client_name(self, obj):
        if obj.matter:
            return obj.matter.client.name

        return 'None'

    def client_id(self, obj):
        return obj.matter.client.id

    def matter_id(self, obj):
        return obj.matter.id

    def matter_name(self, obj):
        if obj.matter:
            return obj.matter.name

        return 'None'


class NoteAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'matter', 'client_name',
                    'text', 'user', 'date_time'
                    )
                }
            ),
        )
    readonly_fields = ('client_name',)
    list_display = ('client_name', 'matter', 'date_time', 'note_text')
    list_filter = (('date_time', DateRangeFilter), )
    list_display_links = ('note_text', 'client_name')
    search_fields = ('text', 'matter__name')

    def client_name(self, obj):
        if obj.matter:
            return obj.matter.client.name
        return 'None'

    def note_text(self, obj):
        if len(obj.text) < 50:
            return obj.text
        return obj.text[:50] + '...'


sitename_admin.register(Matter, MatterAdmin)
sitename_admin.register(TimeEntry, TimeEntryAdmin)
sitename_admin.register(StandartDisbursement)
sitename_admin.register(Note, NoteAdmin)
sitename_admin.register(EntryType)
