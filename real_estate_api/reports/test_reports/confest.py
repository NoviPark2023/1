import dataclasses
import json
import attr
import datetime
import random

import factory.django
import pytest
from faker import Faker
from dataclasses import dataclass

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi, AzuriranjeCena

fake = Faker()


# region NOVA TRI STANA FIXTURE
@pytest.fixture(autouse=False)
def nova_tri_stana_fixture_reporti(db, kreiraj_tri_auriranja_cena_stanovi) -> Stanovi:
    """
    Kreiranje novih Stanova.

    @param kreiraj_auriranje_cena:  pytest.fixture (kreiraj_tri_auriranja_cena_stanovi)
    @param db: Testna DB.
    @return: Entitet 'Stanovi'.
    """
    stanovi = Stanovi.objects.bulk_create(
        [
            Stanovi(
                id_stana=1,
                lamela="L2.1.S10",
                adresa_stana="Adresa Stana L2.1.S10",
                kvadratura=67.49,
                kvadratura_korekcija=65.47,
                iznos_za_korekciju_kvadrature=0.97,
                sprat="1.0",
                broj_soba=3,
                orijentisanost="Jug",
                broj_terasa="0",
                cena_stana="103085.59",
                cena_kvadrata="1574.66",
                napomena='Nema napomene',
                status_prodaje="dostupan",
            ),
            Stanovi(
                id_stana=2,
                lamela="L3.1.S1",
                adresa_stana="Adresa Stana L3.1.S1",
                kvadratura=50.25,
                kvadratura_korekcija=48.74,
                iznos_za_korekciju_kvadrature=0.97,
                sprat="1.0",
                broj_soba=3,
                orijentisanost="Jug",
                broj_terasa="1",
                cena_stana="76428.24",
                cena_kvadrata="1568.00",
                napomena='Nema napomene',
                status_prodaje="kupljen",
            ),
            Stanovi(
                id_stana=3,
                lamela="L1.1.S4",
                adresa_stana="Adresa Stana L3.1.S1",
                kvadratura=49.23,
                kvadratura_korekcija=47.75,
                iznos_za_korekciju_kvadrature=0.97,
                sprat="1.0",
                broj_soba=2,
                orijentisanost="Sever",
                broj_terasa="1",
                cena_stana="74128.09",
                cena_kvadrata="1552.32",
                napomena='Nema napomene',
                status_prodaje="rezervisan",
            )
        ]

    )

    return stanovi


# endregion


# region NOVO AZURIRANJE CENA FIXTURE REPORTS
@pytest.fixture(autouse=False)
def azuriranje_cena_fixture(db):
    """
    Kreiranje novog Azuriranja cena.

    @param db: Testna DB.
    @return: Entitet 'Azuriranje cena'.
    """
    azuriranje_cena = AzuriranjeCena.objects.create(
        id_azur_cene=1,
        sprat="1.0",
        broj_soba=3,
        orijentisanost="Jug",
        cena_kvadrata=1568.00
    )

    return azuriranje_cena


# endregion



# region NOVI STAN 1 FIXTURE
@pytest.fixture(autouse=False)
def novi_stan_1_fixture_stanovi(db, azuriranje_cena_fixture) -> Stanovi:
    """
    Kreiranje Stana1.

    @param azuriranje_cena_fixture:
    @param kreiraj_auriranje_cena:  pytest.fixture (kreiraj_tri_auriranja_cena_stanovi)
    @param db: Testna DB.
    @return: Entitet 'Stanovi'.
    """

    stan1 = Stanovi.objects.create(
        id_stana=1,
        lamela="L2.1.S10",
        adresa_stana="Adresa Stana L2.1.S10",
        kvadratura=67.49,
        kvadratura_korekcija=65.47,
        iznos_za_korekciju_kvadrature=0.97,
        sprat="1.0",
        broj_soba=3,
        orijentisanost="Jug",
        broj_terasa="0",
        cena_stana="103085.59",
        cena_kvadrata="1574.66",
        napomena='Nema napomene',
        status_prodaje="dostupan"
    )

    return stan1


# endregion


