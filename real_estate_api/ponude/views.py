from smtplib import SMTPException

import boto3
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from .models import Ponude
from .serializers import PonudeSerializer
from .ugovor.ugovori import CreateContract
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
        print(f' id_ponude: {ponuda.id_ponude}')
        print(f' status_ponude: {ponuda.status_ponude}')
        print(f' stan: {ponuda.stan}')
        print(ponuda.id_ponude)

        if ponuda.status_ponude == 'rezervisan':
            CreateContract.create_contract(ponuda, ponuda.stan, ponuda.kupac)
            ponuda.stan.status_prodaje = 'rezervisan'
            ponuda.stan.save()
            print("REZERVISAN !!!")

            try:
                for korisnici_email in settings.RECIPIENT_ADDRESS:
                    send_mail(f'Potrebno ODOBRENJE za Stan ID: {str(ponuda.stan.id_stana)}.',
                              f'Stan ID: {str(ponuda.stan.id_stana)}, Adresa: {str(ponuda.stan.adresa_stana)} je rezervisan.\n'
                              f'Cena stana: {round(ponuda.stan.cena_stana, 2)}\n'
                              f'Cena Ponude je: {round(ponuda.cena_stana_za_kupca, 2)}.',
                              settings.EMAIL_HOST_USER, [korisnici_email])
            except SMTPException as e:
                print(f"failed to send mail: {e}")

        elif ponuda.status_ponude == 'kupljen':
            CreateContract.create_contract(ponuda, ponuda.stan, ponuda.kupac)
            ponuda.stan.status_prodaje = 'prodat'
            ponuda.stan.save()
            print("PRODAT !!!")
            # Posalji svim preplatnicima EMAIL da je Stan KUPLJEN.
            try:
                for korisnici_email in settings.RECIPIENT_ADDRESS:
                    send_mail(f'Stan ID: {str(ponuda.stan.id_stana)} je KUPLJEN.',
                              f'Stan ID: {str(ponuda.stan.id_stana)}, Adresa: {str(ponuda.stan.adresa_stana)} je kupljen.\n'
                              f'Cena stana: {round(ponuda.stan.cena_stana, 2)}\n'
                              f'Cena Ponude je: {round(ponuda.cena_stana_za_kupca, 2)}.',
                              settings.EMAIL_HOST_USER, [korisnici_email])
            except SMTPException as e:
                print(f"failed to send mail: {e}")

        elif ponuda.status_ponude == 'potencijalan':
            ponuda.stan.status_prodaje = 'dostupan'
            ponuda.stan.save()
            print("POTENCIJALAN !!!")

    # def post(self, request, *args, **kwargs):
    #     """
    #     * Prilikom kreiranja Stana automatski update polja 'klijent_prodaje, sa
    #       korisnikom koji je prijavljen. Prosledjuje se ka Izvestajima.
    #     * Kreiranje Ugovora ukoliko je inicijalno ponuda na statusu 'rezervisan'.
    #     ---
    #     :param request: klijent_plrodaje
    #     :return: Ponude request
    #     """
    #     print(f' KWARGS: {kwargs}')
    #     if request.data['status_ponude'] == 'rezervisan':
    #         print(f' KWARGS: {kwargs}')
    #
    #         #CreateContract.create_contract(request, **kwargs)  # Kreiraj ugovor.
    #
    #     elif request.data['status_ponude'] == 'kupljen':
    #         # Ukoliko je status ponude preskocio fazu rezervisan, update Stan na kupljen
    #         stan = Stanovi.objects.get(id_stana__exact=request.data['stan'])
    #         stan.status_prodaje = 'prodat'
    #         stan.save()
    #
    #     # Set Klijenta prodaje stana u ponudu, potrebno kasnije za izvestaje.
    #     request.data['klijent_prodaje'] = request.user.id
    #
    #     return self.create(request, *args, **kwargs)

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
        ponuda = serializer.save()

        if ponuda.status_ponude == 'rezervisan':
            ponuda.stan.status_prodaje = 'rezervisan'
            ponuda.stan.save()
            ponuda.odobrenje = True  # Potrebno odobrenje jer je stan kaparisan (Rezervisan)
            ponuda.save()
            CreateContract.create_contract(ponuda, ponuda.stan, ponuda.kupac)

            try:
                for korisnici_email in settings.RECIPIENT_ADDRESS:
                    send_mail(f'Potrebno ODOBRENJE za Stan ID: {str(ponuda.stan.id_stana)}.',
                              f'Stan ID: {str(ponuda.stan.id_stana)}, Adresa: {str(ponuda.stan.adresa_stana)} je rezervisan.\n'
                              f'Cena stana: {round(ponuda.stan.cena_stana, 2)}\n'
                              f'Cena Ponude je: {round(ponuda.cena_stana_za_kupca, 2)}.',
                              settings.EMAIL_HOST_USER, [korisnici_email])
            except SMTPException as e:
                print(f"failed to send mail: {e}")


        elif ponuda.status_ponude == 'kupljen':
            ponuda.stan.status_prodaje = 'prodat'
            ponuda.stan.save()
            ponuda.odobrenje = True  # Potrebno odobrenje jer je stan kaparisan (Rezervisan)
            ponuda.save()
            CreateContract.create_contract(ponuda, ponuda.stan, ponuda.kupac)

            # Posalji svim preplatnicima EMAIL da je Stan KUPLJEN.
            try:
                for korisnici_email in settings.RECIPIENT_ADDRESS:
                    send_mail(f'Stan ID: {str(ponuda.stan.id_stana)} je KUPLJEN.',
                              f'Stan ID: {str(ponuda.stan.id_stana)}, Adresa: {str(ponuda.stan.adresa_stana)} je kupljen.\n'
                              f'Cena stana: {round(ponuda.stan.cena_stana, 2)}\n'
                              f'Cena Ponude je: {round(ponuda.cena_stana_za_kupca, 2)}.',
                              settings.EMAIL_HOST_USER, [korisnici_email])
            except SMTPException as e:
                print(f"failed to send mail: {e}")

        elif ponuda.status_ponude == 'potencijalan':
            ponuda.stan.status_prodaje = 'dostupan'
            ponuda.stan.save()
            ponuda.odobrenje = False
            ponuda.save()

            CreateContract.delete_contract(ponuda)

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

        # CreateContract.create_contract(request, **kwargs)  # Kreiraj ugovor

        return self.partial_update(request, *args, **kwargs)


class ObrisiPonuduAPIView(generics.RetrieveDestroyAPIView):
    """Brisanje Ponude po ID-ju"""
    permission_classes = [IsAuthenticated, ]
    lookup_field = lookup_field
    queryset = Ponude.objects.all().order_by('-id_ponude')
    serializer_class = PonudeSerializer

    def perform_destroy(self, instance):
        # TODO setovanje stana na osnovu prioriteta ponuda koje ima
        # Kada se obrise jedna ponuda, a postoji jos ostalih ponuda setovati status stana
        # na onu ponudu koja ima najvisi status.
        # Ukoliko nema ponuda nakon brisanja te jedine, setovati status na DOSTUPAN
        CreateContract.delete_contract(instance)
        instance.delete()


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

        @see Generisanje Ugovora: CreateContract
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
                                                    'Key': 'ugovor-br-' + str(queryset.broj_ugovora) + '.docx'
                                                }, ExpiresIn=70000)

        except (FileNotFoundError, Ponude.DoesNotExist):
            raise NotFound('Željeni ugovor nije nađen !', code=404)

        return HttpResponse(url)
