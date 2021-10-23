from django.db import models


class Kupci(models.Model):
    STATUS_LICA = (
        ('Fizicko', 'Fizicko Lice'),
        ('Pravno', 'Pravno Lice'),
    )
    id_kupca = models.BigAutoField(primary_key=True)
    lice = models.CharField(max_length=20,
                            choices=STATUS_LICA,
                            default='Fizicko Lice')
    ime_prezime = models.CharField('Ime i prezime Kupca', max_length=50)
    email = models.EmailField('Email Kupca')
    broj_telefona = models.CharField('Broj telefona', max_length=20)
    Jmbg_Pib = models.IntegerField('JMBG ili PIB')
    adresa = models.CharField('Adresa', max_length=50)

    def get_id_kupca(self):
        return self.id_kupca + ' id_kupca ' + self.id_kupca + ' id_kupca.'

    def __repr__(self):
        return self.ime_prezime + ' je dodat.'

    def __str__(self):
        return f"{self.ime_prezime}"

    class Meta:
        db_table = 'kupci'
        verbose_name = "Kupac"
        verbose_name_plural = "Kupci"


