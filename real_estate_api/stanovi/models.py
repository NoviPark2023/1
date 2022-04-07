from decimal import Decimal

from django.db import models, IntegrityError
from django.http import Http404
from rest_framework.exceptions import APIException


class Stanovi(models.Model):
    class OrijentacijaStana(models.TextChoices):
        SEVER = 'Sever', "Sever"
        JUG = 'Jug', "Jug"
        ISTOK = 'Istok', "Istok"
        ZAPAD = 'Zapad', "Zapad"

    class StatusProdaje(models.TextChoices):
        DOSTUPAN = 'dostupan', "Dostupan"
        REZERVISAN = 'rezervisan', "Rezervisan"
        PRODAT = 'prodat', "Prodat"

    id_stana = models.BigAutoField(primary_key=True)

    lamela = models.CharField('Lamela',
                              max_length=50,
                              default='',
                              unique=True
                              )

    adresa_stana = models.CharField('Adresa stana',
                                    max_length=254,
                                    default='',
                                    blank=False,
                                    null=False
                                    )

    kvadratura = models.DecimalField('Kvadratura stana', max_digits=7, decimal_places=2)

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

    sprat = models.CharField('Sprat stana', max_length=10, default='1')

    broj_soba = models.FloatField('Broj soba stana', default=1)

    orijentisanost = models.CharField(max_length=20,
                                      choices=OrijentacijaStana.choices,
                                      default=OrijentacijaStana.JUG,
                                      blank=True,
                                      null=True
                                      )

    broj_terasa = models.PositiveIntegerField('Broj terasa stana', default=0)

    unesena_mauelna_cena_stana = models.BooleanField("Manuelan Unos Cene Stana",
                                                     default=False,
                                                     blank=True,
                                                     null=True
                                                     )

    cena_stana = models.DecimalField('Cena stana', max_digits=8, decimal_places=2,
                                     default=0)

    cena_kvadrata = models.DecimalField('Cena kvadrata', max_digits=8, decimal_places=2,
                                        default=0)

    napomena = models.CharField('Napomena', null=True, blank=True, max_length=250,
                                default='')

    status_prodaje = models.CharField(max_length=20,
                                      choices=StatusProdaje.choices,
                                      default=StatusProdaje.DOSTUPAN)

    def __str__(self):
        return f"{self.id_stana}, {self.lamela}, {self.kvadratura}"

    def save(self, *args, **kwargs):
        """
        Automatsko izracunavanje cene kvadrata na osnovu predefinisanih pravila Korisnika.
        Izracunavanje cene se odvija nad korigovanom kvadraturom.
        Cena se izracunava prilikom samog unosa Stana u sistem.

          * Polje 'kvadratura_korekcija' predstavlja korekciju polja 'kvadratura' za x%
            koje deklarise sam korisnik sistema.
          * Cena Stana se odredjuje po 3 parametra (sprat, broj soba, orijentacija)
          * Pronalazimo cenu tako sto filtriramo tabelu 'azuriranje_cena' po ova 3 parametra.

        Ukoliko je polje "unesena_mauelna_cena_stana" TRUE, tada je markiran Stan za
        manuelni unos cene i nije potrebno za isti da se radi Automatsko izracunavanje
        cene.
        ---
        @param args: none
        @param kwargs: none
        @save: Korigovanu cenu Stana
        """

        if self.unesena_mauelna_cena_stana:
            return super(Stanovi, self).save(*args, **kwargs)
        else:
            try:

                self.kvadratura_korekcija = Decimal(self.kvadratura) * Decimal(
                    self.iznos_za_korekciju_kvadrature)

                pronadji_cenu_stana = AzuriranjeCena.objects.get(
                    sprat=self.sprat,
                    broj_soba=float(self.broj_soba),
                    orijentisanost=self.orijentisanost
                )

                # Izracunaj Cenu Stana
                self.cena_stana = self.kvadratura_korekcija * pronadji_cenu_stana.cena_kvadrata

                self.cena_kvadrata = pronadji_cenu_stana.cena_kvadrata

            except AzuriranjeCena.DoesNotExist:
                raise Http404("Konfiguracija Auzriranja cena ne postoji u sistemu.")

            return super(Stanovi, self).save(*args, **kwargs)

    class Meta:
        db_table = 'stanovi'
        verbose_name = "Stan"
        verbose_name_plural = "Stanovi"


class AzuriranjeCena(models.Model):
    """
    Pomocna klasa(tabela) koja sluzi za automatsku kalkulaciju cena Stanova
    pri samom unosu Stana.
    """

    class OrijentacijaStana(models.TextChoices):
        SEVER = 'Sever', "Sever"
        JUG = 'Jug', "Jug"
        ISTOK = 'Istok', "Istok"
        ZAPAD = 'Zapad', "Zapad"

    id_azur_cene = models.BigAutoField(primary_key=True)

    sprat = models.CharField('Sprat stana', max_length=10, default='1')

    broj_soba = models.FloatField('Broj soba stana', default=1)

    orijentisanost = models.CharField(max_length=20,
                                      choices=OrijentacijaStana.choices,
                                      default=OrijentacijaStana.JUG,
                                      blank=True,
                                      null=True
                                      )

    cena_kvadrata = models.DecimalField('Cena kvadrata', max_digits=8, decimal_places=2,
                                        default=0)

    def save(self, *args, **kwargs):

        try:
            stanovi = Stanovi.objects.all().filter(unesena_mauelna_cena_stana=False)

            for stan in stanovi:
                pronadji_cenu_stana = AzuriranjeCena.objects.get(
                    sprat=stan.sprat,
                    broj_soba=float(stan.broj_soba),
                    orijentisanost=stan.orijentisanost
                )
                if (
                    self.sprat == stan.sprat and
                    self.broj_soba == stan.broj_soba and
                    self.orijentisanost == stan.orijentisanost
                ):
                    # Sacuvaj prvo azuriranu cenu
                    super(AzuriranjeCena, self).save(*args, **kwargs)

                    # Izracunaj Cenu Stana
                    stan.cena_stana = stan.kvadratura_korekcija * pronadji_cenu_stana.cena_kvadrata

                    stan.cena_kvadrata = pronadji_cenu_stana.cena_kvadrata

                    Stanovi.save(stan)

                return super(AzuriranjeCena, self).save(*args, **kwargs)
            return super(AzuriranjeCena, self).save(*args, **kwargs)

        except Exception:
            raise APIException(f"Ne moze da se unese Azuriranje Cene.")

    class Meta:
        db_table = 'azuriranje_cena'
        verbose_name = "AzuriranjeCena"
        verbose_name_plural = "AzuriranjeCena"
