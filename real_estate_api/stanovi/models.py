from decimal import Decimal

from django.db import models


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

    cena_stana = models.DecimalField('Cena stana', max_digits=8, decimal_places=2, default=0)

    cena_kvadrata = models.DecimalField('Cena kvadrata', max_digits=8, decimal_places=2, default=0)

    napomena = models.CharField('Napomena', null=True, blank=True, max_length=250, default='')

    status_prodaje = models.CharField(max_length=20,
                                      choices=StatusProdaje.choices,
                                      default=StatusProdaje.DOSTUPAN)

    def save(self, *args, **kwargs):
        """
        Automatsko izracunavanje cene kvadrata na osnovu predefinisanih pravila Korisnika.
        Izracunavanje cene se odvija nad korigovanom kvadraturom.
        Cena se izracunava prilikom samog unosa Stana u sistem.

          * Polje 'kvadratura_korekcija' predstavlja korekciju polja 'kvadratura' za x%
            koje deklarise sam korisnik sistema.
          * Cena Stana se odredjuje po 3 parametra (sprat, broj soba, orijentacija)
          * Pronalazimo cenu tako sto filtriramo tabelu 'azuriranje_cena' po ova 3 parametra.
        ---
        @param args: none
        @param kwargs: none
        @save: Korigovanu cenu Stana
        """

        self.kvadratura_korekcija = Decimal(self.kvadratura) * Decimal(self.iznos_za_korekciju_kvadrature)

        # TODO: Izostavi sve Stanove koji imaju polje "unesena_mauelna_cena_stana" TRUE !
        # TODO: Takodje implementirati Exeption ako nema postavke za stan u Azuriranju cena (Orijent-Sprat-Sobe).
        pronadji_cenu_stana = AzuriranjeCena.objects.get(
            sprat=self.sprat,
            broj_soba=float(self.broj_soba),
            orijentisanost=self.orijentisanost
        )

        # Izracunaj Cenu Stana
        self.cena_stana = self.kvadratura_korekcija * pronadji_cenu_stana.cena_kvadrata

        # Moze .first() jer samo jedna cena moze da se pronadje
        self.cena_kvadrata = pronadji_cenu_stana.cena_kvadrata

        return super(Stanovi, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_stana}, {self.lamela}, {self.kvadratura}"

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

    cena_kvadrata = models.DecimalField('Cena kvadrata', max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = 'azuriranje_cena'
        verbose_name = "AzuriranjeCena"
        verbose_name_plural = "AzuriranjeCena"
