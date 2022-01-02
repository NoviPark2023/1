import pytest
from faker import Faker

from real_estate_api.kupci.models import Kupci

fake = Faker()


@pytest.mark.django_db
def test_new_korisnik(kupci_factory):

    kupac = kupci_factory.create()

    print('\n')

    print(f'########### KUPAC IME PREZIME: {kupci_factory.ime_prezime}  #############################')

    print(f'########### KUPAC EMAIL: {kupci_factory.email}  #############################')

    print(f'##############  TELEFON KUPCA: {kupci_factory.broj_telefona}  ##########################')

    broj_kupaca_u_bazi = Kupci.objects.all().count()
    print(f'##############  COUNT: {broj_kupaca_u_bazi}  ##########################')

    assert broj_kupaca_u_bazi == 1
    assert kupac.id_kupca == 1
    assert kupac.lice == "Fizicko"
    assert kupac.Jmbg_Pib == "1234567890"
    assert kupac.adresa == "Test Adresa 1"
