import json

from rest_framework.reverse import reverse


class TestRestApiKupci:
    """Testitanje API Endpointa entiteta Kupci"""

    def test_sa_ne_autorizovanim_korisnikom(self, client):
        """
        Test poziv 'endpoint_svi_kupci' -a sa ne autorizovanim Korisnikom.

            * @see conftest.py (novi_korisnik_ne_autorizovan_fixture)

        @param client: A Django test client instance.
        @param novi_korisnik_ne_autorizovan_fixture: Obican Korisnik bez autorizacije.
        @return status code 401: Unauthorized
        """

        url_svi_kupca = reverse('kupci:lista_kupaca')

        response = client.get(url_svi_kupca)

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self, client, novi_autorizovan_korisnik_fixture):
        """
        Test poziv 'endpoint_svi_kupci' -a sa autorizovanim Korisnikom.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture: Obican Korisnik sa autorizacijom.
        @return status code 200: OK
        """

        url_svi_kupca = reverse('kupci:lista_kupaca')

        response = client.get(url_svi_kupca)

        assert response.status_code == 200

    def test_detalji_kupca(self, client, novi_autorizovan_korisnik_fixture, novi_kupac_fixture):
        """
        Test poziv 'endpoint_detalji_kupca' za API poziv Detalja Kupca sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (novi_kupac_fixture)

        @param client: A Django test client instance.
        @param novi_kupac_fixture: Klinet (Kupac).
        @param novi_autorizovan_korisnik_fixture: Obican Korisnik sa autorizacijom.
        """

        url_detalji_kupca = reverse('kupci:detalji_kupca', args=[novi_kupac_fixture.id_kupca])

        response = client.get(url_detalji_kupca)

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

    def test_izmeni_kupca(self, client, novi_autorizovan_korisnik_fixture, novi_kupac_fixture):
        """
        Test poziv 'endpoint_izmeni_kupca' za API poziv Izmeni Kupca sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (novi_kupac_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture: Korisnik.
        @param novi_kupac_fixture: Klinet (Kupac).
        """

        # Proveri prvo da li je ime_prezime iz fixtura 'ime_prezime'
        assert novi_kupac_fixture.ime_prezime == novi_kupac_fixture.ime_prezime

        # Podaci za izmenu Kupca
        test_novi_kupac = json.dumps({
            "lice": "Pravno",
            "ime_prezime": "Slobodan Tomic",
            "email": "slobodan.tomic@factorywws.com",
            "broj_telefona": "+381 63 136 90 988",
            "Jmbg_Pib": "0102030605",
            "adresa": "Milenke Dravica 54"
        })

        url_izmeni_kupca = reverse('kupci:izmeni_kupca', args=[novi_kupac_fixture.id_kupca])

        response = client.put(url_izmeni_kupca, data=test_novi_kupac, content_type='application/json')

        assert response.status_code == 200

        assert response.json()["lice"] == json.loads(test_novi_kupac)['lice']
        assert response.json()["ime_prezime"] == json.loads(test_novi_kupac)['ime_prezime']
        assert response.json()["email"] == json.loads(test_novi_kupac)['email']
        assert response.json()["broj_telefona"] == json.loads(test_novi_kupac)['broj_telefona']
        assert response.json()["Jmbg_Pib"] == json.loads(test_novi_kupac)['Jmbg_Pib']
        assert response.json()["adresa"] == json.loads(test_novi_kupac)['adresa']

    def test_obrisi_kupca(self, client, novi_autorizovan_korisnik_fixture, novi_kupac_fixture):
        """
        Test poziv 'endpoint_obrisi_kupca' za API poziv Obrisi Kupca sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (novi_kupac_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture: Korisnik.
        @param novi_kupac_fixture: Klinet (Kupac).
        """

        # Proveri prvo da li je ID kupca  iz fixtura 'id_kupca'
        assert novi_kupac_fixture.id_kupca == novi_kupac_fixture.id_kupca

        url_obrisi_kupca = reverse('kupci:obrisi_kupca', args=[novi_kupac_fixture.id_kupca])
        print(f'REVERSE URLs: {url_obrisi_kupca}')

        response = client.get(url_obrisi_kupca)

        assert response.status_code == 200
