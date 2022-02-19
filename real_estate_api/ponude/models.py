from django.db import models
from django.db.models import Q
from docx.opc.exceptions import PackageNotFoundError

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.ponude.ugovor.ugovori import Contract
from real_estate_api.stanovi.models import Stanovi


class Ponude(models.Model):
    """
    Model Entiteta Ponude Stana.
    """

    class StatusPonude(models.TextChoices):
        """
        Status Ponuda Stana po PDDu u kontekstu prodaje Stana (Potencijalan, Rezervisan, Kupljen).
        """
        POTENCIJALAN = 'potencijalan', "Potencijalan"
        REZERVISAN = 'rezervisan', "Rezervisan"
        KUPLJEN = 'kupljen', "Kupljen"

    class NacinPlacanja(models.TextChoices):
        """
        Nacin placanja Stana po PDDu u kontekstu prodaje Stana (Kredit, U celosti, Na rate, Ucesce).
        """
        U_CELOSTI = 'Ceo iznos', "Placanje u celosti"
        KREDIT = 'Kredit', "Kreditom"
        RATE = 'Na rate', "Na rate"
        UCESCE = 'Ucesce', "Učešće"

    id_ponude = models.BigAutoField(primary_key=True)

    kupac = models.ForeignKey(Kupci,
                              on_delete=models.CASCADE,
                              db_column='id_kupca',
                              related_name='lista_ponuda_kupca'
                              )

    stan = models.ForeignKey(Stanovi,
                             on_delete=models.CASCADE,
                             db_column='id_stana',
                             related_name='lista_ponuda_stana'
                             )

    '''
        * null=True || zato sto kada se kreira stan ne znamo kom klijentu ce se dodeliti.
        * models.SET_NULL || Jer kada se obrise iz sistema Klijent svi stanovi ostaju.
       '''
    klijent_prodaje = models.ForeignKey(Korisnici,
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL
                                        )

    cena_stana_za_kupca = models.FloatField('Cena stana za kupca', default=0)

    napomena = models.CharField("Napomena",
                                max_length=252,
                                default="",
                                blank=True
                                )

    broj_ugovora = models.CharField("Broj Ugovora",
                                    max_length=252,
                                    blank=True,
                                    null=True,
                                    unique=True
                                    )

    datum_ugovora = models.DateField("Datum Ponude", null=True, blank=True)

    status_ponude = models.CharField(max_length=20,
                                     choices=StatusPonude.choices,
                                     null=False,
                                     blank=False,
                                     default=StatusPonude.POTENCIJALAN
                                     )

    nacin_placanja = models.CharField("Nacin Placanja",
                                      max_length=30,
                                      choices=NacinPlacanja.choices,
                                      null=False, blank=False,
                                      default=NacinPlacanja.U_CELOSTI
                                      )

    odobrenje = models.BooleanField("Odobrenje", default=False)

    @property
    def ime_kupca(self):
        """Return field 'ime_kupca' for Ponuda serializers and in front form table"""
        return self.kupac.ime_prezime

    @property
    def adresa_stana(self):
        """Return field 'adresa_stana' for Ponuda serializers"""
        return self.stan.adresa_stana

    @property
    def cena_stana(self):
        """Return field 'cena_stana' for Ponuda serializers"""
        cena_stana_formatirana = round(self.stan.cena_stana, 2)
        return cena_stana_formatirana

    @property
    def lamela_stana(self):
        """Return field 'lamela' for Ponuda serializers"""
        return self.stan.lamela

    def __str__(self):
        return f" {self.kupac.id_kupca}" \
               f" {self.cena_stana_za_kupca} \
                  {self.broj_ugovora}" \
               f" {self.kupac.ime_prezime}" \
               f" {self.stan.adresa_stana}" \
               f" {self.stan.adresa_stana}"

    def save(self, *args, **kwargs):
        """
        Prilikom cuvanja Ponude potrebno je setovati status Stana korespondno statusu
        Ponude.
        Statusi imaju svoju hijerahiju po kojoj je Ponuda sa statusom "KUPLJEN" na najvisem
        nivou i ukoliko postoji u ponudama, status Stana se setuje na "KUPLJEN".
        Sledece u hijerahiji je status "REZERVISAN", po istom principu kao i gorespomenuto.
        Na kraju je status "DOSTUPAN".

        :param args: None
        :param kwargs: 'force_insert': True, 'using': 'default'
        """
        super(Ponude, self).save(*args, **kwargs)

        status_rezervisan = Ponude.StatusPonude.REZERVISAN
        status_kupljen = Ponude.StatusPonude.KUPLJEN

        status_rezervisan = Ponude.objects.filter(Q(status_ponude=status_rezervisan)).filter(
            stan__id_stana=self.stan.id_stana).exists()

        status_kupljen = Ponude.objects.filter(Q(status_ponude=status_kupljen)).filter(
            stan__id_stana=self.stan.id_stana).exists()

        if status_kupljen:
            self.stan.status_prodaje = Stanovi.StatusProdaje.PRODAT
            self.odobrenje = True

            try:
                Contract.create_contract(self, self.stan, self.kupac)  # Kreiraj Ugovor.
            except PackageNotFoundError:
                print("Paket za kreiranje Ugovora nije nadjen.")

        elif status_rezervisan and not status_kupljen:
            self.stan.status_prodaje = Stanovi.StatusProdaje.REZERVISAN
            self.odobrenje = True

            try:
                Contract.create_contract(self, self.stan, self.kupac)  # Kreiraj Ugovor.
            except PackageNotFoundError:
                print("Paket za kreiranje Ugovora nije nadjen.")

        elif not status_kupljen or not status_rezervisan:
            self.stan.status_prodaje = Stanovi.StatusProdaje.DOSTUPAN
            self.odobrenje = False

        self.stan.save()

    def delete(self, *args, **kwargs):
        """
        Prilikom brisanja Ponude potrebno je setovati status Stana korespondno statusu
        Ponude.
        Statusi imaju svoju hijerahiju po kojoj je Ponuda sa statusom "KUPLJEN" na najvisem
        nivou i ukoliko postoji u ponudama, status Stana se setuje na "KUPLJEN".
        Sledece u hijerahiji je status "REZERVISAN", po istom principu kao i gorespomenuto.
        Na kraju je status "DOSTUPAN".

        :param args: None
        :param kwargs: 'force_insert': True, 'using': 'default'
        """
        super(Ponude, self).delete(*args, **kwargs)

        status_rezervisan = Ponude.StatusPonude.REZERVISAN
        status_kupljen = Ponude.StatusPonude.KUPLJEN

        status_rezervisan = Ponude.objects.filter(Q(status_ponude=status_rezervisan)).filter(
            stan__id_stana=self.stan.id_stana).exists()

        status_kupljen = Ponude.objects.filter(Q(status_ponude=status_kupljen)).filter(
            stan__id_stana=self.stan.id_stana).exists()

        if status_kupljen:
            self.stan.status_prodaje = Stanovi.StatusProdaje.PRODAT
        elif status_rezervisan and not status_kupljen:
            self.stan.status_prodaje = Stanovi.StatusProdaje.REZERVISAN
        elif not status_kupljen or not status_rezervisan:
            self.stan.status_prodaje = Stanovi.StatusProdaje.DOSTUPAN

        self.stan.save()

    class Meta:
        """
        Prilagodjeni naziv tabele 'Ponude 'u Bazi Podataka.
        """
        db_table = 'ponude'
        verbose_name = "Ponuda Kupcima"
        verbose_name_plural = "Ponude Kupcima"
        ordering = ['-id_ponude']
