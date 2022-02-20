from django.urls import path

from real_estate_api.stanovi.stanovi_dms.views import (
    StanoviDmsUploadAPIView,
    ListaDokumenaStanoviAPIView,
    DetaljiDokumentaStanaPIView,
    DokumentiStanovaDownloadAPIView,
)

app_name = "stanovi-dms"

urlpatterns = [
    # Lista svih Fajlova Stanova
    path('', ListaDokumenaStanoviAPIView.as_view(), name='lista_dokumenata_stanova'),

    path('upload-stanovi-files/', StanoviDmsUploadAPIView.as_view(), name='upload_dokumenta'),

    # Preuzimanje generisanog dokumenta Stana.
    path('preuzmi-dokument-stana/<int:id_fajla>/', DokumentiStanovaDownloadAPIView.as_view()),
]
