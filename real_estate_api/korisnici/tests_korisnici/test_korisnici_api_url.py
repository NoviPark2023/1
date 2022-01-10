from rest_framework.reverse import reverse

from real_estate_api.korisnici.models import Korisnici


class TestRestApiUrlsKorisnici:
    """Testitanje API URLs Endpointa entiteta Korisnici"""

    def test_sa_ne_autorizovanim_korisnikom(self, client):
        """
        Test poziv 'lista_korisnika' -a sa ne autorizovanim Korisnikom.

        @param client: A Django test client instance.
        @return status code 401: HTTP Unauthorized
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
        @return status code 200: HTTP OK
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
        @return status code 200: HTTP OK
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
        @return status code 201:  HTTP 201 CREATED
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
        @return status code 200: HTTP OK
        """

        # Prvo proveri koliko je korisnika u bazi (trenutno samo jedan SUPER USER)
        broj_korisnika_u_bazi = Korisnici.objects.all().count()
        assert broj_korisnika_u_bazi == 1

        url_detalji_korisnika = reverse('korisnici:detalji_korisnika', args=[novi_jedan_auth_korisnik_fixture.id])

        response = client.get(url_detalji_korisnika)

        assert response.status_code == 200

    def test_izmeni_korisnika(self, client, novi_jedan_auth_korisnik_fixture, novi_jedan_korisnik_json_fixture):
        """
        Test poziv 'korisnici:izmeni_korisnika' za API poziv Izmeni Korisnika sa Korisnikom iz fixture
        "novi_jedan_korisnik_json_fixture". Proverava se razlika i to po:
            * ime
            * prezime
            * email
            * username
            * role
            * is_superuser

        Takodje se proverava i Response status code.

            * @see /test_korisnici/conftest.py (novi_jedan_auth_korisnik_fixture)
            * @see /test_korisnici/conftest.py (novi_jedan_korisnik_json_fixture)
            * @see path('izmeni-korisnika/<int:id>/', UrediKorisnika.as_view(), name='izmeni_korisnika'),

        @param client: A Django test client instance.
        @param novi_jedan_auth_korisnik_fixture: Autorizovan Superuser Korisnik.
        @param novi_jedan_korisnik_json_fixture: Korisnik za izmenu.
        @return status code 200: HTTP OK
        """

        # Prvo proveri koliko je korisnika u bazi (trenutno samo jedan SUPER USER)
        broj_korisnika_u_bazi = Korisnici.objects.all().count()
        assert broj_korisnika_u_bazi == 1

        url_izmeni_korisnika = reverse('korisnici:izmeni_korisnika', args=[novi_jedan_auth_korisnik_fixture.id])

        response = client.put(url_izmeni_korisnika,
                              data=novi_jedan_korisnik_json_fixture,
                              content_type='application/json'
                              )

        assert response.status_code == 200

        assert response.json()["ime"] != novi_jedan_auth_korisnik_fixture.ime
        assert response.json()["prezime"] != novi_jedan_auth_korisnik_fixture.prezime
        assert response.json()["email"] != novi_jedan_auth_korisnik_fixture.email
        assert response.json()["username"] != novi_jedan_auth_korisnik_fixture.username
        assert response.json()["role"] != novi_jedan_auth_korisnik_fixture.role
        assert response.json()["is_superuser"] != novi_jedan_auth_korisnik_fixture.is_superuser

    def test_obrisi_korisnika(self, client, novi_jedan_auth_korisnik_fixture):
        """
        Test poziv 'korisnici:obrisi_korisnika' za API poziv Obrisi Korisnika.

            * @see /test_korisnici/conftest.py (novi_jedan_auth_korisnik_fixture)
            * @see path('obrisi-korisnika/<int:id>/', ObrisiKoriniska.as_view(), name='obrisi_korisnika')

        @param client: A Django test client instance.
        @param novi_jedan_auth_korisnik_fixture: Autorizovan Superuser Korisnik.
        @return status code 204: HTTP No Content
        """

        # Prvo proveri koliko je korisnika u bazi (trenutno samo jedan SUPER USER)
        broj_korisnika_u_bazi = Korisnici.objects.all().count()
        assert broj_korisnika_u_bazi == 1

        url_obrisi_korisnika = reverse('korisnici:obrisi_korisnika', args=[novi_jedan_auth_korisnik_fixture.id])

        response = client.delete(url_obrisi_korisnika)

        assert response.status_code == 204

        # Prvo proveri koliko je korisnika u bazi (treba da ima 0 korisnika)
        broj_korisnika_u_bazi = Korisnici.objects.all().count()
        assert broj_korisnika_u_bazi == 0
