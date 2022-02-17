import boto3
from django.conf import settings
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from docx.opc.exceptions import PackageNotFoundError
from rest_framework import generics, filters
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from real_estate_api.lokali.lokali_api.models import Lokali
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala
from real_estate_api.lokali.ponude_lokala.serializers import PonudeLokalaSerializer
from real_estate_api.lokali.ugovori_lokali.ugovori_lokali import ContractLokali

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

    def perform_create(self, serializer):
        """
        Svaki Lokal ima svoje statuse prodaje (Dostupan, Rezervisan, Kupljen).
        Prilikom svake promene statusa Ponude potrebno je azurirati i status prodaje Lokala.
        Ukoliko je status ponude setovan na jedna od dva stanja (Rezervisan, Kupljen),
        potrebno j egenerisati ugovor.
        Ukoliko je status ponude promenjen na potencijalan, potrebno je obrisati ugovor.

            @see Generisanje Ugovora: /ugovori_lokali/ugovori_lokali.py
        ---
        :param serializer: PonudeLokalaSerializer
        """
        ponude_lokali = serializer.save()


        if ponude_lokali.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.POTENCIJALAN and \
            ponude_lokali.status_ponude_lokala != PonudeLokala.StatusPonudeLokala.REZERVISAN and \
            ponude_lokali.status_ponude_lokala != PonudeLokala.StatusPonudeLokala.KUPLJEN:

            ponude_lokali.lokali.status_prodaje_lokala = Lokali.StatusProdajeLokala.DOSTUPAN
            ponude_lokali.odobrenje_kupovine_lokala = False


        elif ponude_lokali.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.REZERVISAN and \
            ponude_lokali.status_ponude_lokala != PonudeLokala.StatusPonudeLokala.KUPLJEN:

            ponude_lokali.lokali.status_prodaje_lokala = Lokali.StatusProdajeLokala.REZERVISAN
            ponude_lokali.odobrenje_kupovine_lokala = True

            # Kreiranje Ugovora
            try:
                ContractLokali.create_contract(
                    ponude_lokali,
                    ponude_lokali.lokali,
                    ponude_lokali.kupac_lokala
                )
            except PackageNotFoundError:
                # TODO: Implementirati ovaj exception.
                print("Greska u kreiranju ugovora !")


        elif ponude_lokali.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.KUPLJEN:
            ponude_lokali.lokali.status_prodaje_lokala = Lokali.StatusProdajeLokala.PRODAT
            ponude_lokali.odobrenje_kupovine_lokala = True

            # Kreiranje Ugovora
            try:
                ContractLokali.create_contract(
                    ponude_lokali,
                    ponude_lokali.lokali,
                    ponude_lokali.kupac_lokala
            )
            except PackageNotFoundError:
                # TODO: Implementirati ovaj exception.
                print("Greska u kreiranju ugovora !")


        ponude_lokali.lokali.save()
        ponude_lokali.save()


class IzmeniPonuduLokalaAPIView(generics.RetrieveUpdateAPIView):
    """Izmena Ponude Lokala po ID-ju"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = PonudeLokala.objects.all().order_by('id_ponude_lokala')
    serializer_class = PonudeLokalaSerializer

    def perform_update(self, serializer):
        """
        Svaki Lokal ima svoje statuse prodaje (Dostupan, Rezervisan, Kupljen).
        Prilikom svake promene statusa Ponude potrebno je azurirati i status prodaje Lokala.
        Ukoliko je status ponude setovan na jedna od dva stanja (Rezervisan, Kupljen),
        potrebno j egenerisati ugovor.
        Ukoliko je status ponude promenjen na potencijalan, potrebno je obrisati ugovor.

            @see Generisanje Ugovora: /ugovori_lokali/ugovori_lokali.py
        ---
        :param serializer: PonudeLokalaSerializer
        """
        ponude_lokali = serializer.save()

        if ponude_lokali.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.POTENCIJALAN and \
            ponude_lokali.status_ponude_lokala != PonudeLokala.StatusPonudeLokala.REZERVISAN and \
            ponude_lokali.status_ponude_lokala != PonudeLokala.StatusPonudeLokala.KUPLJEN:

            ponude_lokali.lokali.status_prodaje_lokala = Lokali.StatusProdajeLokala.DOSTUPAN

            ponude_lokali.lokali.save()
            ponude_lokali.odobrenje_kupovine_lokala = False
            ponude_lokali.save()

            # Obrisi ugovor jer je Lokal dobio status "Dostupan".
            ContractLokali.delete_contract(ponude_lokali)

        elif ponude_lokali.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.REZERVISAN and \
            ponude_lokali.status_ponude_lokala != PonudeLokala.StatusPonudeLokala.KUPLJEN:

            ponude_lokali.lokali.status_prodaje_lokala = Lokali.StatusProdajeLokala.REZERVISAN

            ponude_lokali.lokali.save()
            ponude_lokali.odobrenje_kupovine_lokala = True
            ponude_lokali.save()

            # Kreiranje Ugovora
            try:
                ContractLokali.create_contract(
                    ponude_lokali,
                    ponude_lokali.lokali,
                    ponude_lokali.kupac_lokala
                )
            except PackageNotFoundError:
                # TODO: Implementirati ovaj exception.
                print("Greska u kreiranju ugovora !")

        elif ponude_lokali.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.KUPLJEN:
            ponude_lokali.lokali.status_prodaje_lokala = Lokali.StatusProdajeLokala.PRODAT

            ponude_lokali.lokali.save()
            ponude_lokali.odobrenje_kupovine_lokala = True
            ponude_lokali.save()

            try:
                ContractLokali.create_contract(
                    ponude_lokali,
                    ponude_lokali.lokali,
                    ponude_lokali.kupac_lokala
                )
            except PackageNotFoundError:
                # TODO: Implementirati ovaj exception.
                print("Greska u kreiranju ugovora !")


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

    def perform_destroy(self, instance):
        # TODO: Setovanje statusa Lokala na osnovu prioriteta ponuda koje ima  (MOZE BOLJE)
        # Kada se obrise jedna ponuda lokala, a postoji jos ostalih ponuda setovati status lokala
        # na onu ponudu koja ima najvisi status.
        # Ukoliko nema ponuda nakon brisanja te jedine, setovati status na DOSTUPAN

        ponude_lokala = self.get_object()

        id_lokala = ponude_lokala.lokali.id_lokala

        instance.delete()

        # Obrisi ugovor jer je Lokal dobio status "Dostupan".
        ContractLokali.delete_contract(ponude_lokala)

        # Provera da li u bazi ima jos ponuda
        broj_ponuda_lokala_from_db = PonudeLokala.objects.all()

        # Status Ponude
        for ponuda in broj_ponuda_lokala_from_db.filter(lokali_id=id_lokala):
            if ponuda == 0:
                ponuda.lokali.status_prodaje_lokala = Lokali.StatusProdajeLokala.DOSTUPAN

            elif ponuda != 0 and\
                ponuda.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.REZERVISAN and\
                ponuda.status_ponude_lokala != PonudeLokala.StatusPonudeLokala.KUPLJEN:

                ponuda.lokali.status_prodaje_lokala = Lokali.StatusProdajeLokala.REZERVISAN
                ponuda.odobrenje_kupovine_lokala = True

            elif ponuda != 0 and \
                ponuda.status_ponude_lokala == PonudeLokala.StatusPonudeLokala.KUPLJEN:

                ponuda.lokali.status_prodaje_lokala = Lokali.StatusProdajeLokala.PRODAT
                ponuda.odobrenje_kupovine_lokala = True


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
