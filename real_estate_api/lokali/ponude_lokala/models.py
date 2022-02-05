from django.db import models

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.lokali.lokali_api.models import Lokali


class PonudeLokala(models.Model):
    """
    Model Entiteta Ponude Lokala.
    """

    class StatusPonudeLokala(models.TextChoices):
        """
        Status Ponuda Lokala po PDDu u kontekstu prodaje Stana (Potencijalan, Rezervisan, Kupljen).
        """
        POTENCIJALAN = 'potencijalan', "Potencijalan"
        REZERVISAN = 'rezervisan', "Rezervisan"
        KUPLJEN = 'kupljen', "Kupljen"

    class NacinPlacanjaLokala(models.TextChoices):
        """
        Nacin placanja Stana po PDDu u kontekstu prodaje Stana (Kredit, U celosti, Na rate, Ucesce).
        """
        U_CELOSTI = 'ceo_iznos', "Placanje u celosti"
        KREDIT = 'kredit', "Kreditom"
        RATE = 'na_rate', "Na rate"
        UCESCE = 'ucesce', "Učešće"

    id_ponude_lokala = models.BigAutoField(primary_key=True)

    kupac_lokala = models.ForeignKey(Kupci,
                                     on_delete=models.CASCADE,
                                     db_column='id_kupca',
                                     related_name='lista_ponuda_kupca_lokala'
                                     )

    lokali = models.ForeignKey(Lokali,
                               on_delete=models.CASCADE,
                               db_column='id_lokala',
                               related_name='lista_ponuda_lokala'
                               )

    '''
        * null=True || zato sto kada se kreira Lokal ne znamo kom klijentu ce se dodeliti.
        * models.SET_NULL || Jer kada se obrise iz sistema Klijent svi lokali ostaju.
    '''
    klijent_prodaje_lokala = models.ForeignKey(Korisnici,
                                               null=True,
                                               blank=True,
                                               on_delete=models.SET_NULL
                                               )

    cena_lokala_za_kupca = models.FloatField('Cena Lokala za kupca', default=0)

    napomena_ponude_lokala = models.CharField("Napomena Ponude Lokala",
                                              max_length=252,
                                              default="",
                                              null=True,
                                              blank=True
                                              )

    broj_ugovora_lokala = models.CharField("Broj Ugovora Lokala",
                                           max_length=252,
                                           blank=True,
                                           null=True,
                                           unique=True
                                           )

    datum_ugovora_lokala = models.DateField("Datum Ponude Lokala", null=True, blank=True)

    status_ponude_lokala = models.CharField(max_length=20,
                                            choices=StatusPonudeLokala.choices,
                                            null=False,
                                            blank=False,
                                            default=StatusPonudeLokala.POTENCIJALAN
                                            )

    nacin_placanja_lokala = models.CharField("Nacin Placanja Lokala",
                                             max_length=30,
                                             choices=NacinPlacanjaLokala.choices,
                                             null=False,
                                             blank=False,
                                             default=NacinPlacanjaLokala.U_CELOSTI
                                             )

    odobrenje_kupovine_lokala = models.BooleanField("Odobrenje Kupovine Lokala", default=False)

    @property
    def ime_kupca_lokala(self):
        """Return field 'ime_kupca' for Ponuda Lokala serializers and in front form table"""
        return self.kupac_lokala.ime_prezime

    @property
    def adresa_lokala(self):
        """Return field 'adresa_lokala' for Ponude Lokala serializers"""
        return self.lokali.adresa_lokala

    @property
    def lamela_lokala(self):
        """Return field 'lamela_lokala' for Ponuda Lokali serializers"""
        return self.lokali.lamela_lokala

    @property
    def cena_lokala(self):
        """Return field 'cena_lokala' for Ponuda Lokala serializers"""
        cena_lokala_formatirana = round(self.lokali.cena_lokala, 2)
        return cena_lokala_formatirana

    def __str__(self):
        return f"{self.lokali.id_lokala} {self.lokali.lamela_lokala}"

    class Meta:
        """
        Prilagodjeni naziv tabele 'Ponude Lokala'u Bazi Podataka.
        """
        db_table = 'ponude_lokala'
        verbose_name = "Ponuda Lokala Kupcima"
        verbose_name_plural = "Ponude Lokala Kupcima"
        ordering = ['-id_ponude_lokala']