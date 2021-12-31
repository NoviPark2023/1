from real_estate_api.kupci.models import Kupci


class TestKupciSerializersAppModels:

    def test_kreiranje_novog_kupca(self, kreiraj_novog_kupaca):
        assert kreiraj_novog_kupaca.id_kupca == 1
        assert kreiraj_novog_kupaca.lice == "Fizicko"
        assert kreiraj_novog_kupaca.ime_prezime == "Slobodan Tomic"
        assert kreiraj_novog_kupaca.email == "sloba@factoryww.com"
        assert kreiraj_novog_kupaca.broj_telefona == "+381 63 136 90 98"
        assert kreiraj_novog_kupaca.Jmbg_Pib == "123456789123"
        assert kreiraj_novog_kupaca.adresa == "Test Adresa Kupaca"
        assert Kupci.objects.count() == 1
        assert Kupci.objects.count() != 2

    def test_kreiranje_novog_kupca_fizicko_lice(self, kreiraj_novog_kupaca_fizicko_lice):
        assert kreiraj_novog_kupaca_fizicko_lice.lice == "Fizicko"

    def test_kreiranje_novog_kupca_pravno_lice(self, kreiraj_novog_kupaca_pravno_lice):
        assert kreiraj_novog_kupaca_pravno_lice.lice == "Pravno"

