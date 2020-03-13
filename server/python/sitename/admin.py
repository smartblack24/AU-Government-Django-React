from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy


class sitenameAdminSite(AdminSite):
    site_title = ugettext_lazy('sitename admin')
    site_header = ugettext_lazy('sitename administration')
    index_title = ugettext_lazy('sitename administration')


admin = sitenameAdminSite()
