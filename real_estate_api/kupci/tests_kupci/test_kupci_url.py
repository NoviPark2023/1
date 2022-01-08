class TestRestApiKupci:
    """Testitanje API Endpointa entireta Kupci"""

    endpoint_svi_kupci = '/kupci'
    endpoint_detalji_kupca = f'{endpoint_svi_kupci}/detalji-kupca'

    def test_sa_ne_autorizovanim_korisnikom(self, client, django_user_model, novi_korisnik_ne_autorizovan_fixture):
        """
        Test poziv 'endpoint_svi_kupci' -a sa ne autorizovanim korisnikom.

            * @see conftest.py (novi_korisnik_ne_autorizovan_fixture)

        @param client: A Django test client instance.
        @param django_user_model: Korisnik.
        @param novi_korisnik_ne_autorizovan_fixture: Obican Korisnik bez autorizacije.
        @return status code 401: Unauthorized
        """
        response = client.get(f'{self.endpoint_svi_kupci}/')

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self, client, django_user_model, novi_autorizovan_korisnik_fixture):
        """
        Test poziv 'endpoint_svi_kupci' -a sa autorizovanim korisnikom.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)

        @param client: A Django test client instance.
        @param django_user_model: Korisnik.
        @param novi_autorizovan_korisnik_fixture: Obican Korisnik sa autorizacijom.
        @return status code 200: OK
        """

        response = client.get(f'{self.endpoint_svi_kupci}/')

        assert response.status_code == 200

    def test_detealji_kupca(self, client, django_user_model, novi_autorizovan_korisnik_fixture, novi_kupac_fixture):
        """
        Test poziv 'endpoint_detalji_kupca' za API poziv Detalja Kupca sa autorizovanim korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (novi_kupac_fixture)

        @param client: A Django test client instance.
        @param django_user_model: Korisnik.
        @param novi_kupac_fixture: Klinet (Kupac).
        @param novi_autorizovan_korisnik_fixture: Obican Korisnik sa autorizacijom.
        """

        response = client.get(f'{self.endpoint_detalji_kupca}/{novi_kupac_fixture.id_kupca}/')

        assert response.status_code == 200

        assert response.json() == {
            "id_kupca": novi_kupac_fixture.id_kupca,
            "lice": novi_kupac_fixture.lice,
            "ime_prezime": novi_kupac_fixture.ime_prezime,
            "email": novi_kupac_fixture.email,
            "broj_telefona": novi_kupac_fixture.broj_telefona,
            "Jmbg_Pib": str(novi_kupac_fixture.Jmbg_Pib),
            "adresa": novi_kupac_fixture.adresa,
            "lista_ponuda_kupca": [],
            "izmeni_kupca_url": "/kupci/izmeni-kupca/1/",
            "obrisi_kupca_url": "/kupci/obrisi-kupca/1/",
            "lista_kupaca_url": "/kupci/"
        }
