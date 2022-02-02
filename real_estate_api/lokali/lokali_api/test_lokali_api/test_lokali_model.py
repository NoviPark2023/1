from real_estate_api.lokali.lokali_api.models import Lokali


class TestEntitetaLokali:
    """Testiranje entiteta Lokali"""

    def test_kreiraj_novi_lokal(self, novi_jedan_lokal_fixture):
        """
        testiranje kreiranja novog Lokala u bazi podataka i provera "id_lokala".

        * @see conftest.py (novi_jedan_lokal_fixture)
        @param novi_jedan_lokal_fixture: Entitet Lokali
        """
        lokali_from_db = Lokali.objects.all()
        assert lokali_from_db.count() == 1
        assert lokali_from_db.first().id_lokala == 1

    def test_sva_polja_lokala(self, novi_jedan_lokal_fixture):
        """
        Testiranje svih polja modela 'Lokali'.

        * @see conftest.py (novi_jedan_lokal_fixture)
        @param novi_jedan_lokal_fixture: Entitet Lokali
        """
        lokali_from_db = Lokali.objects.all()

        assert novi_jedan_lokal_fixture.id_lokala == lokali_from_db[0].id_lokala
        assert novi_jedan_lokal_fixture.lamela_lokala == lokali_from_db[0].lamela_lokala
        assert novi_jedan_lokal_fixture.adresa_lokala == lokali_from_db[0].adresa_lokala
        assert novi_jedan_lokal_fixture.kvadratura_lokala == lokali_from_db[0].kvadratura_lokala
        assert novi_jedan_lokal_fixture.broj_prostorija == lokali_from_db[0].broj_prostorija
        assert novi_jedan_lokal_fixture.napomena_lokala == lokali_from_db[0].napomena_lokala
        assert novi_jedan_lokal_fixture.orijentisanost_lokala == lokali_from_db[0].orijentisanost_lokala
        assert novi_jedan_lokal_fixture.status_prodaje_lokala == lokali_from_db[0].status_prodaje_lokala
        assert novi_jedan_lokal_fixture.cena_lokala == lokali_from_db[0].cena_lokala

    def test_broj_novih_lokala_u_bazi(self, novi_jedan_lokal_fixture):
        """
        Testiranje broja kreiranih Lokala u bazi.

        @param novi_jedan_lokal_fixture: Entitet Lokali
        """
        assert Lokali.objects.all().count() == 1
