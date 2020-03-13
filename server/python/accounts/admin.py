from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from sitename.admin import admin as sitename_admin
# from gmailbox.forms import GmailAccountForm
from gmailbox.models import GmailAccount

from .models import Client, Contact, Location, Organisation, User


# class GmailInline(admin.StackedInline):
#     model = GmailAccount
#     form = GmailAccountForm


class LocationAdmin(admin.ModelAdmin):
    search_fields = ['address1', 'address2', 'suburb', 'country', 'post_code']


class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('full_name', 'email')
    list_display_links = ('full_name', 'email')
    fieldsets = (
        (None,
            {'fields': ('salutation', 'first_name', 'last_name', 'email')},
         ),
        (None,
         {'fields': (
                    'photo', 'rate', 'mobile', 'is_staff',
                    'is_active', 'is_legal', 'password', 'groups'
                    )}
         )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    # inlines = [
    #     GmailInline,
    # ]
    search_fields = ['email']


class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fieldsets = (
        (None,
            {'fields': (
                'id', 'first_name', 'last_name', 'middle_name',
                'email', 'secondary_email', 'mobile', 'salutation',
                'occupation', 'skype', 'is_active', 'preferred_first_name',
                'date_of_birth', 'date_of_death', 'estimated_wealth',
                'estimated_wealth_date', 'referrer', '_spouses', 'mother',
                'father', 'location', 'postal_location', 'voi',
                'direct_line', 'beverage', 'organisations', 'role',
                'is_general')},
         ),
    )
    list_display = ('full_name', 'email', 'mobile', 'direct_line')
    list_display_links = ('full_name', 'email')
    autocomplete_fields = ('location', 'postal_location')
    search_fields = ['email', 'mobile']

    def full_name(self, obj):
        return obj.full_name


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    fieldsets = (
        (None,
            {'fields': (
                'id', 'is_active', 'office')},
         ),
        ('Contact',
            {'fields': (
                'contact_id', 'contact',
            )},
         ),
        ('Second contact',
            {'fields': (
                'second_contact_id', 'second_contact',
            )},
         ),
        ('Organisation',
            {'fields': (
                'organisation_id', 'organisation'
            )},
         ),
    )
    readonly_fields = (
        'id', 'contact_id', 'second_contact_id', 'organisation_id')

    def name(self, obj):
        return obj.name

    def contact_id(self, obj):
        return obj.contact.id

    def second_contact_id(self, obj):
        return obj.second_contact.id

    def organisation_id(self, obj):
        return obj.organisation.id


class OrganisationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fieldsets = (
        (None, {'fields': (
            'id', 'name', 'main_line', 'website',
            'industry', 'location', 'postal_location',
            'group_status', 'group_parent', 'business_search_words'
        )}),
    )
    autocomplete_fields = ('location', 'postal_location')


sitename_admin.register(User, UserAdmin)
sitename_admin.register(Organisation, OrganisationAdmin)
sitename_admin.register(Contact, ContactAdmin)
sitename_admin.register(Client, ClientAdmin)
sitename_admin.register(Location, LocationAdmin)
sitename_admin.register(Group, GroupAdmin)
