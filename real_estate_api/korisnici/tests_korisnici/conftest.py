import json

import pytest
from faker import Faker

from real_estate_api.korisnici.models import Korisnici

fake = Faker()


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

# region FIXTURE REGISTROVANA JEDAN KORISNIKA FULL
@pytest.fixture(autouse=False)
def novi_jedan_korisnik_fixture(db, client, django_user_model, novi_jedan_auth_korisnik_fixture) -> Korisnici:
    """
    Kreiranje novog jednog Korisnika bez autorizacija istog na sistem.
        * Test-Ime-Korisnika je sa rolom PRODAVAC.
    @param novi_jedan_auth_korisnik_fixture: Autorizovan Korisnik (super user).
    @param db: Testna DB.
    @param client: A Django test client instance.
    @param django_user_model: Korisnik.
    @return: Entitet autorizovan tri Korisnika.
    """

    korisnik = Korisnici.objects.create(
        id=1,
        email=fake.email(),
        username=fake.user_name(),
        password='testpswd',
        ime='Test-Ime-Korisnika',
        prezime='Test-Prezime-Korisnika',
        role=Korisnici.PrivilegijeKorisnika.PRODAVAC,
        about=fake.text(max_nb_chars=25),
        is_staff=True,
        is_active=True,
        is_superuser=False,
    )

    return korisnik


# endregion

# region FIXTURE REGISTROVANA TRI KORISNIKA FULL
@pytest.fixture(autouse=False)
def nova_tri_korisnika_fixture(db, client, django_user_model, novi_jedan_auth_korisnik_fixture) -> Korisnici:
    """
    Kreiranje nova tri Korisnika i autorizacija istih na sistem.
    Ovi korisnici predstavljaju testne Korisnike sa popunjenim svim poljima.
        * Dejan je sa rolom ADMINISTRATOR.
        * Slobodan je sa rolom FINANSIJE.
        * Ivana je sa rolom PRODAVAC.

    @param novi_jedan_auth_korisnik_fixture: Autorizovan Korisnik (super user).
    @param db: Testna DB.
    @param client: A Django test client instance.
    @param django_user_model: Korisnik.
    @return: Entitet autorizovan tri Korisnika.
    """

    korisnici = Korisnici.objects.bulk_create(
        [
            Korisnici(
                id=1,
                email=fake.email(),
                username=fake.user_name(),
                password='dejan',
                ime='Dejan',
                prezime='Cugalj',
                role=Korisnici.PrivilegijeKorisnika.ADMINISTRATOR,
                about=fake.text(max_nb_chars=25),
                is_staff=True,
                is_active=True,
                is_superuser=False,
            ),
            Korisnici(
                id=2,
                email=fake.email(),
                username=fake.user_name(),
                password='sloba',
                ime='Slobodan',
                prezime='Tomic',
                role=Korisnici.PrivilegijeKorisnika.FINANSIJE,
                about=fake.text(max_nb_chars=25),
                is_staff=True,
                is_active=True,
                is_superuser=False,
            ),
            Korisnici(
                id=3,
                email=fake.email(),
                username=fake.user_name(),
                password='ivana',
                ime='Ivana',
                prezime='Tepavac',
                role=Korisnici.PrivilegijeKorisnika.PRODAVAC,
                about=fake.text(max_nb_chars=25),
                is_staff=True,
                is_active=True,
                is_superuser=False,
            )
        ]
    )

    return korisnici


# endregion

# region FIXTURE JSON DUMP JEDAN KORISNIK
@pytest.fixture(autouse=False)
def novi_jedan_korisnik_json_fixture():
    return json.dumps(
        {
            "id": 5,
            "email": fake.email(),
            "username": fake.user_name(),
            "password": "testStrongPSWD",
            "ime": fake.name(),
            "prezime": fake.last_name(),
            "role": Korisnici.PrivilegijeKorisnika.PRODAVAC,
            "about": fake.text(max_nb_chars=25),
            "is_staff": True,
            "is_active": True,
            "is_superuser": False,
        }
    )


# endregion

# region FIXTURE JSON DUMP TRI KORISNIKA
@pytest.fixture(autouse=False)
def nova_tri_korisnika_json_fixture():
    return json.dumps(
        [
            {
                "id": 5,
                "email": fake.email(),
                "username": fake.user_name(),
                "password": "testStrongPSWD",
                "ime": fake.name(),
                "prezime": fake.last_name(),
                "role": Korisnici.PrivilegijeKorisnika.PRODAVAC,
                "about": fake.text(max_nb_chars=25),
                "is_staff": True,
                "is_active": True,
                "is_superuser": False,
            },
            {
                "id": 6,
                "email": fake.email(),
                "username": fake.user_name(),
                "password": "testStrongPSWD-2",
                "ime": fake.name(),
                "prezime": fake.last_name(),
                "role": Korisnici.PrivilegijeKorisnika.FINANSIJE,
                "about": fake.text(max_nb_chars=25),
                "is_staff": True,
                "is_active": True,
                "is_superuser": False,
            },
            {
                "id": 7,
                "email": fake.email(),
                "username": fake.user_name(),
                "password": "testStrongPSWD-3",
                "ime": fake.name(),
                "prezime": fake.last_name(),
                "role": Korisnici.PrivilegijeKorisnika.FINANSIJE,
                "about": fake.text(max_nb_chars=25),
                "is_staff": True,
                "is_active": True,
                "is_superuser": False,
            }
        ]
    )
# endregion
