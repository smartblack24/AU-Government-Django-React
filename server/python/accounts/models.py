import re

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from sitename.mixins import UpdateAttributesMixin
from core.models import Industry

from sitename.utils import get_xero_client

from integration.models import Gmail

from .managers import UserManager
from .utils import format_address, prepare_xero_contact_param, check_contact_in_xero

MR = 1
SALUTATIONS = ((1, 'Mr'), (2, 'Mrs'), (3, 'Ms'), (4, 'Miss'), (5, 'Dr'))


class User(AbstractBaseUser, PermissionsMixin, UpdateAttributesMixin):
    email = models.EmailField(unique=True)
    second_email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_legal = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="users/photos", null=True, blank=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    location = models.ForeignKey(
        'accounts.Location', blank=True, null=True, on_delete=models.SET_NULL
    )
    postal_location = models.ForeignKey(
        'accounts.Location',
        related_name='user_postal',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    admission_date = models.DateField(auto_now_add=True, blank=True, null=True)
    salutation = models.IntegerField(choices=SALUTATIONS, default=MR)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def can_use_xero(self):
        return self.has_perm('integration.can_use_xero')

    @property
    def can_link_mails(self):
        return self.has_perm('integration.can_link_mails')

    @property
    def can_delete_mails(self):
        return self.has_perm('integration.can_delete_mails')

    @property
    def gmail(self):
        return self.gmail_account.address if hasattr(self, 'gmail_account') else None

    @property
    def mail_enabled(self):
        gmail_config = Gmail.objects.first()
        return False if not gmail_config else gmail_config.show_mails
        
    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name


class Location(models.Model, UpdateAttributesMixin):
    STATES = ((1, 'SA'), (2, 'NSW'), (3, 'VIC'), (4, 'WA'), (5, 'QLD'),
              (6, 'TAS'), (7, 'NT'), (8, 'ACT'))

    address1 = models.CharField(max_length=256, blank=True, null=True)
    address2 = models.CharField(max_length=256, blank=True, null=True)
    suburb = models.CharField(max_length=256, blank=True, null=True)
    state = models.IntegerField(choices=STATES, blank=True, null=True)
    post_code = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(
            self.address1,
            self.address2,
            self.suburb,
            self.get_state_display(),
            self.country
        )

    def __eq__(self, location):
        if not location:
            return False

        if self.address1 != location.address1:
            return False
        elif self.address2 != location.address2:
            return False
        elif self.suburb != location.suburb:
            return False
        elif self.state != location.state:
            return False
        elif self.country != location.country:
            return False

        return True


class Contact(models.Model, UpdateAttributesMixin):
    ACCOUNTANT = 1
    OCCUPATIONS = ((1, 'Accountant'), (2, 'Financial planner'),
                   (3, 'Banker'), (4, 'Lawyer'), (5, 'Barrister'),
                   (6, 'Engineer'), (7, 'Builder'),
                   (8, 'Doctor - Healthcare Provider'), (9, 'Retailer'),
                   (10, 'Manager'), (11, 'Executive'),
                   (12, 'Administration function'), (13, 'Farmer'),
                   (14, 'Small businessperson'), (15, 'Medium businessperson'),
                   (16, 'Large businessperson'), (17, 'Retired'))

    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    middle_name = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    secondary_email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=256, null=True, blank=True)
    salutation = models.IntegerField(choices=SALUTATIONS, null=True)
    occupation = models.ForeignKey(
        'core.Occupation', on_delete=models.SET_NULL, null=True, default=1)
    skype = models.CharField(max_length=25, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    preferred_first_name = models.CharField(
        max_length=256, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=300, null=True, blank=True)
    estimated_wealth = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True)
    estimated_wealth_date = models.DateField(blank=True, null=True)
    referrer = models.ForeignKey(
        'self',
        related_name='referrers',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    _spouses = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True,
    )
    mother = models.ForeignKey(
        'self',
        related_name="children_from_mother",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    father = models.ForeignKey(
        'self',
        related_name="children_from_father",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    location = models.ForeignKey(
        Location,
        related_name='contact',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    postal_location = models.ForeignKey(
        'accounts.Location',
        related_name='contact_postal',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    voi = models.BooleanField(default=False)
    direct_line = models.CharField(max_length=100, null=True, blank=True)
    beverage = models.CharField(max_length=25, null=True, blank=True)
    organisations = models.ManyToManyField(
        'accounts.Organisation', related_name='contacts', blank=True,
    )
    role = models.CharField(max_length=100, blank=True, null=True)
    link_mails = models.BooleanField(default=True)
    is_general = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ('first_name', 'last_name')

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def formatted_postal_address(self):
        if self.postal_location:
            return format_address(self.postal_location)

        return None

    @property
    def formatted_street_address(self):
        if self.location:
            return format_address(self.location)

        return None

    @property
    def children(self):
        return list(self.children_from_father.all()) \
            + list(self.children_from_mother.all())

    def get_spouse(self):
        return self._spouses.first()

    def set_spouse(self, contact_id):
        self._spouses.set([contact_id])

    def remove_spouse(self):
        self._spouses.clear()

    def __str__(self):
        return self.full_name


class Organisation(models.Model, UpdateAttributesMixin):
    GROUP_STATUSES = ((1, 'Parent'), (2, 'Group memeber'))

    name = models.CharField(max_length=256, unique=True)
    main_line = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    industry = models.ForeignKey(
        Industry,
        related_name='organisations',
        null=True,
        on_delete=models.SET_NULL
    )
    location = models.ForeignKey(
        Location,
        related_name='organisation',
        null=True,
        on_delete=models.SET_NULL
    )
    postal_location = models.ForeignKey(
        'accounts.Location',
        related_name='organisation_postal',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    group_status = models.IntegerField(choices=GROUP_STATUSES)
    group_parent = models.ForeignKey(
        'self',
        related_name="group_children",
        null=True,
        on_delete=models.SET_NULL
    )
    business_search_words = models.TextField(blank=True, null=True)
    link_mails = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def formatted_postal_address(self):
        if self.postal_location:
            return format_address(self.postal_location)

        return None

    @property
    def formatted_street_address(self):
        if self.location:
            return format_address(self.location)

        return None


class Client(models.Model):
    contact = models.ForeignKey(
        Contact,
        related_name='clients',
        null=True,
        on_delete=models.SET_NULL
    )
    organisation = models.ForeignKey(
        Organisation,
        related_name='clients',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    second_contact = models.ForeignKey(
        Contact,
        related_name='second_clients',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    office = models.ForeignKey(
        'core.Office',
        related_name="clients",
        null=True,
        on_delete=models.SET_NULL
    )
    xero_contact_id = models.CharField(max_length=256, null=True)

    class Meta:
        ordering = (
            'organisation__name',
            'contact__first_name',
            'contact__last_name'
        )

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self.organisation and self.contact and self.second_contact:
            return "{} - {} and {}".format(
                self.organisation.name,
                self.contact.full_name,
                self.second_contact.full_name
            )
        elif self.organisation and self.contact:
            return "{} - {}".format(
                self.organisation.name,
                self.contact.full_name
            )
        elif self.organisation and self.second_contact:
            return "{} - {}".format(
                self.organisation.name,
                self.second_contact.full_name
            )
        elif self.organisation and not self.contact and not self.second_contact:
            return self.organisation.name

        elif self.contact and not self.organisation and not self.second_contact:
            return self.contact.full_name
        elif self.contact and self.second_contact and not self.organisation:
            return "{} and {}".format(
                self.contact.full_name,
                self.second_contact.full_name
            )
        elif self.second_contact and not self.contact and not self.organisation:
            return self.second_contact.full_name

        return "Have neither Organisation or Contact associated"

    @property
    def has_matter(self):
        return bool(self.matters.count())

    @property
    def invoicing_address(self):
        if self.organisation:
            return self.organisation.formatted_postal_address or ''

        return self.contact.formatted_postal_address or ''

    @property
    def invoicing_location(self):
        if self.organisation:
            return self.organisation.postal_location

        return self.contact.postal_location

    def create_or_update_xero_contact(self, force_update=False):
        try:
            xero = get_xero_client()

            needs_create = False

            if not self.xero_contact_id:
                needs_create = check_contact_in_xero(self)
            else:
                res = xero.contacts.filter(ContactID=self.xero_contact_id)
                if not res:
                    needs_create = check_contact_in_xero(self)

            contact_param = prepare_xero_contact_param(self)
            valid = contact_param.get('valid')

            if not valid:
                return {'success': False, 'error': contact_param.get('error')}

            xero_contact_data = contact_param.get('data')

            if needs_create:
                xero_contact = xero.contacts.put(xero_contact_data)[0]
                self.xero_contact_id = xero_contact.get('ContactID')
                self.save()

            elif force_update:
                xero_contact_data['ContactID'] = self.xero_contact_id
                xero.contacts.save(xero_contact_data)

            return {'success': True}

        except Exception as e:
            match = re.search(r'\((.*?)\)', str(e))
            if match:
                error = 'Contact: {}'.format(match.group(1))
            else:
                error = 'Failed to create contact in Xero'

            return {'success': False, 'error': error}
