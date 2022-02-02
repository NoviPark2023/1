from django.db import models
from real_estate_api.kupci.models import Kupci


class Garaze(models.Model):
    """
    Model Entiteta Garaza.
    """

    class StatusProdajeGaraze(models.TextChoices):
        DOSTUPNA = 'dostupna', "Dostupna"
        REZERVISANA = 'rezervisana', "Rezervisana"
        PRODATA = 'prodata', "Prodata"

    id_garaze = models.BigAutoField(primary_key=True)

    jedinstveni_broj_garaze = models.PositiveIntegerField('Broj Garaze',
                                                          null=False,
                                                          blank=False,
                                                          unique=True
                                                          )

    cena_garaze = models.FloatField('Cena Garaze',
                                    null=False,
                                    blank=False,
                                    default=0.0
                                    )

    napomena_garaze = models.CharField('Napomena',
                                       null=True,
                                       blank=True,
                                       max_length=250,
                                       default='Nema Napomene'
                                       )

    status_prodaje_garaze = models.CharField(max_length=20,
                                             choices=StatusProdajeGaraze.choices,
                                             default=StatusProdajeGaraze.DOSTUPNA
                                             )

    kupac = models.ForeignKey(Kupci,
                              on_delete=models.SET_NULL,
                              db_column='id_kupca',
                              related_name='lista_garaza_kupca',
                              blank=True,
                              null=True,
                              )

    @property
    def ime_kupca(self):
        """Return field 'ime_kupca' for Garaze serializers and in front form table"""
        return self.kupac.ime_prezime

    def __str__(self):
        return f"{self.jedinstveni_broj_garaze}"

    class Meta:
        """
        Prilagodjeni naziv tabele 'Garaze 'u Bazi Podataka.
        """
        db_table: str = 'garaze'
        verbose_name: str = "Garaze"
        verbose_name_plural: str = "Garaze"
        ordering = ['jedinstveni_broj_garaze']
