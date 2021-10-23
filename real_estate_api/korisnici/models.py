from django.contrib.auth.models import AbstractUser
from django.db import models


class Korisnici(AbstractUser):
    class PrivilegijeKorisnika(models.TextChoices):
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
        return f"{self.ime} {self.prezime}"

    # def __str__(self):
    #     return f" {self.ime} {self.prezime} {self.korisnicko_ime} {self.lozinka} {self.potvrda_lozinka}  \
    #               {self.is_admin} {self.is_finansije} {self.is_prodavac}"

    class Meta:
        db_table = 'korisnici'
        verbose_name = "Korisnik"
        verbose_name_plural = "Korisnici"
