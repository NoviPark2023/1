import datetime
import json
import random

import pytest
from faker import Faker

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci
from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi, AzuriranjeCena

fake = Faker()


# region KORISNICI FIXTURE
# ##################################
# ##### KORISNICI FIXTURE ##########
# ##################################

# region FIXTURE NE REGISTROVAN KORISNIK
@pytest.fixture()
def novi_korisnik_ne_autorizovan_fixture_ponude(db) -> Korisnici:
    return Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )


# endregion

# region FIXTURE REGISTROVAN JEDAN KORISNIK SUPERUSER  FULL
@pytest.fixture(autouse=False)
def novi_jedan_auth_korisnik_fixture_ponude(db, client, django_user_model) -> Korisnici:
    """
    Kreiranje novog Korisnika i autorizacija istog na sistem.
    Ovaj korisnik predstavlja testnog Korisnika sa popunjenim svim poljima.
        * Ovaj Korisnik je SUPER USER.

    @param db: Testna DB.
    @param client: A Django test client instance.
    @param django_user_model: Korisnik.
    @return: Entitet autorizovan (super user) Korisnik.
    """

    korisnik = Korisnici.objects.create(
        email=fake.email(),
        username=fake.user_name(),
        password='nikola',
        ime='Nikola',
        prezime='Nikola',
        role=Korisnici.PrivilegijeKorisnika.ADMINISTRATOR,
        about=fake.text(max_nb_chars=25),
        is_staff=True,
        is_active=True,
        is_superuser=True,
    )

    client.force_login(korisnik)

    return korisnik


# endregion

# ##################################
# ########## END KORISNICI #########
# ##################################
# endregion

# region STANOVI FIXTURE POTREBNO ZA PONUDU
# ###########################################
# ### STANOVI FIXTURE POTREBNO ZA PONUDU ####
# ###########################################

# region AZURIRANJE CENA Stanova
@pytest.fixture(autouse=False)
def kreiraj_auriranje_cena_ponude(db) -> list[AzuriranjeCena]:
    """
    Separaciona tabela 'Azuriranje Cena Stanova' koja se koristi za Automatsko
    racunanje cene stanova na osnovu zadatih parametara.

    @param db: Testna DB
    @return: AzuriranjeCena obj.
    """
    azuriranje_cena = AzuriranjeCena.objects.bulk_create(
        [
            AzuriranjeCena(
                id_azur_cene=1,
                sprat="1.0",
                broj_soba=2,
                orijentisanost="Jug",
                cena_kvadrata=1568.00
            ),
            AzuriranjeCena(
                id_azur_cene=2,
                sprat="1.0",
                broj_soba=3,
                orijentisanost="Jug",
                cena_kvadrata=1574.66
            ),
            AzuriranjeCena(
                id_azur_cene=3,
                sprat="1.0",
                broj_soba=3,
                orijentisanost="Jug",
                cena_kvadrata=1568.00
            ),
        ]
    )

    return azuriranje_cena


# endregion

# region NOVI JEDAN STAN FIXTURE (status: "DOSTUPAN")
@pytest.fixture(autouse=False)
def novi_jedan_stan_fixture_ponude_status_dostupan(db, kreiraj_auriranje_cena_ponude) -> Stanovi:
    stan_dostupan = Stanovi.objects.create(
        # id_stana=1,
        lamela="FROM-TEST-L3.1.S1",
        adresa_stana="Adresa Stana L3.1.S2",
        kvadratura=48.02,
        kvadratura_korekcija=46.58,
        iznos_za_korekciju_kvadrature=0.97,
        sprat="1.0",
        broj_soba=2,
        orijentisanost="Jug",
        broj_terasa="0",
        cena_stana="73.036,499",
        cena_kvadrata="1568.00",
        napomena='Nema napomene',
        status_prodaje=Stanovi.StatusProdaje.DOSTUPAN,
    )

    return stan_dostupan