# region NOVI STAN 2 FIXTURE
@pytest.fixture(autouse=False)
def novi_stan_2_fixture_stanovi(db, azuriranje_cena_fixture) -> Stanovi:

    stan2 = Stanovi.objects.create(
        id_stana=2,
        lamela="L3.1.S1",
        adresa_stana="Adresa Stana L3.1.S1",
        kvadratura=50.25,
        kvadratura_korekcija=48.74,
        iznos_za_korekciju_kvadrature=0.97,
        sprat="1.0",
        broj_soba=3,
        orijentisanost="Jug",
        broj_terasa="1",
        cena_stana="76428.24",
        cena_kvadrata="1568.00",
        napomena='Nema napomene',
        status_prodaje="kupljen"
    )

    return stan2


# endregion


# region NOVI STAN 3 FIXTURE
@pytest.fixture(autouse=False)
def novi_stan_3_fixture_stanovi(db, azuriranje_cena_fixture) -> Stanovi:

    stan3 = Stanovi.objects.create(
        id_stana=3,
        lamela="L1.1.S4",
        adresa_stana="Adresa Stana L3.1.S1",
        kvadratura=49.23,
        kvadratura_korekcija=47.75,
        iznos_za_korekciju_kvadrature=0.97,
        sprat="1.0",
        broj_soba=3,
        orijentisanost="Jug",
        broj_terasa="1",
        cena_stana="74128.09",
        cena_kvadrata="1552.32",
        napomena='Nema napomene',
        status_prodaje="rezervisan"
    )

    return stan3


# endregion


# region NOVI KUPAC FIXTURE
@pytest.fixture(autouse=False)
def novi_kupac_fixture_reporti(db) -> Kupci:
    """
    Kreiranje novog Kupca.

    @param db: Testna DB.
    @return: Entitet Kupci.
    """
    kupac = Kupci.objects.create(
        id_kupca=1,
        lice='Fizicko',
        ime_prezime='Mihailo Pupin',
        email='miha@gmail.com',
        broj_telefona='+381631369098',
        Jmbg_Pib=str(random.randrange(1000000000000, 9999999999999)),
        adresa='Milentija Popovica 32',
    )

    return kupac


# endregion


# region NOVE TRI PONUDE FIXTURES
@pytest.fixture(autouse=False)
def nove_tri_ponude_fixture_reporti(db,
                                    novi_kupac_fixture_reporti,
                                    novi_stan_1_fixture_stanovi,
                                    novi_stan_2_fixture_stanovi,
                                    novi_stan_3_fixture_stanovi,
                                    novi_autorizovan_korisnik_fixture_reports,
                                    # novi_agent_prodaje_stanova
                                    ) -> Ponude:

    nove_tri_ponude_fixture = Ponude.objects.bulk_create(
        [
            Ponude(
                id_ponude=1,
                kupac=novi_kupac_fixture_reporti,
                stan=novi_stan_1_fixture_stanovi,
                klijent_prodaje=novi_autorizovan_korisnik_fixture_reports,
                cena_stana_za_kupca=70000,
                napomena=fake.text(max_nb_chars=25),
                broj_ugovora="broj_ugovora-1",
                datum_ugovora=datetime.date(2021, 9, 1),
                status_ponude=Ponude.StatusPonude.POTENCIJALAN,
                nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
                odobrenje=False
            ),
            Ponude(
                id_ponude=2,
                kupac=novi_kupac_fixture_reporti,
                stan=novi_stan_2_fixture_stanovi,
                klijent_prodaje=novi_autorizovan_korisnik_fixture_reports,
                cena_stana_za_kupca=55000,
                napomena=fake.text(max_nb_chars=25),
                broj_ugovora="broj_ugovora-2",
                datum_ugovora=datetime.date(2021, 3, 11),
                status_ponude=Ponude.StatusPonude.KUPLJEN,
                nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
                odobrenje=False
            ),
            Ponude(
                id_ponude=3,
                kupac=novi_kupac_fixture_reporti,
                stan=novi_stan_3_fixture_stanovi,
                klijent_prodaje=novi_autorizovan_korisnik_fixture_reports,
                cena_stana_za_kupca=65000,
                napomena=fake.text(max_nb_chars=25),
                broj_ugovora="broj_ugovora-3",
                datum_ugovora=datetime.date(2022, 1, 10),
                status_ponude=Ponude.StatusPonude.REZERVISAN,
                nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
                odobrenje=False
            )
        ]
    )
    return nove_tri_ponude_fixture


# endregion


