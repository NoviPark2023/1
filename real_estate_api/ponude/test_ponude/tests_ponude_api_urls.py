from rest_framework.reverse import reverse

from real_estate_api.ponude.models import Ponude


class TestRestApiUrlsPonude:
    """Testitanje API URLs Endpointa entiteta Ponude"""

    def test_sa_ne_autorizovanim_korisnikom(self, client):
        """
        Test poziv 'lista_ponuda' -a sa ne autorizovanim Korisnikom.

        @param client: A Django test client instance.
        @return status code 401: HTTP Unauthorized
        """

        url_sve_ponude = reverse('ponude:lista_ponuda')

        response = client.get(url_sve_ponude)

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self, client, novi_jedan_auth_korisnik_fixture):
        """
        Test poziv 'ponude:lista_ponuda' sa autorizovanim SuperUser Korisnikom.

            * @see /test_ponude/conftest.py : novi_jedan_auth_korisnik_fixture

        @param client: A Django test client instance.
        @param novi_jedan_auth_korisnik_fixture: Autorizovan Superuser Korisnik.
        @return status code 200: HTTP OK
        """

        url_sve_ponude = reverse('ponude:lista_ponuda')

        response = client.get(url_sve_ponude)

        assert response.status_code == 200

    def test_lista_svih_ponuda_api_url(self, client, novi_jedan_auth_korisnik_fixture):
        """
        Test poziv 'ponude:lista_ponuda' za API poziv listing svih Ponuda.

            * @see /test_ponude/conftest.py (novi_jedan_auth_korisnik_fixture)
            * @see path('', ListaKorisnikaAPIview.as_view(), name='lista_korisnika')

        @param client: A Django test client instance.
        @param novi_jedan_auth_korisnik_fixture: Autorizovan Superuser Korisnik.
        @return status code 200: HTTP OK
        """

        url_sve_ponude = reverse('ponude:lista_ponuda')

        response_sve_ponude = client.get(url_sve_ponude)

        assert response_sve_ponude.status_code == 200

    def test_kreiraj_ponudu_status_potencijalan_401(self, client, nova_jedna_ponuda_json_fixture):
        """
        Test poziv 'ponude:kreiraj_ponudu' za API poziv kreiranja Ponude sa Korisnikom
        koji NIJE AUTORIZOVAN.

            * @see /test_ponude/conftest.py (nova_jedna_ponuda_json_fixture)
            * @see path('kreiraj-ponudu/', KreirajPonuduAPIView.as_view(), name='kreiraj_ponudu'),

        @param client: A Django test client instance.
        @param nova_jedna_ponuda_json_fixture: Nova Ponuda Fixture.
        @return status code 401: HTTP Unauthorized.
        """

        url_kreiraj_ponudu = reverse('ponude:kreiraj_ponudu')

        response_kreiraj_ponudu = client.post(
            url_kreiraj_ponudu,
            data=nova_jedna_ponuda_json_fixture,
            content_type='application/json'
        )

        # response_kreiraj_korisnka = client.post(url_kreiraj_korisnika)
        assert response_kreiraj_ponudu.status_code == 401

        # Proveri koliko je Ponuda u DBu
        broj_ponuda_from_db = Ponude.objects.all().count()
        assert broj_ponuda_from_db == 0

    def test_kreiraj_ponudu_status_potencijalan_200(self,
                                                    client,
                                                    nova_jedna_ponuda_json_fixture,
                                                    novi_jedan_auth_korisnik_fixture
                                                    ):
        """
        Test poziv 'ponude:kreiraj_ponudu' za API poziv kreiranja Ponude sa Korisnikom
        koji JE AUTORIZOVAN.

            * @see /test_ponude/conftest.py (nova_jedna_ponuda_json_fixture)
            * @see /test_ponude/conftest.py (novi_jedan_auth_korisnik_fixture)
            * @see path('kreiraj-ponudu/', KreirajPonuduAPIView.as_view(), name='kreiraj_ponudu'),

        @param client: A Django test client instance.
        @param nova_jedna_ponuda_json_fixture: Nova Ponuda Fixture.
        @return status code 201:  HTTP 201 CREATED
        """

        # Proveri da li je DB prazna, tj. nema ni jedna Ponuda.
        broj_ponuda_from_db = Ponude.objects.all().count()
        assert broj_ponuda_from_db == 0

        url_kreiraj_ponudu = reverse('ponude:kreiraj_ponudu')

        response_kreiraj_ponudu = client.post(
            url_kreiraj_ponudu,
            data=nova_jedna_ponuda_json_fixture,
            content_type='application/json'
        )

        assert response_kreiraj_ponudu.status_code == 201

        # Nakon kreiranja Ponude, proveri koliko ima Ponuda *(1).
        broj_ponuda_from_db = Ponude.objects.all().count()
        assert broj_ponuda_from_db == 1

    def test_detalji_ponude(self, client, novi_jedan_auth_korisnik_fixture, nova_jedna_ponuda):
        """
        Test poziv 'ponude:detalji_ponude' za API poziv detalja Ponude.
        U samoj inicijalizaciji imamo samo jednou Ponudu.

            * @see /test_ponude/conftest.py (nova_jedna_ponuda)
            * @see path('detalji-ponude/<int:id_ponude>/', PonudeDetaljiAPIView.as_view(), name='detalji_ponude')
        ---
        @param client: A Django test client instance.
        @param novi_jedan_auth_korisnik_fixture: Autorizovan Superuser Korisnik.
        @param nova_jedna_ponuda: Ponuda.
        @return status code 200: HTTP OK
        """

        broj_ponuda_from_db = Ponude.objects.all().count()
        assert broj_ponuda_from_db == 1

        url_detalji_ponude = reverse('ponude:detalji_ponude', args=[nova_jedna_ponuda.id_ponude])

        response = client.get(url_detalji_ponude)
        assert response.status_code == 200

    def test_izmeni_ponudu(self, client, nova_jedna_ponuda, nova_jedna_ponuda_json_fixture):
        """
        Test poziv 'ponude:izmeni_ponudu' za API poziv izmene Ponude.
        U samoj inicijalizaciji imamo samo jednou Ponudu.

            * @see /test_ponude/conftest.py (nova_jedna_ponuda)
            * @see /test_ponude/conftest.py (nova_jedna_ponuda_json_fixture)
            * @see path('izmeni-ponudu/<int:id_ponude>/', UrediPonuduViewAPI.as_view(), name='izmeni_ponudu')
        ---
        @param client: A Django test client instance.
        @param nova_jedna_ponuda: Ponuda.
        @return status code 200: HTTP OK
        """
        broj_ponuda_from_db = Ponude.objects.all().count()
        assert broj_ponuda_from_db == 1

        url_izmeni_ponudu = reverse('ponude:izmeni_ponudu', args=[nova_jedna_ponuda.id_ponude])

        response = client.put(url_izmeni_ponudu,
                              data=nova_jedna_ponuda_json_fixture,
                              content_type='application/json'
                              )

        assert response.status_code == 200

    def test_obrisi_ponudu(self, client, nova_jedna_ponuda):
        """
        Test poziv 'ponude:obrisi_ponudu' za API poziv Obrisi Ponudu.

            * @see /test_ponude/conftest.py (nova_jedna_ponuda)
            * @see path('obrisi-ponudu/<int:id_ponude>/', ObrisiPonuduAPIView.as_view(), name='obrisi_ponudu')

        @param client: A Django test client instance.
        @return status code 204: HTTP No Content
        """

        broj_ponuda_from_db = Ponude.objects.all().count()
        assert broj_ponuda_from_db == 1

        url_obrisi_ponudu = reverse('ponude:obrisi_ponudu', args=[nova_jedna_ponuda.id_ponude])

        response = client.delete(url_obrisi_ponudu)

        assert response.status_code == 204

        # Prvo proveri koliko je Ponuda u bazi (treba da ima 0 Ponuda)
        broj_ponuda_u_bazi = Ponude.objects.all().count()
        assert broj_ponuda_u_bazi == 0