# region NOVI JEDAN STAN FIXTURE (status: "REZERVISAN")
@pytest.fixture(autouse=False)
def novi_jedan_stan_fixture_ponude_status_rezervisan(db, kreiraj_auriranje_cena_ponude) -> Stanovi:
    stan_rezervisan = Stanovi.objects.create(
        # id_stana=1,
        lamela="FROM-TEST-L3.1.S2",
        adresa_stana="Adresa Stana L3.1.S2",
        kvadratura=48.02,
        kvadratura_korekcija=46.58,
        iznos_za_korekciju_kvadrature=0.97,
        sprat="1.0",
        broj_soba=2,
        orijentisanost="Jug",
        broj_terasa="0",
        cena_stana="73.036,499",
        cena_kvadrata="1568.00",
        napomena='Nema napomene',
        status_prodaje=Stanovi.StatusProdaje.REZERVISAN,
    )

    return stan_rezervisan


# region NOVI JEDAN STAN FIXTURE (status: "PRODAT")
@pytest.fixture(autouse=False)
def novi_jedan_stan_fixture_ponude_status_prodat(db, kreiraj_auriranje_cena_ponude) -> Stanovi:
    stan_rezervisan = Stanovi.objects.create(
        # id_stana=1,
        lamela="FROM-TEST-L3.1.S3",
        adresa_stana="Adresa Stana L3.1.S2",
        kvadratura=48.02,
        kvadratura_korekcija=46.58,
        iznos_za_korekciju_kvadrature=0.97,
        sprat="1.0",
        broj_soba=2,
        orijentisanost="Jug",
        broj_terasa="0",
        cena_stana="73.036,499",
        cena_kvadrata="1568.00",
        napomena='Nema napomene',
        status_prodaje=Stanovi.StatusProdaje.PRODAT,
    )

    return stan_rezervisan


# endregion
# endregion

# ##################################
# #### END STANOVI FIXTURE #########
# ##################################
# endregion

# region KUPCI FIXTURE
# ##################################
# ######## KUPCI FIXTURE ##########
# ##################################

# region NOVI JEDAN KUPAC FIXTURE
@pytest.fixture(autouse=False)
def novi_kupac_fixture_ponude(db) -> Kupci:
    """
    Kreiranje novog Kupca.

    @param db: Testna DB.
    @return: Entitet Kupci.
    """
    kupac = Kupci.objects.create(
        id_kupca=1,
        lice='Fizicko',
        ime_prezime=fake.name(),
        email=fake.email(),
        broj_telefona='+381631369098',
        Jmbg_Pib=str(random.randrange(1000000000000, 9999999999999)),
        adresa='Milentija Popovica 32',
    )

    return kupac


# endregion

# ##################################
# ###### END KUPCI FIXTURE #########
# ##################################
# endregion

# region PONUDE FIXTURE
# ##################################
# ######## PONUDE FIXTURE ##########
# ##################################

# region JEDNA PONUDA FIXTURES (STATUS POTENCIJALAN)
@pytest.fixture()
def nova_jedna_ponuda_fixture(db,
                              novi_kupac_fixture_ponude,
                              novi_jedan_stan_fixture_ponude_status_dostupan,
                              novi_jedan_auth_korisnik_fixture_ponude) -> Ponude:
    nova_jedna_ponuda_fixture = Ponude.objects.create(
        # id_ponude=1,
        kupac=novi_kupac_fixture_ponude,
        stan=novi_jedan_stan_fixture_ponude_status_dostupan,
        klijent_prodaje=novi_jedan_auth_korisnik_fixture_ponude,
        cena_stana_za_kupca=0,
        napomena=fake.text(max_nb_chars=25),
        broj_ugovora="broj_ugovora",
        datum_ugovora=datetime.date(2021, 9, 1),
        status_ponude=Ponude.StatusPonude.POTENCIJALAN,
        nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
        odobrenje=False
    )

    return nova_jedna_ponuda_fixture


# endregion

# region JEDNA PONUDA FIXTURES (STATUS REZERVISAN)
@pytest.fixture()
def nova_jedna_ponuda_fixture_status_rezervisan(db,
                                                novi_kupac_fixture_ponude,
                                                novi_jedan_stan_fixture_ponude_status_rezervisan,
                                                novi_jedan_auth_korisnik_fixture_ponude) -> Ponude:
    nova_jedna_ponuda_fixture_status_rezervisan = Ponude.objects.create(
        kupac=novi_kupac_fixture_ponude,
        stan=novi_jedan_stan_fixture_ponude_status_rezervisan,
        klijent_prodaje=novi_jedan_auth_korisnik_fixture_ponude,
        cena_stana_za_kupca=0,
        napomena="nema napomene",
        broj_ugovora="broj_ugovora",
        datum_ugovora=datetime.date(2021, 9, 1),
        status_ponude=Ponude.StatusPonude.REZERVISAN,
        nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
        odobrenje=True
    )

    return nova_jedna_ponuda_fixture_status_rezervisan


