import pytest
import random
from faker import Faker

from real_estate_api.korisnici.models import Korisnici
from real_estate_api.kupci.models import Kupci

fake = Faker()


@pytest.fixture()
def novi_korisnik_ne_autorizovan_fixture(db) -> Korisnici:
    return Korisnici.objects.create(
        username='nikola',
        password='nikola',
        email='nikola@nikola.com',
        ime='Nikola',
        prezime='Nikola',
    )


@pytest.fixture(autouse=False)
def novi_autorizovan_korisnik_fixture(db, client, django_user_model) -> Korisnici:
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


@pytest.fixture(autouse=False)
def nova_dva_kupaca_fixture(db) -> list:
    """
    Kreiranje dva nova Kupca za test serijalizersa.

    @param db: Testna DB.
    @return: Entitet Kupci.
    """

    kupac_jedan = Kupci.objects.create(
        id_kupca=1,
        lice='Fizicko',
        ime_prezime=fake.name(),
        email=fake.email(),
        broj_telefona='+381631369098',
        Jmbg_Pib=random.randrange(1000000000000, 9999999999999),  # Random 13 digits number.
        adresa='Milentija Popovica 32',
    )
    kupac_dva = Kupci.objects.create(
        id_kupca=2,
        lice='Pravno',
        ime_prezime=fake.name(),
        email=fake.email(),
        broj_telefona='+381 333 999',
        Jmbg_Pib=random.randrange(1000000000000, 9999999999999),  # Random 13 digits number.
        adresa='Milke Canic 32',
    )
    novi_kupci = [kupac_jedan, kupac_dva]

    return novi_kupci
