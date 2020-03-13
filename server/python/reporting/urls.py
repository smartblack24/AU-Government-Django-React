from django.conf.urls import url

from .views import MatterReportPDF, PrincipalReportPDF

urlpatterns = [
    url(r'pdf/matter-report/(?P<user_id>.*)/(?P<billable_status>[0-9]*)',
        MatterReportPDF.as_view()),
    url(r'pdf/principal-report/(?P<user_id>.*)/(?P<billable_status>[0-9]*)',
        PrincipalReportPDF.as_view()),
]
