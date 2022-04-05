import boto3
from django.conf import settings
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from real_estate_api.garaze.models import Garaze
from real_estate_api.garaze.serializers import GarazeSerializer
from real_estate_api.garaze.ugovori_garaze.ugovor_garaze import ContractGaraze

lookup_field = 'id_garaze'
lookup_field_kupac = 'id_kupca'


class ListaGarazaAPIView(generics.ListAPIView):
    """
    API poziv za listu svih Garaza.
    ---
        * Pretraga po poljima:
         - jedinstveni_broj_garaze
         - cena_garaze
         - broj_ugovora_garaze
         - napomena_garaze
         - kupac
         - ime_kupca
    ---
        * Filtriranje po poljima:
         - jedinstveni_broj_garaze (exact)
         - status_prodaje_garaze (exact)
         - nacin_placanja_garaze (exact)
    """
    permission_classes = [IsAuthenticated]
    queryset = Garaze.objects.all()
    serializer_class = GarazeSerializer

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        DjangoFilterBackend,
        filters.SearchFilter
    ]

    filterset_fields = {
        "jedinstveni_broj_garaze": ["exact"],
        "status_prodaje_garaze": ["exact"],
        "nacin_placanja_garaze": ["exact"]
    }

    search_fields = [
        'jedinstveni_broj_garaze',
        'cena_garaze',
        'broj_ugovora_garaze',
        'napomena_garaze',
        'kupac',
        'ime_kupca'
    ]


class DetaljiGarazeAPIView(generics.RetrieveAPIView):
    """Lista Garaze po ID-ju, || Detalji Garaze"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Garaze.objects.all().order_by('id_garaze')
    serializer_class = GarazeSerializer


class KreirajGarazuAPIView(generics.CreateAPIView):
    """Kreiranje nove Garaze"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field_kupac
    queryset = Garaze.objects.all().order_by('id_garaze')
    serializer_class = GarazeSerializer

    def perform_create(self, serializer):
        """
        Prilikom kreiranja Garaye potrebno je  generisati ili obrisati ugovor.
        Takođe je potrebno postaviti odobrenje(True)  Stana ukoliko je stan
        rezervisan ili prodat.

        :param serializer: GarazeSerializer
        """
        garaza = serializer.save()

        if garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.REZERVISANA:

            ContractGaraze.create_contract(garaza, garaza.kupac)  # Kreiraj Ugovor Garaže.

        elif garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.PRODATA:

            ContractGaraze.create_contract(garaza, garaza.kupac)  # Kreiraj Ugovor Garaže.


class UrediGarazuAPIView(generics.RetrieveUpdateAPIView):
    """Uredjivanje Garaze po pk-id"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Garaze.objects.all().order_by('id_garaze')
    serializer_class = GarazeSerializer

    def perform_update(self, serializer):
        """
        Prilikom uređivanja statusa Garaže potrebno je  generisati ili obrisati ugovor.

        :param serializer: GarazeSerializer
        """
        garaza = serializer.save()

        if garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.REZERVISANA:

            ContractGaraze.create_contract(garaza, garaza.kupac)  # Kreiraj Ugovor Garaže.

        elif garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.PRODATA:

            ContractGaraze.create_contract(garaza, garaza.kupac)  # Kreiraj Ugovor Garaže.


class ObrisiGarazuAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Garaze po pk-id"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Garaze.objects.all().order_by('id_garaze')
    serializer_class = GarazeSerializer


class UgovorPonudeGarazeDownloadAPIView(generics.ListAPIView):
    """
    API View za preuzimanje generisanog ugovora Garaze.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = GarazeSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Generisanje jedinstvenog URL za svaki ugovor graze koji je ucitan na Digital Ocean Space.
        Url se generisa sa sigurnosnim parametrima AWSa.

            @see Generisanje Ugovora Garaze: ContractGaraze
        ---
        @param request: None
        @param args: None
        @param kwargs: ID Ponude Stana
        @return: Respons sa jedinstvenim URL za preuzimanje ugovora
        """

        queryset = Garaze.objects.get(id_garaze__exact=kwargs['id_garaze'])

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
                    'Bucket': 'ugovori-garaze',
                    'Key': 'ugovor-garaze-br-' + str(queryset) + '.docx'
                }, ExpiresIn=70000
            )

        except (FileNotFoundError, Garaze.DoesNotExist):
            raise NotFound('Željeni ugovor garaze nije nađen !', code=404)

        return HttpResponse(url)
