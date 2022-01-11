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
def novi_korisnik_ne_autorizovan_fixture(db) -> Korisnici:
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
def novi_jedan_auth_korisnik_fixture(db, client, django_user_model) -> Korisnici:
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
def kreiraj_auriranje_cena(db) -> list[AzuriranjeCena]:
    """
    Separaciona tabela 'Azuriranje Cena Stanova' koja se koristi za Automatsko
    racunanje cene stanova na osnovu zadatih parametara.

    @param db: Testna DB
    @return: AzuriranjeCena obj.
    """
    azuriranje_cena = AzuriranjeCena.objects.bulk_create(
        [
            AzuriranjeCena(id_azur_cene=1,
                           sprat="1.0",
                           broj_soba=2,
                           orijentisanost="Jug",
                           cena_kvadrata=1568.00
                           ),
            AzuriranjeCena(id_azur_cene=2,
                           sprat="1.0",
                           broj_soba=3,
                           orijentisanost="Jug",
                           cena_kvadrata=1574.66
                           ),
            AzuriranjeCena(id_azur_cene=3,
                           sprat="1.0",
                           broj_soba=3,
                           orijentisanost="Jug",
                           cena_kvadrata=1568.00
                           ),
        ]
    )

    return azuriranje_cena


# endregion

# region NOVI JEDAN STAN FIXTURE
@pytest.fixture(autouse=False)
def novi_jedan_stan_fixture(db, kreiraj_auriranje_cena) -> Stanovi:
    """
    Kreiranje novog Stana.

    @param kreiraj_auriranje_cena:  pytest.fixture (kreiraj_auriranje_cena)
    @param db: Testna DB.
    @return: Entitet 'Stanovi'.
    """
    print("\n")
    stan = Stanovi.objects.create(
        id_stana=1,
        lamela="L3.1.S2",
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
        status_prodaje="dostupan",
    )

    return stan


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
def novi_kupac_fixture(db) -> Kupci:
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

# region JEDNA PONUDA JSON DUMP FIXTURES
@pytest.fixture()
def nova_jedna_ponuda(db,
                      novi_kupac_fixture,
                      novi_jedan_stan_fixture,
                      novi_jedan_auth_korisnik_fixture) -> Ponude:
    nova_jedna_ponuda_fixture = Ponude.objects.create(
        id_ponude=1,
        kupac=novi_kupac_fixture,
        stan=novi_jedan_stan_fixture,
        klijent_prodaje=novi_jedan_auth_korisnik_fixture,
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


# region JEDNA PONUDA JSON DUMP FIXTURES
@pytest.fixture()
def nova_jedna_ponuda_json_fixture(novi_kupac_fixture, novi_jedan_stan_fixture):
    return json.dumps(
        {
            "id_ponude": 1,
            "kupac": novi_kupac_fixture.id_kupca,
            "ime_kupca": novi_kupac_fixture.ime_prezime,
            "stan": novi_jedan_stan_fixture.id_stana,
            "adresa_stana": novi_jedan_stan_fixture.adresa_stana,
            "lamela_stana": novi_jedan_stan_fixture.lamela,
            "cena_stana": 77320.28,
            "cena_stana_za_kupca": 70000,
            "napomena": "nema napomene",
            "broj_ugovora": "123",
            "datum_ugovora": "21.12.2021",
            "status_ponude": "rezervisan",
            "nacin_placanja": "kredit",
            "odobrenje": True,
            "klijent_prodaje": 1,
            "detalji_ponude_url": "/ponude/detalji-ponude/1/",
            "izmeni_ponudu_url": "/ponude/izmeni-ponudu/1/",
            "obrisi_ponudu_url": "/ponude/obrisi-ponudu/1/",
            "kreiraj_ponudu_url": "/ponude/kreiraj-ponudu/",
            "lista_ponuda_url": "/ponude/"
        }
    )

# endregion


# ##################################
# #### END PONUDE FIXTURE #########
# ##################################
# endregion
