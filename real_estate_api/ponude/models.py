from django.db import models
import datetime

from real_estate_api.kupci.models import Kupci
from real_estate_api.stanovi.models import Stanovi


class Ponude(models.Model):
    """
    Model Entiteta Ponude
    """

    class StatusPonude(models.TextChoices):
        """
        Status Ponuda Stana po PDDu u kontekstu prodaje Stana (Potencijalan, Rezervisan, Kupljen).
        """
        POTENCIJALAN = 'potencijalan', "Potencijalan"
        REZERVISAN = 'rezervisan', "Rezervisan"
        KUPLJEN = 'kupljen', "Kupljen"

    class NacinPlacanja(models.TextChoices):
        """
        Nacin placanja Stana po PDDu u kontekstu prodaje Stana (Kredit, U celosti, Na rate, Ucesce).
        """
        U_CELOSTI = 'ceo_iznos', "Placanje u celosti"
        KREDIT = 'kredit', "Kreditom"
        RATE = 'na_rate', "Na rate"
        UCESCE = 'ucesce', "Učešće"

    id_ponude = models.BigAutoField(primary_key=True)
    kupac = models.ForeignKey(Kupci,
                              on_delete=models.CASCADE,
                              db_column='id_kupca',
                              related_name='lista_ponuda_kupca')

    stan = models.ForeignKey(Stanovi,
                             on_delete=models.CASCADE,
                             db_column='id_stana',
                             related_name='lista_ponuda_stana')

    cena_stana_za_kupca = models.PositiveIntegerField('Cena stana za kupca', default=0)
    napomena = models.CharField(max_length=252, default="", blank=True)
    broj_ugovora = models.CharField(max_length=252, default="", blank=True)
    datum_ugovora = models.DateField(default=datetime.date.today)
    status_ponude = models.CharField(max_length=20,
                                     choices=StatusPonude.choices,
                                     null=False, blank=False,
                                     default=StatusPonude.POTENCIJALAN)

    nacin_placanja = models.CharField(max_length=30,
                                      choices=NacinPlacanja.choices,
                                      null=False, blank=False,
                                      default=NacinPlacanja.U_CELOSTI)

    odobrenje = models.BooleanField(default=False)

    @property
    def adresa_stana(self):
        """Return field 'adresa_stana' for Ponuda serializers"""
        return self.stan.adresa_stana

    @property
    def cena_stana(self):
        """Return field 'cena_stana' for Ponuda serializers"""
        return self.stan.cena_stana

    def __str__(self):
        return f"{self.kupac.id_kupca} {self.cena_stana_za_kupca} \
                  {self.broj_ugovora} {self.kupac.ime_prezime} {self.stan.adresa_stana}"

    class Meta:
        """
        Prilagodjeni naziv tabele 'Ponude 'u Bazi Podataka.
        """
        db_table = 'ponude'
        verbose_name = "Ponuda Kupcima"
        verbose_name_plural = "Ponude Kupcima"
        ordering = ['-id_ponude']