@dataclass
class ReportStatistikaStanova:
    ukupno_stanova: int
    rezervisano: int
    dostupan: int
    prodat: int
    procenat_rezervisan: float
    procenat_dostupan: float
    procenat_prodat: float
    prodaja_po_mesecima: json
    broj_ponuda_po_mesecima: json
    ukupna_suma_prodatih_stanova: json


class ReportFactoryStatistikaStanova(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportStatistikaStanova

    ukupno_stanova = factory.Faker("ukupno_stanova")
    rezervisano = factory.Faker("rezervisano")
    dostupan = factory.Faker("dostupan")
    prodat = factory.Faker("prodat")
    procenat_rezervisan = factory.Faker("procenat_rezervisan")
    procenat_dostupan = factory.Faker("procenat_dostupan")
    procenat_prodat = factory.Faker("procenat_prodat")
    prodaja_po_mesecima = factory.Faker("prodaja_po_mesecima")
    broj_ponuda_po_mesecima = factory.Faker("broj_ponuda_po_mesecima")
    ukupna_suma_prodatih_stanova = factory.Faker("ukupna_suma_prodatih_stanova")


# region NOVI JEDAN REPORT FIXTURE
@pytest.fixture(autouse=False)
def novi_izvestaj_stanovi_statistika_fixture():
    """
    Kreiranje novog Report-a.

    @param db: Testna DB.
    @return: Entitet 'Faker'.
    """
    report = ReportStatistikaStanova(3, 1, 1, 0, 33.33, 33.33, 0.0,
                                     # prodaja po mesecima.
                                     [{"jan": 0, "feb": 0, "mart": 1, "apr": 0, "maj": 0, "jun": 0, "jul": 0, "avg": 0,
                                       "sep": 0,
                                       "okt": 0, "nov": 0, "dec": 0}],
                                     # Broj Ponuda po mesecima.
                                     [{"jan": 1, "feb": 0, "mart": 1, "apr": 0, "maj": 0, "jun": 0, "jul": 0, "avg": 0,
                                       "sep": 1,
                                       "okt": 0, "nov": 0, "dec": 0}],
                                     # Ukupna suma prodatih stanova.
                                     [{"jan": 0, "feb": 0, "mart": 55000, "apr": 0, "maj": 0, "jun": 0, "jul": 0,
                                       "avg": 0, "sep": 0,
                                       "okt": 0, "nov": 0, "dec": 0}]
                                     )

    return report


# endregion


# region FIXTURE NEREGISTROVAN KORISNIK REPORTS
@pytest.fixture()
def novi_neautorizovan_korisnik_fixture_reports(db) -> Korisnici:
    return Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )


# endregion


# region FIXTURE REGISTROVAN KORISNIK REPORTS
@pytest.fixture(autouse=False)
def novi_autorizovan_korisnik_fixture_reports(db, client, django_user_model) -> Korisnici:
    """
    Kreiranje novog Korisnika i autorizacija istog na sistem.

    @param db: Testna DB.
    @param client: A Django test client instance.
    @param django_user_model: Korisnik.
    @return: Entitet autorizovan Korisnik.
    """

    korisnik = Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )

    client.force_login(korisnik)

    return korisnik


# endregion


@dataclass
class ReportProdajaPoAgentu:
    id: int
    ime: str
    prezime: str
    email: str
    role: str
    prodati_stanovi_korisnici: int


