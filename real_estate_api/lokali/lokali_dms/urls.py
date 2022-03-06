from django.urls import path

from real_estate_api.lokali.lokali_dms.views import ListaDokumenaLokaliAPIView, LokaliDmsUploadAPIView, \
    DokumentiLokalaDownloadAPIView, ObrisiDokumentLokalaAPIView


app_name = "lokali-dms"

urlpatterns = [
    # Lista svih Fajlova Lokala
    path('', ListaDokumenaLokaliAPIView.as_view(), name='lista_dokumenata_lokala'),

    path('upload-lokala-files/', LokaliDmsUploadAPIView.as_view(), name='upload_dokumenta_lokala'),

    # Preuzimanje generisanog dokumenta Lokala.
    path('preuzmi-dokument-lokala/<int:id_fajla>/', DokumentiLokalaDownloadAPIView.as_view()),

    # Brisanje Dokumenta Lokala.
    path('obrisi-dokument-lokala/<int:id_fajla>/', ObrisiDokumentLokalaAPIView.as_view(), name='obrisi_dokument_lokala'),

]
