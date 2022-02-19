import boto3
from django.conf import settings
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from real_estate_api.lokali.ponude_lokala.models import PonudeLokala
from real_estate_api.lokali.ponude_lokala.serializers import PonudeLokalaSerializer

lookup_field = 'id_ponude_lokala'
lookup_field_lokal = 'id_lokala'


class ListaPonudaLokalaAPIView(generics.ListAPIView):
    """
    API poziv za listu svih Ponuda Lokala.
        * Filtriranje se radi po polju 'id_ponude_lokala'.
        * Pretraga se radi po poljima 'lamela_lokala', 'id_lokala'.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = PonudeLokala.objects.all().order_by(lookup_field)
    serializer_class = PonudeLokalaSerializer

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = {
        "id_ponude_lokala": ["exact"],
    }

    search_fields = ['id_ponude_lokala']


class ListaPonudaZaLokalAPIView(generics.ListAPIView):
    """Lista svih Ponuda"""
    permission_classes = [IsAuthenticated, ]
    lookup_field_stan = lookup_field
    queryset = PonudeLokala.objects.all()
    serializer_class = PonudeLokalaSerializer

    def get_queryset(self):
        """
        This view should return a list of all the Ponuda Lokala for
        the Lokal as determined by the Lokal ID portion of the URL.
        """
        id_lokala = self.kwargs['id_lokala']
        return PonudeLokala.objects.all().filter(lokali__id_lokala=id_lokala)


class DetaljiPonudeLokalaAPIView(generics.RetrieveAPIView):
    """Get Ponude Lokala po ID-ju  || Detalji Ponude Lokala"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = PonudeLokala.objects.all()
    serializer_class = PonudeLokalaSerializer


class KreirajPonuduLokalaAPIView(generics.CreateAPIView):
    """Kreiranje nove Ponude Lokala"""
    permission_classes = [IsAuthenticated, ]
    lookup_field_lokal = lookup_field_lokal
    queryset = PonudeLokala.objects.all().order_by('id_ponude_lokala')
    serializer_class = PonudeLokalaSerializer


class IzmeniPonuduLokalaAPIView(generics.RetrieveUpdateAPIView):
    """Izmena Ponude Lokala po ID-ju"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = PonudeLokala.objects.all().order_by('id_ponude_lokala')
    serializer_class = PonudeLokalaSerializer

    def put(self, request, *args, **kwargs):
        # Set Klijenta prodaje Lokala u ponudu, potrebno kasnije za izvestaje.
        request.data['klijent_prodaje_lokala'] = request.user.id
        return self.partial_update(request, *args, **kwargs)


class ObrisiPonuduLokalaAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Ponude Lokala po ID-ju"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = PonudeLokala.objects.all().order_by('-id_ponude_lokala')
    serializer_class = PonudeLokalaSerializer


class UgovorPonudeLokalaDownloadListAPIView(generics.ListAPIView):
    """
    API View za preuzimanje generisanog ugovora Lokala.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = PonudeLokalaSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Generisanje jedinstvenog URL za svaki ugovor Lokala koji je ucitan na Digital Ocean Space.
        Url se generisa sa sigurnosnim parametrima AWSa.

            @see Generisanje Ugovora Lokala: ContractLokali
        ---
        @param request: None
        @param args: None
        @param kwargs: ID Ponude Stana
        @return: Respons sa jedinstvenim URL za preuzimanje ugovora
        """

        queryset = PonudeLokala.objects.get(id_ponude_lokala__exact=kwargs['id_ponude_lokala'])

        try:
            session = boto3.session.Session()
            client = session.client('s3',
                                    region_name='fra1',
                                    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            # Generisi sigurnosni URL za preuzimanje ugovora
            url = client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': 'ugovori-lokali',
                    'Key': 'ugovor-lokala-br-' +
                           str(queryset.id_ponude_lokala) +
                           '-' +
                           str(queryset.lokali.lamela_lokala) +
                           '.docx'
                }, ExpiresIn=70000
            )

        except (FileNotFoundError, PonudeLokala.DoesNotExist):
            raise NotFound('Željeni ugovor nije nađen !', code=404)

        return HttpResponse(url)
