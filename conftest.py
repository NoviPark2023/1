import pytest

from factories_kupci import KupciFactory
from real_estate_api.kupci.models import Kupci
from pytest_factoryboy import register

register(KupciFactory) # for impl. use: < kupci_factory >

@pytest.fixture()
def kupac(db, kupci_factory) -> Kupci:
    kupac = kupci_factory.create()
    return kupac

# @pytest.fixture()
# def novi_kupac_factory(db):
#     def kreiranje_kupca(
#         lice: str = 'Fizicko',
#         ime_prezime: str = 'Slobodan Tomic',
#         email: str = 'sloba@factoryww.com',
#         broj_telefona: str = '+381 63 136 90 98',
#         Jmbg_Pib: str = '123456789123',
#         adresa: str = 'Test Adresa Kupaca',
#     ):
#         kupac = Kupci.objects.create(
#             lice=lice,
#             ime_prezime=ime_prezime,
#             email=email,
#             broj_telefona=broj_telefona,
#             Jmbg_Pib=Jmbg_Pib,
#             adresa=adresa,
#         )
#         return kupac
#
#     return kreiranje_kupca



#
#
# @pytest.fixture
# def kreiraj_novog_kupaca_fizicko_lice(db, novi_kupac_factory) -> Kupci:
#     return novi_kupac_factory(lice="Fizicko")
#
#
# @pytest.fixture
# def kreiraj_novog_kupaca_pravno_lice(db, novi_kupac_factory) -> Kupci:
#     return novi_kupac_factory(lice="Pravno")
