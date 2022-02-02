from django.db import models
from decimal import Decimal


class Lokali(models.Model):
    """Model Entiteta Lokali"""

    class OrijentacijaLokala(models.TextChoices):
        SEVER = 'Sever', "Sever"
        JUG = 'Jug', "Jug"
        ISTOK = 'Istok', "Istok"
        ZAPAD = 'Zapad', "Zapad"

    class StatusProdajeLokala(models.TextChoices):
        DOSTUPAN = 'dostupan', "Dostupan"
        REZERVISAN = 'rezervisan', "Rezervisan"
        PRODAT = 'prodat', "Prodat"

    id_lokala = models.BigAutoField(primary_key=True)

    lamela_lokala = models.CharField('Lamela Lokala',
                                     max_length=50,
                                     default='',
                                     unique=True
                                     )

    adresa_lokala = models.CharField('Adresa Lokala',
                                     max_length=254,
                                     default='',
                                     blank=False,
                                     null=False
                                     )

    kvadratura_lokala = models.DecimalField('Kvadratura Lokala', max_digits=7, decimal_places=2)

    kvadratura_korekcija = models.DecimalField('Korekcija kvadrature',
                                               max_digits=7,
                                               decimal_places=2,
                                               default=0,
                                               blank=True,
                                               )

    # mora se uneti kao decimalni broj, npr 0.97 za korekciju od 3%
    iznos_za_korekciju_kvadrature = models.DecimalField('Iznos za korekciju kvadrature',
                                                        max_digits=3,
                                                        decimal_places=2,
                                                        default=0.97)

    broj_prostorija = models.FloatField('Broj prostorija lokala', default=1)

    napomena_lokala = models.CharField('Napomena Lokala',
                                       null=True,
                                       blank=True,
                                       max_length=250,
                                       default=''
                                       )

    orijentisanost_lokala = models.CharField(max_length=20,
                                             choices=OrijentacijaLokala.choices,
                                             default=OrijentacijaLokala.JUG,
                                             blank=True,
                                             null=True)

    status_prodaje_lokala = models.CharField(max_length=20,
                                             choices=StatusProdajeLokala.choices,
                                             default=StatusProdajeLokala.DOSTUPAN
                                             )

    cena_lokala = models.DecimalField('Cena lokala', max_digits=8, decimal_places=2, default=0)

    cena_kvadrata_lokala = models.DecimalField('Cena kvadrata lokala', max_digits=8, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        """
        Polje 'kvadratura_korekcija' predstavlja korekciju polja 'kvadratura_lokala' za x%
        koje deklarise sam korisnik sistema.
        """

        self.kvadratura_korekcija = Decimal(self.kvadratura_lokala) * Decimal(self.iznos_za_korekciju_kvadrature)

    def __str__(self):
        return f"{self.lamela_lokala}"

    class Meta:
        """
        Prilagodjeni naziv tabele 'Lokali 'u Bazi Podataka.
        """
        db_table: str = 'lokali'
        verbose_name: str = "Lokali"
        verbose_name_plural: str = "Lokali"
        ordering = ['id_lokala']
