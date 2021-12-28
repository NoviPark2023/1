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
    lamela = models.CharField('Lamela', max_length=50, default='')
    adresa_stana = models.CharField('Adresa stana', max_length=254, default='', blank=False, null=False)
    kvadratura = models.DecimalField('Kvadratura stana', max_digits=7, decimal_places=4)
    sprat = models.CharField('Sprat stana', max_length=10, default='1')
    broj_soba = models.FloatField('Broj soba stana', default=1)
    orijentisanost = models.CharField(max_length=20,
                                      choices=OrijentacijaStana.choices,
                                      default=OrijentacijaStana.JUG,
                                      blank=True,
                                      null=True)
    broj_terasa = models.PositiveIntegerField('Broj terasa stana', default=0)
    cena_stana = models.FloatField('Cena stana', default=0)
    napomena = models.CharField('Napomena', null=True, blank=True, max_length=250, default='')
    status_prodaje = models.CharField(max_length=20,
                                      choices=StatusProdaje.choices,
                                      default=StatusProdaje.DOSTUPAN)

    def __str__(self):
        return f"{self.id_stana}, {self.lamela}, {self.kvadratura}"

    class Meta:
        db_table = 'stanovi'
        verbose_name = "Stan"
        verbose_name_plural = "Stanovi"
