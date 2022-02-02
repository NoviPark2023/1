from real_estate_api.garaze.models import Garaze


class TestEntitetaGaraze:
    """Testiranje entiteta Garaze"""

    def test_kreiraj_novu_garazu(self, nova_jedna_garaza_fixture, novi_kupac_fixture_garaze):
        """
        testiranje kreiranje nove Garaze u bazi podataka i provera "id_garaze".

        * @see conftest.py (nova_jedna_garaza_fixture)
        @param nova_jedna_garaza_fixture: Entitet Garaze
        """
        garaze_from_db = Garaze.objects.all()

        assert garaze_from_db.first().id_garaze == 1

    def test_sva_polja_garaze(self, nova_jedna_garaza_fixture):
        """
        Testiranje svih polja modela 'Garaze'.

        * @see conftest.py (nova_jedna_garaza_fixture)
        @param nova_jedna_garaza_fixture: Entitet Garaze
        """
        garaze_from_db = Garaze.objects.all()

        assert nova_jedna_garaza_fixture.id_garaze == garaze_from_db[0].id_garaze
        assert nova_jedna_garaza_fixture.jedinstveni_broj_garaze == garaze_from_db[0].jedinstveni_broj_garaze
        assert nova_jedna_garaza_fixture.kupac == garaze_from_db[0].kupac
        assert nova_jedna_garaza_fixture.ime_kupca == garaze_from_db[0].ime_kupca
        assert nova_jedna_garaza_fixture.cena_garaze == garaze_from_db[0].cena_garaze
        assert nova_jedna_garaza_fixture.napomena_garaze == garaze_from_db[0].napomena_garaze
        assert nova_jedna_garaza_fixture.status_prodaje_garaze == garaze_from_db[0].status_prodaje_garaze

    def test_broj_novih_garaza_u_bazi(self, nova_jedna_garaza_fixture):
        """
        Testiranje broja kreiranih Garaza u bazi.

        @param nova_jedna_garaza_fixture: Entitet Garaze
        """
        assert Garaze.objects.all().count() == 1
