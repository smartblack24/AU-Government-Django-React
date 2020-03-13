from sitename.admin import admin as sitename_admin
from solo.admin import SingletonModelAdmin

from .models import Xero, Gmail

sitename_admin.register(Xero, SingletonModelAdmin)
sitename_admin.register(Gmail, SingletonModelAdmin)
