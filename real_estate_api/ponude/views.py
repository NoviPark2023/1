import boto3
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from .models import Ponude
from .serializers import PonudeSerializer
from .ugovor.ugovori import Contract
from ..stanovi.models import Stanovi

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
    queryset = Ponude.objects.all().order_by('-id_ponude')
    serializer_class = PonudeSerializer

    def perform_create(self, serializer):
        """Some doc here!"""
        ponuda = serializer.save()

        if ponuda.status_ponude == Ponude.StatusPonude.REZERVISAN:

            # Kreiranje Ugovora
            Contract.create_contract(ponuda, ponuda.stan, ponuda.kupac)

            ponuda.stan.status_prodaje = Stanovi.StatusProdaje.REZERVISAN
            ponuda.stan.save()
            ponuda.odobrenje = True
            ponuda.klijent_prodaje = self.request.user  # Set klijenta prodaje Stana
            ponuda.save()

        elif ponuda.status_ponude == Ponude.StatusPonude.KUPLJEN:

            # Kreiranje Ugovora
            Contract.create_contract(ponuda, ponuda.stan, ponuda.kupac)

            ponuda.stan.status_prodaje = Stanovi.StatusProdaje.PRODAT
            ponuda.stan.save()
            ponuda.odobrenje = True
            ponuda.klijent_prodaje = self.request.user  # Set klijenta prodaje Stana
            ponuda.save()

        elif ponuda.status_ponude == Ponude.StatusPonude.POTENCIJALAN:
            ponuda.stan.status_prodaje = Stanovi.StatusProdaje.DOSTUPAN
            ponuda.stan.save()
            ponuda.odobrenje = False
            ponuda.save()

    def get_queryset(self):
        # Potrebno za prikaz svih Ponuda samo za odredjeni Stan
        id_stana = self.kwargs['id_stana']
        return Ponude.objects.all().filter(stan=id_stana)


class UrediPonuduViewAPI(generics.RetrieveUpdateAPIView):
    """Urednjivanje Ponude po ID-ju"""

    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Ponude.objects.all().order_by('-id_ponude')
    serializer_class = PonudeSerializer

    def perform_update(self, serializer):
        """
        Svaki Stan ima svoje statuse prodaje (Dostupan, Rezervisan, Kupljen).
        Prilikom svake promene statusa Ponude potrebno je azurirati i status prodaje Stana.
        Ukoliko je status ponude setovan na jedna od dva stanja (Rezervisan, Kupljen),
        potrebno j egenerisati ugovor.
        Ukoliko je status ponude promenjen na potencijalan, potrebno je obrisati ugovor.

            @see Generisanje Ugovora: Contract
        ---
        :param serializer: PonudeSerializer
        """
        ponuda = serializer.save()

        if ponuda.status_ponude == Ponude.StatusPonude.REZERVISAN:
            ponuda.stan.status_prodaje = Stanovi.StatusProdaje.REZERVISAN
            ponuda.stan.save()
            ponuda.odobrenje = True  # Potrebno odobrenje jer je stan kaparisan (Rezervisan)
            ponuda.save()

            Contract.create_contract(ponuda, ponuda.stan, ponuda.kupac)  # Kreiraj Ugovor.

        elif ponuda.status_ponude == Ponude.StatusPonude.KUPLJEN:
            ponuda.stan.status_prodaje = Stanovi.StatusProdaje.PRODAT
            ponuda.stan.save()
            ponuda.odobrenje = True
            ponuda.save()

            Contract.create_contract(ponuda, ponuda.stan, ponuda.kupac)  # Kreiraj Ugovor.

        elif ponuda.status_ponude == Ponude.StatusPonude.POTENCIJALAN:
            ponuda.stan.status_prodaje = Stanovi.StatusProdaje.DOSTUPAN
            ponuda.stan.save()
            ponuda.odobrenje = False
            ponuda.save()

            Contract.delete_contract(ponuda)  # Obrisi Ugovor.

    def put(self, request, *args, **kwargs):
        """
        * U trenutku setovanja statusa ponuda na 'Rezervisan', Stan se smatra kaparisan.
        * Takodje se setuje status Stana na 'rezervisan', @see(Contract)

            @see Generisanje Ugovora: Contract
        ---
        :param request: Ponude
        :return: partial_update
        """

        # Set Klijenta prodaje stana u ponudu, potrebno kasnije za izvestaje.
        request.data['klijent_prodaje'] = request.user.id

        return self.partial_update(request, *args, **kwargs)


class ObrisiPonuduAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Ponude po ID-ju"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Ponude.objects.all().order_by('-id_ponude')
    serializer_class = PonudeSerializer

    def perform_destroy(self, instance):
        # TODO: Setovanje stana na osnovu prioriteta ponuda koje ima  (MOZE BOLJE)
        # Kada se obrise jedna ponuda, a postoji jos ostalih ponuda setovati status stana
        # na onu ponudu koja ima najvisi status.
        # Ukoliko nema ponuda nakon brisanja te jedine, setovati status na DOSTUPAN

        ponude_stana = self.get_object()
        id_stana = ponude_stana.stan.id_stana

        instance.delete()
        Contract.delete_contract(instance)

        # Set Status Stana
        for status_ponude in self.queryset.filter(stan__id_stana=id_stana).values("status_ponude").iterator():
            if status_ponude["status_ponude"] == "potencijalan":
                instance.stan.status_prodaje = 'dostupan'
                instance.stan.save()
            elif status_ponude["status_ponude"] == "rezervisan":
                instance.stan.status_prodaje = 'rezervisan'
                instance.stan.save()
            elif status_ponude["status_ponude"] == "kupljen":
                instance.stan.status_prodaje = 'prodat'
                instance.stan.save()

        # Nema vise Ponuda, mozemo da setujemo status prodaje Stana na "Dostupan".
        if self.queryset.filter(stan__id_stana=id_stana).count() == 0:
            instance.stan.status_prodaje = 'dostupan'
            instance.stan.save()


class UgovorPonudeDownloadListAPIView(generics.ListAPIView):
    """
    API View za preuzimanje generisanog ugovora.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = PonudeSerializer

    def get(self, request, *args, **kwargs):
        """
        Generisanje jedinstvenog URL za svaki ugovor koji je ucitan na Digital Ocean Space.
        Url se generisa sa sigurnosnim parametrima AWSa.

            @see Generisanje Ugovora: Contract
        ---
        @param request: None
        @param args: None
        @param kwargs: ID Ponude Stana
        @return: Respons sa jedinstvenim URL za preuzimanje ugovora
        """

        queryset = Ponude.objects.get(id_ponude__exact=kwargs['id_ponude'])

        try:
            session = boto3.session.Session()
            client = session.client('s3',
                                    region_name='fra1',
                                    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

            # Generisi sigurnosni URL za preuzimanje ugovora
            url = client.generate_presigned_url(ClientMethod='get_object',
                                                Params={
                                                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                    'Key': 'ugovor-br-' + str(queryset.stan.lamela) + '.docx'
                                                }, ExpiresIn=70000)

        except (FileNotFoundError, Ponude.DoesNotExist):
            raise NotFound('Željeni ugovor nije nađen !', code=404)

        return HttpResponse(url)
