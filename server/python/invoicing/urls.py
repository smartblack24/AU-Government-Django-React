from django.conf.urls import url

from .views import GeneratePdf, GenerateReminder, invoice_footer

urlpatterns = [
    url(r'pdf/invoice/(?P<invoice_id>.*)/', GeneratePdf.as_view()),
    url(r'pdf/invoice_footer/(?P<invoice_id>.*)/',
        invoice_footer, name='invoice_footer'),
    url(r'pdf/reminder/(?P<invoice_id>.*)/(?P<reminder>[a-z]+)/user/(?P<user_id>.*)',
        GenerateReminder.as_view()),
]
