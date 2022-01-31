from django.db import models

from real_estate_api.garaze.models import Garaze
from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci


class GarazePonude(models.Model):
    """
    Model Entiteta Ponuda Garaza.
    """

    class StatusPonudeGaraza(models.TextChoices):
        """
        Status Ponuda Garaza u kontekstu prodaje Garaza (Dostupna, Rezervisana, Prodata).
        """
        DOSTUPNA = 'dostupna', "Dostupna"
        REZERVISANA = 'rezervisana', "Rezervisana"
        PRODATA = 'prodata', "Prodata"

    class NacinPlacanjaGaraze(models.TextChoices):
        """
        Nacin placanja Garaze po PDDu (Kredit, U celosti, Na rate, Ucesce).
        """
        U_CELOSTI = 'ceo_iznos', "Placanje u celosti"
        KREDIT = 'kredit', "Kreditom"
        RATE = 'na_rate', "Na rate"
        UCESCE = 'ucesce', "Učešće"

    id_ponude_garaze = models.BigAutoField(primary_key=True)

    garaza = models.ForeignKey(Garaze,
                             on_delete=models.CASCADE,
                             db_column='jedinstveni_broj_garaze',
                             related_name='lista_ponuda_garaza'
                             )

    kupac_garaze = models.ForeignKey(Kupci,
                                     on_delete=models.CASCADE,
                                     db_column='id_kupca',
                                     related_name='lista_ponuda_kupca_garaza'
                                     )

    '''
        * null=True || zato sto kada se kreira ponuda garaze ne znamo kom klijentu ce se dodeliti.
        * models.SET_NULL || Jer kada se obrise iz sistema Klijent sve garaze ostaju.
    '''
    klijent_prodaje_garaze = models.ForeignKey(Korisnici,
                                               null=True,
                                               blank=True,
                                               on_delete=models.SET_NULL
                                               )

    cena_garaze_za_kupca = models.FloatField('Cena Garaze za kupca', default=0)

    napomena_ponude_garaze = models.CharField("Napomena Garaze", max_length=252,
                                              default="Nema Napomene",
                                              blank=True
                                              )

    broj_ugovora_garaze = models.CharField("Broj Ugovora Garaze", max_length=252,
                                           blank=True,
                                           null=True,
                                           unique=True
                                           )

    datum_ugovora_garaze = models.DateField("Datum Ponude Garaze", null=True, blank=True)

    status_ponude_garaze = models.CharField(max_length=20,
                                            choices=StatusPonudeGaraza.choices,
                                            null=False, blank=False,
                                            default=StatusPonudeGaraza.DOSTUPNA
                                            )

    nacin_placanja_garaze = models.CharField("Nacin Placanja Garaze",
                                             max_length=30,
                                             choices=NacinPlacanjaGaraze.choices,
                                             null=False, blank=False,
                                             default=NacinPlacanjaGaraze.U_CELOSTI
                                             )

    odobrenje_ponude_garaze = models.BooleanField("Odobrenje Ponude Garaze",
                                                  default=False
                                                  )

    @property
    def ime_kupca_garaze(self):
        """Return field 'ime_kupca' for Ponude Garaza serializers and in front form table"""
        return self.kupac_garaze.ime_prezime

    def __str__(self):
        return (
            f"{self.klijent_prodaje_garaze.ime}"
            f" {self.kupac_garaze.id_kupca}"
            f" {self.cena_garaze_za_kupca}"
            f" {self.broj_ugovora_garaze}"
            f" {self.kupac_garaze.ime_prezime}"
        )

    class Meta:
        """
        Prilagodjeni naziv tabele 'Ponude Garaza 'u Bazi Podataka.
        """
        db_table = 'ponude_garaze'
        verbose_name = "Ponuda Kupcima Garaze"
        verbose_name_plural = "Ponude Kupcima Garaze"
        ordering = ['id_ponude_garaze']
