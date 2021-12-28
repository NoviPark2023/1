from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import datetime


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, password, email, ime, prezime, **druga_polja):

        druga_polja.setdefault('is_staff', True)
        druga_polja.setdefault('is_superuser', True)
        druga_polja.setdefault('is_active', True)

        if druga_polja.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if druga_polja.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, password, email, ime, prezime, **druga_polja)

    def create_user(self, username, password, email, ime, prezime, **druga_polja):

        if not email:
            raise ValueError('You must provide an email address')

        user = self.model(username=username,
                          password=password,
                          email=email,
                          ime=ime,
                          prezime=prezime,
                          **druga_polja)
        user.set_password(password)
        user.save(using=self.db)
        return user


class Korisnici(AbstractBaseUser, PermissionsMixin):
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

    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=150, unique=True)
    start_date = models.DateField(default=datetime.date.today)

    ime = models.CharField('Ime Korisnika', max_length=50, default="")
    prezime = models.CharField('Prezime Korisnika', max_length=50, default="")
    role = models.CharField(max_length=40,
                            choices=PrivilegijeKorisnika.choices,
                            default=PrivilegijeKorisnika.ADMINISTRATOR,
                            blank=False,
                            null=False)

    about = models.TextField('about', max_length=500, blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['ime', 'email', 'prezime']

    def __str__(self):
        return f"{self.username} {self.ime} {self.prezime}"

    class Meta:
        """
        Prilagodjeni naziv tabele 'Korisnici' u Bazi Podataka.
        """
        db_table = 'korisnici'
        verbose_name = "Korisnik"
        verbose_name_plural = "Korisnici"
        ordering = ['-ime']
