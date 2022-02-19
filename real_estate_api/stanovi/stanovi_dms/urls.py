from django.urls import path

from real_estate_api.stanovi.stanovi_dms.views import (
    StanoviDmsUploadAPIView,
    ListaDokumenaStanoviAPIView,
    DetaljiDokumentaStanaPIView,
)

app_name = "stanovi-dms"

urlpatterns = [

    # Lista svih Fajlova Stanova
    path('', ListaDokumenaStanoviAPIView.as_view(), name='lista_dokumenata_stanova'),
    path('lista-stanovi-files/<int:id_fajla>', DetaljiDokumentaStanaPIView.as_view(), name='lista_dokumenata_stana'),
    path('upload-stanovi-files/', StanoviDmsUploadAPIView.as_view(), name='lista_garazea'),

]
