from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

# Dokumentacija inicijalna podesavanja polje u zaglavlju
from real_estate_api.korisnici.views import CustomTokenObtainPairView

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

    path('logout/', LogoutView.as_view(), name='logout'),

    # PREUZIM API TOKEN (Podatke o Korisniku)
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Root Putanja do Kupaca
    path('kupci/', include('real_estate_api.kupci.urls', namespace='kupci')),

    # Root Putanja do Korisnika
    path('korisnici/', include('real_estate_api.korisnici.urls', namespace='korisnici')),

    # Root Putanja do Stanova
    path('stanovi/', include('real_estate_api.stanovi.urls', namespace='stanovi')),

    # Root Putanja do Ponuda
    path('ponude/', include('real_estate_api.ponude.urls', namespace='ponude')),

    # Root Putanja do Reports
    path('reports/', include('real_estate_api.reports.urls', namespace='reports')),

    # Root Putanja do Garaza
    path('garaze/', include('real_estate_api.garaze.urls', namespace='garaze')),

    # Root Putanja do Lokala
    path('lokali/', include('real_estate_api.lokali.lokali_api.urls', namespace='lokali')),

    # Root Putanja do Ponuda Lokala
    path('ponude-lokali/', include('real_estate_api.lokali.ponude_lokala.urls', namespace='ponude-lokali')),

    # Root Putanja do Dokumentacije
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='docs-redoc'),
]

# If we are in dev mode -- DEBUG=True, also use this urlpatterns form MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
