import factory
from faker import Faker

from real_estate_api.kupci.models import Kupci

fake = Faker()


class KupciFactory(factory.django.DjangoModelFactory):
    lice = 'Fizicko'
    ime_prezime = fake.name()
    email = fake.email()
    broj_telefona = fake.phone_number()
    Jmbg_Pib = '1234567890'
    adresa = 'Test Adresa 1'

    class Meta:
        model = Kupci
