from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

from .admin import admin

urlpatterns = [
    url(r'admin/', admin.urls),
    url(r'graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'', include('invoicing.urls')),
    url(r'', include('reporting.urls')),
    url(r'', include('gmailbox.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
