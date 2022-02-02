import pytest
import json
import random
from real_estate_api.korisnici.models import Korisnici
from real_estate_api.garaze.models import Garaze
from real_estate_api.kupci.models import Kupci


# region FIXTURE NE REGISTROVAN KORISNIK GARAZE
@pytest.fixture()
def novi_korisnik_neautorizovan_fixture_garaze(db) -> Korisnici:
    return Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )


# endregion

# region FIXTURE REGISTROVAN KORISNIK GARAZE
@pytest.fixture(autouse=False)
def novi_autorizovan_korisnik_fixture_garaze(db, client, django_user_model) -> Korisnici:
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

# region NOVI JEDAN KUPAC FIXTURE
@pytest.fixture(autouse=False)
def novi_kupac_fixture_garaze(db) -> Kupci:
    """
    Kreiranje novog Kupca.

    @param db: Testna DB.
    @return: Entitet Kupci.
    """
    kupac = Kupci.objects.create(
        id_kupca=1,
        lice='Fizicko',
        ime_prezime='Mihajlo Pupin',
        email='miha@gmail.com',
        broj_telefona='+381631369098',
        Jmbg_Pib=str(random.randrange(1000000000000, 9999999999999)),
        adresa='Milentija Popovica 32',
    )

    return kupac


# endregion

# region NOVA JEDNA GARAZA FIXTURE
@pytest.fixture(autouse=False)
def nova_jedna_garaza_fixture(db) -> Garaze:
    """
    Kreiranje nove Garaze.

    @param db: Testna DB.
    @param novi_kupac_fixture: Kupac Fixture

    @return: Entitet 'Garaze'.
    """

    kupac_fix = Kupci.objects.create(
        id_kupca=1,
        lice='Fizicko',
        ime_prezime='Mihajlo Pupin',
        email='miha@gmail.com',
        broj_telefona='+381631369098',
        Jmbg_Pib=str(random.randrange(1000000000000, 9999999999999)),
        adresa='Milentija Popovica 32',
    )

    garaza = Garaze.objects.create(
        id_garaze=1,
        jedinstveni_broj_garaze=234,
        cena_garaze=8000.0,
        napomena_garaze='Nema napomene',
        status_prodaje_garaze='dostupna',
        kupac=kupac_fix,

    )

    return garaza


# endregion

# region NOVE DVE GARAZE FIXTURE
@pytest.fixture(autouse=False)
def nove_dve_garaze_fixture(db, novi_kupac_fixture_garaze) -> Garaze:
    """
    Kreiranje dve nove Garaze.

    @param db: Testna DB.
    @return: Entitet 'Garaze'.
    """

    garaza = Garaze.objects.bulk_create(
        [
            Garaze(
                id_garaze=1,
                jedinstveni_broj_garaze=1,
                kupac=novi_kupac_fixture_garaze,
                # ime_kupca=novi_kupac_fixture.ime_prezime,
                cena_garaze=8000.0,
                napomena_garaze='Nema napomene',
                status_prodaje_garaze='dostupna',
            ),
            Garaze(
                id_garaze=2,
                jedinstveni_broj_garaze=2,
                kupac=novi_kupac_fixture_garaze,
                # ime_kupca=novi_kupac_fixture.ime_prezime,
                cena_garaze=7000.0,
                napomena_garaze='Nema napomene',
                status_prodaje_garaze='dostupna'
            )
        ]
    )

    return garaza


# endregion

# region FIXTURE JSON DUMP JEDNA GARAZA
@pytest.fixture(autouse=False)
def nova_jedna_garaza_json_fixture(novi_kupac_fixture_garaze):
    return json.dumps(
        {
            "id_garaze": 1,
            "jedinstveni_broj_garaze": 1,
            "cena_garaze": 5000.0,
            "napomena_garaze": 'Najbolja garaza',
            "status_prodaje_garaze": 'dostupna',
            "kupac": novi_kupac_fixture_garaze.id_kupca,
        }
    )


# endregion

# region FIXTURE JSON DUMP JEDNA NEVALIDNA GARAZA
@pytest.fixture(autouse=False)
def nova_jedna_nevalidna_garaza_json_fixture(novi_kupac_fixture_garaze):
    return json.dumps(
        {
            "id_garaze": 1,
            "jedinstveni_broj_garaze": -2,
            "kupac": 1,
            "ime_kupca": 'Mihajlo Pupin',
            "cena_garaze": 8000.0,
            "napomena_garaze": 'Nema napomene',
            "status_prodaje_garaze": 'dostupna'
        }
    )


# endregion

# region FIXTURE JSON DUMP DVE GARAZE UNIQUIE JEDINSTVENI BROJ GARAZE ERROR
@pytest.fixture(autouse=False)
def nove_dve_garaze_sa_istim_jedinstvenim_brojem_garaze_json_fixture(novi_kupac_fixture_garaze):
    return json.dumps(
        [
            {
                "id_garaze": 1,
                "jedinstveni_broj_garaze": 1,
                "kupac": 1,
                "ime_kupca": 'Mihajlo Pupin',
                "cena_garaze": 8000.0,
                "napomena_garaze": 'Nema napomene',
                "status_prodaje_garaze": 'dostupna',
            },
            {
                "id_garaze": 2,
                "jedinstveni_broj_garaze": 1,
                "kupac": 1,
                "ime_kupca": 'Mihajlo Pupin',
                "cena_garaze": 8000.0,
                "napomena_garaze": 'Nema napomene',
                "status_prodaje_garaze": 'dostupna'
            }
        ]
    )

# endregion
