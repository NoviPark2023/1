from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='./login-home.html'), name='login'),
    path('kupci/', include('real_estate_api.kupci.urls', namespace='kupci')),
    path('korisnici/', include('real_estate_api.korisnici.urls', namespace='korisnici')),
    path('stanovi/', include('real_estate_api.stanovi.urls', namespace='stanovi')),
    path('ponude/', include('real_estate_api.ponude.urls', namespace='ponude')),

]

# If we are in dev mode -- DEBUG=True, also use this urlpatterns form MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