class ReportFactoryProdajaPoAgentu(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportProdajaPoAgentu

    id = factory.Faker("id")
    ime = factory.Faker("ime")
    prezime = factory.Faker("prezime")
    email = factory.Faker("email")
    role = factory.Faker("role")
    prodati_stanovi_korisnici = factory.Faker("prodati_stanovi_korisnici")


# region NOVI JEDAN REPORT PO AGENTU FIXTURE
@pytest.fixture(autouse=False)
def novi_izvestaj_prodaja_stanova_po_agentu():
    """
    Kreiranje novog Report-a.

    @param db: Testna DB.
    @return: Entitet 'Faker'.
    """
    # test = ([{
    #     "id" : 1,
    #     "ime" : "Nikola",
    #     "prezime" : "Nikola",
    #     "email" : "nikola@nikola.com",
    #     "role" : "Administrator",
    #     "prodati_stanovi_korisnici" : 1,
    # }])

    report = ReportProdajaPoAgentu(1, "Nikola", "Nikola", "nikola@nikola.com", "Administrator", 1)

    return report


# endregion


@dataclass
class ReportProdajaPoKupcu:
    id_kupca: int
    ime_prezime: str
    email: str
    prodati_stanovi_klijenti: int
    rezervisani_stanovi_klijenti: int
    potencijalan_stanovi_klijenti: int

class ReportFactoryProdajaPoKupcu(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportProdajaPoKupcu

    id_kupca = factory.Faker("id_kupca")
    ime_prezime = factory.Faker("ime_prezime")
    email = factory.Faker("email")
    prodati_stanovi_klijenti = factory.Faker("prodati_stanovi_klijenti")
    rezervisani_stanovi_klijenti = factory.Faker("rezervisani_stanovi_klijenti")
    potencijalan_stanovi_klijenti = factory.Faker("potencijalan_stanovi_klijenti")


# region NOVI JEDAN REPORT PO KUPCU FIXTURE
@pytest.fixture(autouse=False)
def novi_izvestaj_prodaja_stanova_po_kupcu():
    """
    Kreiranje novog Report-a.

    @param db: Testna DB.
    @return: Entitet 'Faker'.
    """
    report = ReportProdajaPoKupcu(1, 'Mihailo Pupin', 'miha@gmail.com', 1, 1, 1)

    return report


# endregion


@dataclass
class ReportROI:
    kvadratura_stanova: dict                       # ili json, prvo sredi decimale
    ukupna_cena_stanova_po_lamelama: dict
    ukupan_roi_stanova: dict


class ReportFactoryROI(factory.django.DjangoModelFactory):
    class Meta:
        model = ReportROI

    kvadratura_stanova = factory.Faker("kvadratura_stanova")
    ukupna_cena_stanova_po_lamelama = factory.Faker("ukupna_cena_stanova_po_lamelama")
    ukupan_roi_stanova = factory.Faker("ukupan_roi_stanova")


# region NOVI JEDAN REPORT ROI STANOVA FIXTURE
@pytest.fixture(autouse=False)
def novi_izvestaj_roi_stanova():
    """
    Kreiranje novog Report-a.

    @param db: Testna DB.
    @return: Entitet 'Faker'.
    """
    report = ReportROI({"stanovi_ukupno_kvadrata": 166.97,
                        "stanovi_ukupno_korekcija_kvadrata": 161.96,
                        "razlika_kvadrati_korekcija": 5.01},
                       {"svi_stanovi_po_lameli_l1_1": 74128.09,
                        "svi_stanovi_po_lameli_l2_1": 103085.59,
                        "svi_stanovi_po_lameli_l3_1": 76428.24,
                        "svi_stanovi_po_lameli_l1_2": 0,
                        "svi_stanovi_po_lameli_l2_2": 0,
                        "svi_stanovi_po_lameli_l3_2": 0,
                        "svi_stanovi_po_lameli_l1_3": 0,
                        "svi_stanovi_po_lameli_l2_3": 0,
                        "svi_stanovi_po_lameli_l3_3": 0,
                        "svi_stanovi_po_lameli_l1_4": 0,
                        "svi_stanovi_po_lameli_l2_4": 0,
                        "svi_stanovi_po_lameli_l3_4": 0,
                        "svi_stanovi_po_lameli_l1_5": 0,
                        "svi_stanovi_po_lameli_l2_5": 0,
                        "svi_stanovi_po_lameli_l3_5": 0,
                        "svi_stanovi_po_lameli_l1_6": 0,
                        "svi_stanovi_po_lameli_l2_6": 0,
                        "svi_stanovi_po_lameli_l3_6": 0,
                        "svi_stanovi_po_lameli_l1_7": 0,
                        "svi_stanovi_po_lameli_l2_7": 0,
                        "svi_stanovi_po_lameli_l3_7": 0,
                        "svi_stanovi_po_lameli_l1_ps": 0,
                        "svi_stanovi_po_lameli_l2_ps": 0,
                        "svi_stanovi_po_lameli_l3_ps": 0},
                       {"suma_cena_stanova_lamela_l1": 74128.09,
                        "suma_cena_stanova_lamela_l2": 103085.59,
                        "suma_cena_stanova_lamela_l3": 76428.24,
                        "ukupna_suma_cena_stanova": 253641.92,
                        "prosecna_cena_kvadrata": 1519.09})

    return report


# endregion
