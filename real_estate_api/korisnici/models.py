from django.contrib.auth.models import AbstractUser
from django.db import models


class Korisnici(AbstractUser):
    """
    Model Entiteta Korisnik
    """

    class PrivilegijeKorisnika(models.TextChoices):
        """
        Privilegije korisnika po PDDu u kontekstu ogranicenja pristupa.
        """
        PRODAVAC = 'Prodavac', 'Prodavac'
        FINANSIJE = 'Finansije', 'Finansije'
        ADMINISTRATOR = 'Administrator', 'Administrator'

    ime = models.CharField('Ime Korisnika', max_length=50, default="")
    prezime = models.CharField('Prezime Korisnika', max_length=50, default="")
    role = models.CharField(max_length=40,
                            choices=PrivilegijeKorisnika.choices,
                            default=PrivilegijeKorisnika.ADMINISTRATOR,
                            blank=False,
                            null=False)

    def __repr__(self):
        return self.ime + 'ime' + self.prezime + 'prezime' + 'je dodat.'

    def __str__(self):
        return f"{self.username} {self.ime} {self.prezime}"

    class Meta:
        """
        Prilagodjeni naziv tabele 'Korisnici' u Bazi Podataka.
        """
        db_table = 'korisnici'
        verbose_name = "Korisnik"
        verbose_name_plural = "Korisnici"
