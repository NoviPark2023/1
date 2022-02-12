from typing import Union, Any

from django.db import models
from django.db.models import BigAutoField


class Kupci(models.Model):
    """
    Model Entiteta Kupci
    """

    class StatusLicaKupaca(models.TextChoices):
        """
        Status Lica Kupaca po PDDu u kontekstu prodaje (Pravno Lice, Fizicko Lice).
        """
        FIZICKO = 'Fizicko', 'Fizicko Lice'
        PRAVNO = 'Pravno', 'Pravno Lice'

    id_kupca: Union[BigAutoField, Any] = models.BigAutoField(primary_key=True)

    lice: str = models.CharField(max_length=20,
                                 choices=StatusLicaKupaca.choices,
                                 default=StatusLicaKupaca.FIZICKO,
                                 )

    ime_prezime: str = models.CharField('Ime i prezime Kupca', max_length=50, unique=True)

    email: str = models.EmailField('Email Kupca', unique=True)

    broj_telefona: str = models.CharField('Broj telefona', max_length=20, unique=True)

    Jmbg_Pib: str = models.CharField('JMBG ili PIB', max_length=30, unique=True)

    adresa: str = models.CharField('Adresa', max_length=50)

    def get_id_kupca(self) -> object:
        return self.id_kupca + ' id_kupca '

    def __str__(self):
        return f"{self.ime_prezime}"

    class Meta:
        """
        Prilagodjeni naziv tabele 'Kupci 'u Bazi Podataka.
        """
        db_table: str = 'kupci'
        verbose_name: str = "Kupac"
        verbose_name_plural: str = "Kupci"
        ordering = ['-id_kupca']
