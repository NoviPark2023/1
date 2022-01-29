from django.db import models

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.stanovi.models import Stanovi


class Ponude(models.Model):
    """
    Model Entiteta Ponude Stana.
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
                              related_name='lista_ponuda_kupca'
                              )

    stan = models.ForeignKey(Stanovi,
                             on_delete=models.CASCADE,
                             db_column='id_stana',
                             related_name='lista_ponuda_stana'
                             )

    '''
        * null=True || zato sto kada se kreira stan ne znamo kom klijentu ce se dodeliti.
        * models.SET_NULL || Jer kada se obrise iz sistema Klijent svi stanovi ostaju.
       '''
    klijent_prodaje = models.ForeignKey(Korisnici,
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL
                                        )

    cena_stana_za_kupca = models.FloatField('Cena stana za kupca', default=0)

    napomena = models.CharField("Napomena", max_length=252,
                                default="",
                                blank=True
                                )

    broj_ugovora = models.CharField("Broj Ugovora", max_length=252,
                                    default="",
                                    blank=True,
                                    unique=True
                                    )

    datum_ugovora = models.DateField("Datum Ponude", null=True, blank=True)

    status_ponude = models.CharField(max_length=20,
                                     choices=StatusPonude.choices,
                                     null=False, blank=False,
                                     default=StatusPonude.POTENCIJALAN
                                     )

    nacin_placanja = models.CharField("Nacin Placanja", max_length=30,
                                      choices=NacinPlacanja.choices,
                                      null=False, blank=False,
                                      default=NacinPlacanja.U_CELOSTI
                                      )

    odobrenje = models.BooleanField("Odobrenje", default=False)

    @property
    def ime_kupca(self):
        """Return field 'ime_kupca' for Ponuda serializers and in front form table"""
        return self.kupac.ime_prezime

    @property
    def adresa_stana(self):
        """Return field 'adresa_stana' for Ponuda serializers"""
        return self.stan.adresa_stana

    @property
    def cena_stana(self):
        """Return field 'cena_stana' for Ponuda serializers"""
        cena_stana_formatirana = round(self.stan.cena_stana, 2)
        return cena_stana_formatirana

    @property
    def lamela_stana(self):
        """Return field 'lamela' for Ponuda serializers"""
        return self.stan.lamela

    def __str__(self):
        return f"{self.klijent_prodaje.ime} {self.kupac.id_kupca} {self.cena_stana_za_kupca} \
                  {self.broj_ugovora} {self.kupac.ime_prezime} {self.stan.adresa_stana} {self.stan.adresa_stana}"

    class Meta:
        """
        Prilagodjeni naziv tabele 'Ponude 'u Bazi Podataka.
        """
        db_table = 'ponude'
        verbose_name = "Ponuda Kupcima"
        verbose_name_plural = "Ponude Kupcima"
        ordering = ['-id_ponude']
