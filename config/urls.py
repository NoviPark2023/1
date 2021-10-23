from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kupci/', include('real_estate_api.kupci.urls')),
    path('korisnici/', include('real_estate_api.korisnici.urls')),
    path('stanovi/', include('real_estate_api.stanovi.urls')),
    path('ponude/', include('real_estate_api.ponude.urls')),

]

# If we are in dev mode -- DEBUG=True, also use this urlpatterns form MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
