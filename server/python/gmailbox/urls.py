from django.conf.urls import url

from .views import MailView, MailExportView

urlpatterns = [
    url(r'mail/export/(?P<mail_ids>.*)', MailExportView.as_view()),
    url(r'mail/(?P<mail_id>.*)/', MailView.as_view()),
]
