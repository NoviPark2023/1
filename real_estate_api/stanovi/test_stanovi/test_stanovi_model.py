from decimal import Decimal

from ..models import Stanovi, AzuriranjeCena


class TestEntitetaStanovi:
    """Testiranje entiteta Stanovi"""

    def test_kreiraj_novi_stan(self, novi_jedan_stan_fixture_stanovi):
        """
        testiranje kreiranje novog Stana u bazi podataka i provera "id_stana".

        * @see conftest.py (novi_jedan_stan_fixture)
        @param novi_jedan_stan_fixture_stanovi: Entitet Stanovi
        """
        stanovi_from_db = Stanovi.objects.all()

        assert stanovi_from_db.first().id_stana == 1

    def test_sva_polja_stana(self, novi_jedan_stan_fixture_stanovi):
        """
        Testiranje svih polja modela 'Stanovi'.

        * @see conftest.py (novi_jedan_stan_fixture)
        @param novi_jedan_stan_fixture_stanovi: Entitet Stanovi
        """
        stan_from_db = Stanovi.objects.all()

        assert novi_jedan_stan_fixture_stanovi.id_stana == stan_from_db[0].id_stana
        assert novi_jedan_stan_fixture_stanovi.lamela == stan_from_db[0].lamela
        assert novi_jedan_stan_fixture_stanovi.adresa_stana == stan_from_db[0].adresa_stana
        assert (
            novi_jedan_stan_fixture_stanovi.kvadratura == str(round(Decimal(stan_from_db[0].kvadratura), 2))
        )
        assert (
            str(round(Decimal(novi_jedan_stan_fixture_stanovi.kvadratura_korekcija), 2)) ==
            str(round(Decimal(stan_from_db[0].kvadratura_korekcija), 2))
        )
        assert (
            novi_jedan_stan_fixture_stanovi.iznos_za_korekciju_kvadrature
            == str(round(Decimal(stan_from_db[0].iznos_za_korekciju_kvadrature), 2))
        )
        assert novi_jedan_stan_fixture_stanovi.sprat == stan_from_db[0].sprat
        assert novi_jedan_stan_fixture_stanovi.broj_soba == stan_from_db[0].broj_soba
        assert novi_jedan_stan_fixture_stanovi.orijentisanost == stan_from_db[0].orijentisanost
        assert novi_jedan_stan_fixture_stanovi.broj_terasa == stan_from_db[0].broj_terasa
        assert (
            str(round(Decimal(novi_jedan_stan_fixture_stanovi.cena_stana), 2)) ==
            str(round(Decimal(stan_from_db[0].cena_stana), 2))
        )
        assert (
            str(round(Decimal(novi_jedan_stan_fixture_stanovi.cena_kvadrata), 2)) ==
            str(round(Decimal(stan_from_db[0].cena_kvadrata), 2))
        )
        assert novi_jedan_stan_fixture_stanovi.napomena == stan_from_db[0].napomena
        assert novi_jedan_stan_fixture_stanovi.status_prodaje == stan_from_db[0].status_prodaje

    def test_broj_novih_stanova_u_bazi(self, novi_jedan_stan_fixture_stanovi):
        """
        Testiranje broja kreiranih Stanova u bazi.

        @param novi_jedan_stan_fixture_stanovi: Entitet Stanovi
        """
        assert Stanovi.objects.all().count() == 1

    def test_kreiraj_azuriranje_cena(self, kreiraj_auriranje_cena):
        """
        Testiranje kreiranja Azuriranja cena u bazi podataka i provera "id_azur_cene".

        * @see conftest.py (kreiraj_auriranje_cena)
        @param kreiraj_auriranje_cena: Entitet AzuriranjeCena
        """
        azuriranje_cena_from_db = AzuriranjeCena.objects.all()

        assert azuriranje_cena_from_db.first().id_azur_cene == 1

    def test_sva_polja_azuriranja_cena(self, novo_azuriranje_cena_fixture):
        """
        Testiranje svih polja modela 'AzuriranjeCena'.

        * @see conftest.py (novo_azuriranje_cena_fixture)
        @param novo_azuriranje_cena_fixture: Entitet AzuriranjeCena
        """
        azuriranje_cena_from_db = AzuriranjeCena.objects.all()

        assert novo_azuriranje_cena_fixture.id_azur_cene == azuriranje_cena_from_db[0].id_azur_cene
        assert novo_azuriranje_cena_fixture.sprat == azuriranje_cena_from_db[0].sprat
        assert novo_azuriranje_cena_fixture.broj_soba == azuriranje_cena_from_db[0].broj_soba
        assert novo_azuriranje_cena_fixture.orijentisanost == azuriranje_cena_from_db[0].orijentisanost
        assert novo_azuriranje_cena_fixture.cena_kvadrata == azuriranje_cena_from_db[0].cena_kvadrata
