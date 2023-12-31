from django.db import models


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

    kvadratura_lokala = models.FloatField('Kvadratura Lokala', null=False, blank=False, default=0.0)

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

    cena_lokala = models.FloatField('Cena lokala', null=False, blank=False, default=0)

    def __str__(self):
        return f"{self.id_lokala}, {self.lamela_lokala}"

    class Meta:
        """
        Prilagodjeni naziv tabele 'Lokali 'u Bazi Podataka.
        """
        db_table: str = 'lokali'
        verbose_name: str = "Lokali"
        verbose_name_plural: str = "Lokali"
        ordering = ['id_lokala']
