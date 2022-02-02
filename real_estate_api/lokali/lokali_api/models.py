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

    kvadratura_lokala = models.DecimalField('Kvadratura Lokala', max_digits=7, decimal_places=2)

    napomena_lokala = models.CharField('Napomena Lokala',
                                       null=True,
                                       blank=True,
                                       max_length=250,
                                       default=''
                                       )

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
