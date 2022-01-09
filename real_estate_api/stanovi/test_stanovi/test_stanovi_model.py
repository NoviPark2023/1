from ..models import Stanovi


class TestEntitetaStanovi:
    """Testiranje entiteta Stanovi"""

    def test_kreiraj_novi_stan(self, novi_jedan_stan_fixture):
        """
        testiranje kreiranje novog Stana u bazi podataka i provera "id_stana".

        * @see conftest.py (novi_jedan_stan_fixture)
        @param novi_jedan_stan_fixture: Entitet Stanovi
        """
        stanovi_from_db = Stanovi.objects.all()

        assert stanovi_from_db.first().id_stana == 1

    def test_sva_polja_stana(self, novi_jedan_stan_fixture):
        # TODO:  (IVANA) Testirati sva polja stana iz modela "Stanovi".
        # @ see: TestEntitetaKupci: test_kreiranje_novog_kupca
        pass

    def test_broj_novih_stanova_u_bazi(self, novi_jedan_stan_fixture):
        # TODO:  (IVANA) Testirati koliko je napravljeno Stanova u bazi.
        # @ see: TestEntitetaKupci: test_broj_novih_kupca_u_bazi
        pass

    # TODO:  (IVANA) TESTIRANJE AZURIRANJA CENA STANA !

    # TODO:  (IVANA) TESTIRANJE SVEGA STO IVANA MISLI DA TREBA U MODELU !!!
