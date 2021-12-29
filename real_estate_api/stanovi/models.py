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
                                                blank=True
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
                                      null=True)
    broj_terasa = models.PositiveIntegerField('Broj terasa stana', default=0)

    cena_stana = models.DecimalField('Cena stana', max_digits=8, decimal_places=2, default=0)

    cena_kvadrata = models.DecimalField('Cena kvadrata', max_digits=8, decimal_places=2, default=0)

    napomena = models.CharField('Napomena', null=True, blank=True, max_length=250, default='')

    status_prodaje = models.CharField(max_length=20,
                                      choices=StatusProdaje.choices,
                                      default=StatusProdaje.DOSTUPAN)

    def save(self, *args, **kwargs):
        """
        Polje 'kvadratura_korekcija' predstavlja korekciju polja 'kvadratura' za x%.
        @param args: none
        @param kwargs: none
        @return: kvadratura_korekcija
        """

        self.kvadratura_korekcija = self.kvadratura * self.iznos_za_korekciju_kvadrature
        self.cena_stana = self.kvadratura_korekcija * self.cena_kvadrata

        test = AzuriranjeCena.objects.all().values()
        # for stan in test:

        # QuerySet AzuriranjeCena mapiranja
        sprat_tbl = test[0]['sprat']
        broj_soba_tbl = test[0]['broj_soba']
        orijentisanost_tbl = test[0]['orijentisanost']
        cena_kvadrata_tbl = test[0]['cena_kvadrata']

        # Stan Objects
        sprat_obj: str = self.sprat
        broj_soba_obj: float = float(self.broj_soba)
        orijentisanost_obj: str = self.orijentisanost

        if sprat_obj == sprat_tbl and broj_soba_obj == broj_soba_tbl and orijentisanost_obj == orijentisanost_tbl:
            self.cena_stana = (float(self.kvadratura_korekcija)) * float(cena_kvadrata_tbl)
            print(self.id_stana, self.cena_stana)
            self.save()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_stana}, {self.lamela}, {self.kvadratura}"

    class Meta:
        db_table = 'stanovi'
        verbose_name = "Stan"
        verbose_name_plural = "Stanovi"


class AzuriranjeCena(models.Model):

    class OrijentacijaStana(models.TextChoices):
        SEVER = 'Sever', "Sever"
        JUG = 'Jug', "Jug"
        ISTOK = 'Istok', "Istok"
        ZAPAD = 'Zapad', "Zapad"

    sprat = models.CharField('Sprat stana', max_length=10, default='1')
    broj_soba = models.FloatField('Broj soba stana', default=1)
    orijentisanost = models.CharField(max_length=20,
                                      choices=OrijentacijaStana.choices,
                                      default=OrijentacijaStana.JUG,
                                      blank=True,
                                      null=True)
    cena_kvadrata = models.DecimalField('Cena kvadrata', max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = 'azuriranje_cena'
        verbose_name = "AzuriranjeCena"
        verbose_name_plural = "AzuriranjeCena"
