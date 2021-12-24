from wsgiref.util import FileWrapper

from django.db.models import Sum, Count
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from rest_framework.views import APIView

from .models import Ponude
from .reports_ponude.reports_ponude import ponude_report
from .serializers import PonudeSerializer, FileDownloadListAPI, PonudeReportsListAPI
from .ugovor.ugovori import CreateContract

lookup_field = 'id_ponude'
lookup_field_stan = 'id_stana'


class ListaPonudaAPIView(generics.ListAPIView):
    """Lista svih Ponuda"""
    permission_classes = [IsAuthenticated, ]
    queryset = Ponude.objects.all().order_by(lookup_field)
    serializer_class = PonudeSerializer


class ListaPonudaZaStanAPIView(ListaPonudaAPIView):
    """Lista svih Ponuda"""
    permission_classes = [IsAuthenticated, ]
    lookup_field_stan = lookup_field_stan
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer

    def get_queryset(self):
        """
        This view should return a list of all the Ponuda for
        the Stan as determined by the Stan ID portion of the URL.
        """
        id_stana = self.kwargs['id_stana']
        return Ponude.objects.all().filter(stan=id_stana)


class PonudeDetaljiAPIView(generics.RetrieveAPIView):
    """Get Ponude po ID-ju  || Detalji Ponude"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer


class KreirajPonuduAPIView(generics.CreateAPIView):
    """Kreiranje nove Ponude"""
    permission_classes = [IsAuthenticated, ]
    lookup_field_stan = lookup_field_stan
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer

    def post(self, request, *args, **kwargs):
        """
        * Prilikom kreiranja Stana automatski update polja 'klijent_prodaje, sa
          korisnikom koji je prijavljen. Prosledjuje se ka Izvestajima.
        * Kreiranje Ugovora ukoliko je inicijalno ponuda na statusu 'rezervisan'.
        :param request: klijent_plrodaje
        :return: Ponude request
        """
        if request.data['status_ponude'] == 'rezervisan':
            CreateContract.create_contract(request, **kwargs)  # Kreiraj ugovor.

        # Set Klijenta prodaje stana u ponudu, potrebno kasnije za izvestaje.
        request.data['klijent_prodaje'] = request.user.id

        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        id_stana = self.kwargs['id_stana']
        return Ponude.objects.all().filter(stan=id_stana)


class UgovorPonudeDownloadListAPIView(generics.ListAPIView):
    """
    API View za preuzimanje generisanog ugovora.
    """
    serializer_class = PonudeSerializer

    def get(self, request, *args, **kwargs):
        """Preuzimanje ugovora"""

        queryset = Ponude.objects.get(id_ponude__exact=kwargs['id_ponude'])
        file_handle = settings.MEDIA_ROOT + '/ugovor' + str(queryset.id_ponude) + '.docx'
        try:
            document = open(file_handle, 'rb')
            response = HttpResponse(FileWrapper(document), content_type='application/msword')
            response['Content-Disposition'] = 'attachment; filename=Ugovor-Ponude-' + str(kwargs['id_ponude']) + '.docx'
        except FileNotFoundError:
            raise NotFound('Željeni ugovor nije nađen !', code=500)

        return response


class UrediPonuduViewAPI(generics.RetrieveUpdateAPIView):
    """Urednjivanje Ponude po ID-ju"""

    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer

    def put(self, request, *args, **kwargs):
        """
        * U trenutku setovanja statusa ponuda na 'Rezervisan', Stan se smatra kaparisan.
        * Takodje se setuje status Stana na 'rezervisan', @see(CreateContract)
        * :see: CreateContract
        :param request: Ponude
        :return: partial_update
        """

        # Set Klijenta prodaje stana u ponudu, potrebno kasnije za izvestaje.
        request.data['klijent_prodaje'] = request.user.id

        CreateContract.create_contract(request, **kwargs)  # Kreiraj ugovor

        return self.partial_update(request, *args, **kwargs)


class ObrisiPonuduAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Ponude po ID-ju"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Ponude.objects.all()
    serializer_class = PonudeSerializer


class PonudaReportAPIView(generics.ListAPIView):
    """Lista svih Ponuda"""
    permission_classes = [IsAuthenticated, ]
    queryset = ponude_report()
    serializer_class = PonudeReportsListAPI


