endpoint = '/kupci/'


class TestRestApiKupci:
    """Testitanje API Endpointa entireta Kupci"""

    def test_sa_ne_autorizovanim_korisnikom(self, client, django_user_model, novi_korisnik_ne_autorizovan_fixture):
        """
        Test poziv 'endpoint' -a sa ne autorizovanim korisnikom.
            * @see conftest.py

        @param client: Korisnik.
        @param django_user_model: Korisnik.
        @param novi_korisnik_ne_autorizovan_fixture: Obican Korisnik bez autorizacije.
        """
        response = client.get(endpoint)

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self, client, django_user_model, novi_autorizovan_korisnik_fixture):
        """
        Test poziv 'endpoint' -a sa autorizovanim korisnikom.
            * @see conftest.py

        @param client: Korisnik.
        @param django_user_model: Korisnik.
        @param novi_korisnik_ne_autorizovan_fixture: Obican Korisnik bez autorizacije.
        """

        response = client.get(endpoint)

        assert response.status_code == 200