# endregion

# region JEDNA PONUDA FIXTURES (STATUS POTENCIJALAN)
@pytest.fixture()
def nova_jedna_ponuda_fixture_status_kupljen(db,
                                             novi_kupac_fixture_ponude,
                                             novi_jedan_stan_fixture_ponude_status_dostupan,
                                             novi_jedan_auth_korisnik_fixture_ponude) -> Ponude:
    nova_jedna_ponuda_fixture = Ponude.objects.create(
        kupac=novi_kupac_fixture_ponude,
        stan=novi_jedan_stan_fixture_ponude_status_dostupan,
        klijent_prodaje=novi_jedan_auth_korisnik_fixture_ponude,
        cena_stana_za_kupca=0,
        napomena=fake.text(max_nb_chars=25),
        broj_ugovora="broj_ugovora",
        datum_ugovora=datetime.date(2021, 9, 1),
        status_ponude=Ponude.StatusPonude.KUPLJEN,
        nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
        odobrenje=True
    )

    return nova_jedna_ponuda_fixture


# endregion

# region JEDNA PONUDA BEZ UGOVORA FIXTURES
@pytest.fixture()
def nova_jedna_ponuda_bez_ugovora_fixture(db,
                                          novi_kupac_fixture_ponude,
                                          novi_jedan_stan_fixture_ponude_status_dostupan,
                                          novi_jedan_auth_korisnik_fixture_ponude) -> Ponude:
    nova_jedna_ponuda_fixture = Ponude.objects.create(
        # id_ponude=1,
        kupac=novi_kupac_fixture_ponude,
        stan=novi_jedan_stan_fixture_ponude_status_dostupan,
        klijent_prodaje=novi_jedan_auth_korisnik_fixture_ponude,
        cena_stana_za_kupca=0,
        napomena=fake.text(max_nb_chars=25),
        broj_ugovora="null",
        datum_ugovora=datetime.date(2021, 9, 1),
        status_ponude=Ponude.StatusPonude.POTENCIJALAN,
        nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
        odobrenje=False
    )

    return nova_jedna_ponuda_fixture


# endregion

# region JEDNA PONUDA FIXTURES (401)
@pytest.fixture()
def nova_jedna_ponuda_fixture_401(db,
                                  novi_kupac_fixture_ponude,
                                  novi_jedan_stan_fixture_ponude_status_dostupan,
                                  novi_korisnik_ne_autorizovan_fixture_ponude) -> Ponude:
    nova_jedna_ponuda_fixture_401 = Ponude.objects.create(
        # id_ponude=1,
        kupac=novi_kupac_fixture_ponude,
        stan=novi_jedan_stan_fixture_ponude_status_dostupan,
        klijent_prodaje=novi_korisnik_ne_autorizovan_fixture_ponude,
        cena_stana_za_kupca=70000,
        napomena=fake.text(max_nb_chars=25),
        broj_ugovora="broj_ugovora-1",
        datum_ugovora=datetime.date(2021, 9, 1),
        status_ponude=Ponude.StatusPonude.POTENCIJALAN,
        nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
        odobrenje=False
    )

    return nova_jedna_ponuda_fixture_401


# endregion

