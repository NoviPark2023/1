from rest_framework.reverse import reverse

from real_estate_api.korisnici.models import Korisnici


class TestRestApiUrlsKorisnici:
    """Testitanje API URLs Endpointa entiteta Korisnici"""

    def test_sa_ne_autorizovanim_korisnikom(self, client):
        """
        Test poziv 'lista_korisnika' -a sa ne autorizovanim Korisnikom.

        @param client: A Django test client instance.
        @return status code 401: Unauthorized
        """

        url_svi_korisnici = reverse('korisnici:lista_korisnika')

        response = client.get(url_svi_korisnici)

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self, client, novi_jedan_auth_korisnik_fixture):
        """
        Test poziv 'lista_korisnika' sa autorizovanim SuperUser Korisnikom.

            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture

        @param client: A Django test client instance.
        @param novi_jedan_auth_korisnik_fixture: Autorizovan Superuser Korisnik.
        @return status code 200: OK
        """

        url_svi_korisnici = reverse('korisnici:lista_korisnika')

        response = client.get(url_svi_korisnici)

        assert response.status_code == 200

    def test_lista_svih_korisnika_api_url(self, client, novi_jedan_auth_korisnik_fixture):
        """
        Test poziv 'korisnici:lista_korisnika' za API poziv listing svih Korisnika.

            * @see /test_korisnici/conftest.py (novi_jedan_auth_korisnik_fixture)
            * @see path('', ListaKorisnikaAPIview.as_view(), name='lista_korisnika')

        @param client: A Django test client instance.
        @param novi_jedan_auth_korisnik_fixture: Autorizovan Superuser Korisnik.
        """

        url_svi_korisnici = reverse('korisnici:lista_korisnika')

        response_svi_korisnici = client.get(url_svi_korisnici)

        assert response_svi_korisnici.status_code == 200

    def test_kreiraj_korisnika(self, client, novi_jedan_auth_korisnik_fixture, novi_jedan_korisnik_json_fixture):
        """
        Test poziv 'korisnici:kreiraj_korisnika' za API poziv kreiranja Korisnika.
        U samoj inicijalizaciji imamo samo jednog superuser-a. Nakon toga ucitavamo
        fixture za novog Korisnika. Proveravamo:
            - Inicijalno koliko je Korisnika.
            - Koliko je Korisnika nakon kreiranja.

            * @see /test_korisnici/conftest.py (novi_jedan_auth_korisnik_fixture)
            * @see /test_korisnici/conftest.py (novi_jedan_korisnik_json_fixture)
            * @see path('kreiraj-korisnika/', KreirajKorisnika.as_view(), name='kreiraj_korisnika')
        ---
        @param client: A Django test client instance.
        @param novi_jedan_auth_korisnik_fixture: Autorizovan Superuser Korisnik.
        @param novi_jedan_korisnik_json_fixture: Novi Korisnik koji se kreira iz Fixture.
        """

        # Prvo proveri koliko je korisnika u bazi (trenutno samo jedan SUPER USER)
        broj_korisnika_u_bazi = Korisnici.objects.all().count()
        assert broj_korisnika_u_bazi == 1

        url_kreiraj_korisnika = reverse('korisnici:kreiraj_korisnika')

        response_kreiraj_korisnka = client.post(
            url_kreiraj_korisnika,
            data=novi_jedan_korisnik_json_fixture,
            content_type='application/json'
        )
        # response_kreiraj_korisnka = client.post(url_kreiraj_korisnika)
        assert response_kreiraj_korisnka.status_code == 201

        # Proveri koliko je Korisnika u DB pole kreiranja novog (trebalo bi da ima 2).
        # Jedan je SuperUser, a drugi je kreiran iz Fixture (novi_jedan_korisnik_json_fixture).
        broj_korisnika_u_bazi = Korisnici.objects.all().count()
        assert broj_korisnika_u_bazi == 2

    def test_detalji_korisnika(self, client, novi_jedan_auth_korisnik_fixture):
        """
        Test poziv 'korisnici:detalji_korisnika' za API poziv detalja Korisnika.
        U samoj inicijalizaciji imamo samo jednog superuser-a.
         Proveravamo:
            - Inicijalno koliko je Korisnika (samo jedan).

            * @see /test_korisnici/conftest.py (novi_jedan_auth_korisnik_fixture)
            * @see path('detalji-korisnika/<int:id>/', KorisniciDetaljiAPIView.as_view(), name='detalji_korisnika')
        ---
        @param client: A Django test client instance.
        @param novi_jedan_auth_korisnik_fixture: Autorizovan Superuser Korisnik.
        """

        # Prvo proveri koliko je korisnika u bazi (trenutno samo jedan SUPER USER)
        broj_korisnika_u_bazi = Korisnici.objects.all().count()
        assert broj_korisnika_u_bazi == 1

        url_detalji_korisnika = reverse('korisnici:detalji_korisnika', args=[novi_jedan_auth_korisnik_fixture.id])

        response = client.get(url_detalji_korisnika)

        assert response.status_code == 200
