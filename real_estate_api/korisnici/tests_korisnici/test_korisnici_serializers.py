from rest_framework.reverse import reverse


class TestKorisniciSerijalizers:
    """Tesritanje Serijalizers KORISNICI"""

    def test_serializers_svi_korisnici(self, client, nova_tri_korisnika_fixture, novi_jedan_auth_korisnik_fixture):
        """
        Testiranje serijalizera za pregled svih Klijenata(Kupaca) sa fixturom od dva kreirana nova Kupca.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (nova_dva_kupaca_fixture)

        @param client: A Django test client instance.
        @param nova_dva_kupaca_fixture: Kupci
        @param novi_autorizovan_korisnik_fixture_kupci: Korisnik
        """

    assert True