# region TRI PONUDE FIXTURES
@pytest.fixture()
def nove_tri_ponude_fixture(db,
                            novi_kupac_fixture_ponude,
                            novi_jedan_stan_fixture_ponude_status_dostupan,
                            novi_jedan_auth_korisnik_fixture_ponude) -> Ponude:
    nova_jedna_ponuda_fixture = Ponude.objects.bulk_create(
        [
            Ponude(
                kupac=novi_kupac_fixture_ponude,
                stan=novi_jedan_stan_fixture_ponude_status_dostupan,
                klijent_prodaje=novi_jedan_auth_korisnik_fixture_ponude,
                cena_stana_za_kupca=70000,
                napomena=fake.text(max_nb_chars=25),
                broj_ugovora="broj_ugovora-1",
                datum_ugovora=datetime.date(2021, 9, 1),
                status_ponude=Ponude.StatusPonude.POTENCIJALAN,
                nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
            ),
            Ponude(
                kupac=novi_kupac_fixture_ponude,
                stan=novi_jedan_stan_fixture_ponude_status_dostupan,
                klijent_prodaje=novi_jedan_auth_korisnik_fixture_ponude,
                cena_stana_za_kupca=55000,
                napomena=fake.text(max_nb_chars=25),
                broj_ugovora="broj_ugovora-2",
                datum_ugovora=datetime.date(2021, 10, 11),
                status_ponude=Ponude.StatusPonude.REZERVISAN,
                nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
            ),
            Ponude(
                kupac=novi_kupac_fixture_ponude,
                stan=novi_jedan_stan_fixture_ponude_status_dostupan,
                klijent_prodaje=novi_jedan_auth_korisnik_fixture_ponude,
                cena_stana_za_kupca=65000,
                napomena=fake.text(max_nb_chars=25),
                broj_ugovora="broj_ugovora-3",
                datum_ugovora=datetime.date(2022, 1, 10),
                status_ponude=Ponude.StatusPonude.KUPLJEN,
                nacin_placanja=Ponude.NacinPlacanja.U_CELOSTI,
            )
        ]
    )
    return nova_jedna_ponuda_fixture


# endregion


# region JEDNA PONUDA JSON DUMP FIXTURES(STATUS POTENCIJALAN)
@pytest.fixture()
def nova_jedna_ponuda_json_fixture_status_potencijalan(novi_kupac_fixture_ponude,
                                                       novi_jedan_stan_fixture_ponude_status_dostupan,
                                                       novi_jedan_auth_korisnik_fixture_ponude
                                                       ):
    return json.dumps(
        {
            "id_ponude": 2,
            "kupac": novi_kupac_fixture_ponude.id_kupca,
            "stan": novi_jedan_stan_fixture_ponude_status_dostupan.id_stana,
            "cena_stana_za_kupca": 1000,
            "napomena": "Nema Napomene",
            "broj_ugovora": "BR.1",
            "datum_ugovora": "17.11.2022",
            "status_ponude": Ponude.StatusPonude.POTENCIJALAN,
            "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
            "odobrenje": False,
            "klijent_prodaje": novi_jedan_auth_korisnik_fixture_ponude.id
        }
    )


# endregion

# region JEDNA PONUDA JSON DUMP FIXTURES STATUS(REZERVEISAN)
@pytest.fixture()
def nova_jedna_ponuda_json_fixture_status_rezervisan(novi_kupac_fixture_ponude,
                                                     novi_jedan_stan_fixture_ponude_status_rezervisan,
                                                     novi_jedan_auth_korisnik_fixture_ponude
                                                     ):
    return json.dumps(
        {
            "id_ponude": 3,
            "kupac": novi_kupac_fixture_ponude.id_kupca + 1,
            "stan": novi_jedan_stan_fixture_ponude_status_rezervisan.id_stana,
            "cena_stana_za_kupca": 1000,
            "napomena": "Nema Napomene",
            "broj_ugovora": "BR.1",
            "datum_ugovora": "17.11.2022",
            "status_ponude": Ponude.StatusPonude.REZERVISAN,
            "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
            "odobrenje": False,
            "klijent_prodaje": novi_jedan_auth_korisnik_fixture_ponude.id
        }
    )


# endregion

# region JEDNA PONUDA JSON DUMP FIXTURES STATUS(KUPLJEN)
@pytest.fixture()
def nova_jedna_ponuda_json_fixture_status_prodat(novi_kupac_fixture_ponude,
                                                 novi_jedan_stan_fixture_ponude_status_prodat,
                                                 novi_jedan_auth_korisnik_fixture_ponude
                                                 ):
    return json.dumps(
        {
            "id_ponude": 3,
            "kupac": novi_kupac_fixture_ponude.id_kupca + 2,
            "stan": novi_jedan_stan_fixture_ponude_status_prodat.id_stana,
            "cena_stana_za_kupca": 1000,
            "napomena": "Nema Napomene",
            "broj_ugovora": "BR.1",
            "datum_ugovora": "17.11.2022",
            "status_ponude": Ponude.StatusPonude.KUPLJEN,
            "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
            "odobrenje": False,
            "klijent_prodaje": novi_jedan_auth_korisnik_fixture_ponude.id
        }
    )
# endregion

# ##################################
# #### END PONUDE FIXTURE #########
# ##################################
# endregion
