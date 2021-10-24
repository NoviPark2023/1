from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=(permissions.BasePermission,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='./login-home.html'), name='login'),
    path('kupci/', include('real_estate_api.kupci.urls', namespace='kupci')),
    path('korisnici/', include('real_estate_api.korisnici.urls', namespace='korisnici')),
    path('stanovi/', include('real_estate_api.stanovi.urls', namespace='stanovi')),
    path('ponude/', include('real_estate_api.ponude.urls', namespace='ponude')),
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
]

# If we are in dev mode -- DEBUG=True, also use this urlpatterns form MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
