import pytest
import json
from real_estate_api.korisnici.models import Korisnici
from real_estate_api.garaze.models import Garaze


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

# region NOVA JEDNA GARAZA FIXTURE
@pytest.fixture(autouse=False)
def nova_jedna_garaza_fixture(db) -> Garaze:
    """
    Kreiranje nove Garaze.

    @param db: Testna DB.
    @return: Entitet 'Garaze'.
    """

    garaza = Garaze.objects.create(
        id_garaze=1,
        jedinstveni_broj_garaze=1,
        cena_garaze=8000.0,
        napomena_garaze='Nema napomene',
        status_prodaje_garaze='dostupna'
    )

    return garaza

# endregion

# region NOVE DVE GARAZE FIXTURE
@pytest.fixture(autouse=False)
def nove_dve_garaze_fixture(db) -> Garaze:
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
                cena_garaze=8000.0,
                napomena_garaze='Nema napomene',
                status_prodaje_garaze='dostupna',
            ),
            Garaze(
                id_garaze=2,
                jedinstveni_broj_garaze=2,
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
def nova_jedna_garaza_json_fixture():
    return json.dumps(
        {
            "id_garaze": 1,
            "jedinstveni_broj_garaze": 1,
            "cena_garaze": 5000.0,
            "napomena_garaze": 'Najbolja garaza',
            "status_prodaje_garaze": 'dostupna'
        }
    )

# endregion

# region FIXTURE JSON DUMP JEDNA NEVALIDNA GARAZA
@pytest.fixture(autouse=False)
def nova_jedna_nevalidna_garaza_json_fixture():
    return json.dumps(
        {
            "id_garaze": 1,
            "jedinstveni_broj_garaze": -2,
            "cena_garaze": 8000.0,
            "napomena_garaze": 'Nema napomene',
            "status_prodaje_garaze": 'dostupna'
        }
    )

# endregion

# region FIXTURE JSON DUMP DVE GARAZE UNIQUIE JEDINSTVENI BROJ GARAZE ERROR
@pytest.fixture(autouse=False)
def nove_dve_garaze_sa_istim_jedinstvenim_brojem_garaze_json_fixture():
    return json.dumps(
        [
            {
                "id_garaze": 1,
                "jedinstveni_broj_garaze": 1,
                "cena_garaze": 8000.0,
                "napomena_garaze": 'Nema napomene',
                "status_prodaje_garaze": 'dostupna',
            },
            {
                "id_garaze": 2,
                "jedinstveni_broj_garaze": 1,
                "cena_garaze": 8000.0,
                "napomena_garaze": 'Nema napomene',
                "status_prodaje_garaze": 'dostupna'
            }
        ]
    )

# endregion
