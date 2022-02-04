from rest_framework.reverse import reverse
from real_estate_api.lokali.ponude_lokala.test_ponude_lokala.conftest import *


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

    def test_lista_svih_ponuda_lokala_api_url(self, client, novi_autorizovan_korisnik_fixture_lokali_ponude):
        """
        Test poziv 'ponude-lokali:lista_ponuda_lokala' za API poziv listing svih Ponuda Lokala.

            * @see /test_ponude_lokala/conftest.py (novi_autorizovan_korisnik_fixture_lokali_ponude)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_lokali_ponude: Autorizovan Korisnik.
        @return status code 200: HTTP OK
        """
        url_sve_ponude_lokala = reverse('ponude-lokali:lista_ponuda_lokala')

        response_sve_ponude_lokala = client.get(url_sve_ponude_lokala)

        assert response_sve_ponude_lokala.status_code == 200

    def test_detalji_ponude_lokala_api_url(
        self,
        client,
        novi_autorizovan_korisnik_fixture_lokali_ponude,
        nova_jedna_ponuda_lokala_fixture):
        """
        Test poziv 'ponude_lokala:detalji_ponude_lokala' za API poziv detalja Ponude Lokala.
        U samoj inicijalizaciji imamo samo jednou Ponudu.

            * @see /test_ponude_lokala/conftest.py (nova_jedna_ponuda_lokala_fixture)
            * @see path('detalji-ponude-lokala/<int:id_ponude_lokala>/',
            DetaljiPonudeLokalaAPIView.as_view(),
            name='detalji_ponude')
        ---
        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_lokali_ponude: Autorizovan Korisnik.
        @param nova_jedna_ponuda_lokala_fixture: Ponuda Lokala.
        @return status code 200: HTTP OK
        """
        broj_ponuda_lokala_from_db = PonudeLokala.objects.all().count()
        assert broj_ponuda_lokala_from_db == 1

        url_detalji_ponude_lokala = reverse('ponude-lokali:detalji_ponude_lokala',
                                            args=[nova_jedna_ponuda_lokala_fixture.id_ponude_lokala])

        response = client.get(url_detalji_ponude_lokala)

        assert response.status_code == 200

    def test_kreiraj_ponudu_lokala_status_potencijalan_401(self,
                                                           client,
                                                           nova_jedna_ponuda_lokala_fixture_401):
        """
        Test poziv 'ponude_lokala:kreiraj_ponudu_lokala' za API poziv kreiranja Ponude Lokala sa Korisnikom
        koji NIJE AUTORIZOVAN.

            * @see /test_ponude_lokala/conftest.py (nova_jedna_ponuda_lokala_fixture_401)
            * @see path('kreiraj-ponudu-lokala/', KreirajPonuduLokalaAPIView.as_view(), name='kreiraj_ponudu_lokala'),

        @param client: A Django test client instance.
        @param nova_jedna_ponuda_lokala_fixture_401: Nova Ponuda Lokala Fixture.
        @return status code 401: HTTP Unauthorized.
        """
        url_kreiraj_ponudu_lokala = reverse('ponude-lokali:kreiraj_ponudu_lokala')

        response_kreiraj_ponudu_lokala = client.post(
            url_kreiraj_ponudu_lokala,
            data=nova_jedna_ponuda_lokala_fixture_401,
            content_type='application/json'
        )

        assert response_kreiraj_ponudu_lokala.status_code == 401

        # Proveriti koliko je Ponuda Lokala u DBu
        broj_ponuda_lokala_from_db = PonudeLokala.objects.all().count()
        assert broj_ponuda_lokala_from_db == 1

    def test_kreiraj_ponudu_lokala_status_potencijalan_201(self,
                                                           client,
                                                           nova_jedna_ponuda_lokala_json_fixture,
                                                           novi_autorizovan_korisnik_fixture_lokali_ponude
                                                           ):
        """
        Test poziv 'ponude-lokali:kreiraj_ponudu_lokala' za API poziv kreiranja Ponude Lokala sa Korisnikom
        koji JE AUTORIZOVAN.

            * @see /test_ponude_lokala/conftest.py (nova_jedna_ponuda_lokala_json_fixture)
            * @see /test_ponude_lokala/conftest.py (novi_autorizovan_korisnik_fixture_lokali_ponude)
             * @see path('kreiraj-ponudu-lokala/', KreirajPonuduLokalaAPIView.as_view(), name='kreiraj_ponudu_lokala'),

        @param client: A Django test client instance.
        @param nova_jedna_ponuda_lokala_json_fixture: Nova Ponuda Lokala Fixture.
        @return status code 201:  HTTP 201 CREATED
        """

        # Proveriti da li je DB prazna, tj. nema ni jedne Ponude Lokala.
        broj_ponuda_lokala_from_db = PonudeLokala.objects.all().count()
        assert broj_ponuda_lokala_from_db == 0

        url_kreiraj_ponudu_lokala = reverse('ponude-lokali:kreiraj_ponudu_lokala')

        response_kreiraj_ponudu_lokala = client.post(
            url_kreiraj_ponudu_lokala,
            data=nova_jedna_ponuda_lokala_json_fixture,
            content_type='application/json'
        )

        print(response_kreiraj_ponudu_lokala)

        assert response_kreiraj_ponudu_lokala.status_code == 201

        # # Nakon kreiranja Ponude Lokala, proveriti koliko ih ima u db, treba da bude 1.
        # broj_ponuda_lokala_from_db = PonudeLokala.objects.all().count()
        # assert broj_ponuda_lokala_from_db == 1
