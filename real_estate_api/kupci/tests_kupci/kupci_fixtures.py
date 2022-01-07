import pytest

from real_estate_api.kupci.models import Kupci
from faker import Faker

fake = Faker()


@pytest.fixture(autouse=True)
def novi_kupac_fixture(db) -> Kupci:
    return Kupci.objects.create(
        lice='Fizicko',
        ime_prezime=fake.name(),
        email=fake.email(),
        broj_telefona='+381631369098',
        Jmbg_Pib=fake.random_int(0, 13),
        adresa='Milentija Popovica 32',
    )
