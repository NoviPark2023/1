from rest_framework.reverse import reverse


class TestRestApiUrlsPonudeLokala:
    """Testitanje API URLs Endpointa entiteta Ponude Lokala"""

    def test_sa_neautorizovanim_korisnikom(self, client):
        """
        Test poziv 'lista_ponuda_lokala' sa neautorizovanim Korisnikom.

        @param client: A Django test client instance.
        @return status code 401: HTTP Unauthorized
        """
        url_sve_ponude_lokala = reverse('ponude-lokali:lista_ponuda_lokala')

        response = client.get(url_sve_ponude_lokala)

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self, client, novi_autorizovan_korisnik_fixture_lokali_ponude):
        """
        Test poziv 'ponude-lokali:lista_ponuda_lokala' sa autorizovanim Korisnikom.

            * @see /test_ponude_lokala/conftest.py : novi_autorizovan_korisnik_fixture_lokali_ponude

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_lokali_ponude: Autorizovan Korisnik.
        @return status code 200: HTTP OK
        """
        url_sve_ponude_lokala = reverse('ponude-lokali:lista_ponuda_lokala')

        response = client.get(url_sve_ponude_lokala)

        assert response.status_code == 200


