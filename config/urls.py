from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Dokumentacija inicijalna podesavanja polje u zaglavlju
schema_view = get_schema_view(
    openapi.Info(
        title="FACTORY Real Estate API Managment",
        default_version='v0.1',
        description="Dokumantacija i upravljanje API putanjama na projektu 'Prodaja Stanova'.",
        contact=openapi.Contact(name='@datatab', email="dejan.cugalj@factoryww.com"),
        license=openapi.License(name="GNU General Public License v3"),
    ),
    public=False,
    permission_classes=(permissions.BasePermission,),
)

urlpatterns = [
    # Root Super Admin Path
    path('admin/', admin.site.urls),
    # Root LogIn home path
    path('', LoginView.as_view(template_name='./login-home.html'), name='login'),
    # Root Putanja do Kupaca
    path('kupci/', include('real_estate_api.kupci.urls', namespace='kupci')),
    # Root Putanja do Korisnika
    path('korisnici/', include('real_estate_api.korisnici.urls', namespace='korisnici')),
    # Root Putanja do Stanova
    path('stanovi/', include('real_estate_api.stanovi.urls', namespace='stanovi')),
    # Root Putanja do Ponuda
    path('ponude/', include('real_estate_api.ponude.urls', namespace='ponude')),
    # Root Putanja do Dokumentacije
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
]

# If we are in dev mode -- DEBUG=True, also use this urlpatterns form MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
