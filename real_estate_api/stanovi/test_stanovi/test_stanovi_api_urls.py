import json
from decimal import Decimal

from rest_framework.reverse import reverse

from real_estate_api.stanovi.models import Stanovi


class TestRestApiUrlsStanovi:
    """Testitanje API URLs Endpointa entiteta Stanovi"""

    def test_sa_neautorizovanim_korisnikom(self, client):
        """
        Test poziv 'endpoint_svi_kupci' sa neautorizovanim Korisnikom.

        * @see conftest.py (novi_korisnik_ne_autorizovan_fixture)

        @param client: A Django test client instance.
        @return status code 401: Unauthorized
        """

        url_svi_stanovi = reverse('stanovi:lista_stanova')

        response = client.get(url_svi_stanovi)

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self, client, novi_autorizovan_korisnik_fixture_stanovi):
        """
        Test poziv 'endpoint_svi_kupci' sa autorizovanim Korisnikom.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Obican Korisnik sa autorizacijom.
        @return status code 200: OK
        """

        url_svi_stanovi = reverse('stanovi:lista_stanova')

        response = client.get(url_svi_stanovi)

        assert response.status_code == 200

    # TODO: (IVANA) OVE PUTANJE TREBA TESTIRATI.
    """
    # Broj Ponuda za Stan po mesecima
    path('ponude-stana-meseci/<int:id_stana>', BrojPonudaStanovaPoMesecimaAPIView.as_view(), name='ponude-stana-meseci'),
    # Lista svih mesecnih cena kvadrata
    path('listing-cena-kvadrata', AzuriranjeCenaStanaAPIView.as_view(), name='kreiraj-cenu-kvadrata'),
    # Kreiranje mesecne cene kvadrata
    path('kreiraj-cenu-kvadrata', AzuriranjeCenaCreateAPIView.as_view(), name='kreiraj-cenu-kvadrata'),
    # Promena mesecne cene kvadrata
    path('promeni-cenu-kvadrata/<int:id_azur_cene>', AzuriranjeCenaUpdateAPIView.as_view(), name='promeni-cenu-kvadrata'),
    # Brisanje mesecne cene kvadrata
    path('izbrisi-cenu-kvadrata/<int:id_azur_cene>', AzuriranjeCenaDeleteAPIView.as_view(), name='izbrisi-cenu-kvadrata')
    """

    def test_lista_svih_stanova_url_autorizovan_korisnik(self, client, novi_autorizovan_korisnik_fixture_stanovi):
        """
        Test poziv 'lista_stanova' sa autorizovanim Korisnikom.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Autorizovan Korisnik .
        @return status code 200: OK
        """

        url_svi_stanovi = reverse('stanovi:lista_stanova')

        response = client.get(url_svi_stanovi)

        assert response.status_code == 200  # (HTTP) 200 Authorized.

    def test_lista_svih_stanova_url_neautorizovan_korisnik(self, client, novi_korisnik_neautorizovan_fixture_stanovi):
        """
        Test poziv 'lista_stanova' sa neautorizovanim Korisnikom ((HTTP) 401 Unauthorized).

        * @see conftest.py (novi_korisnik_neautorizovan_fixture_stanovi)

        @param client: A Django test client instance.
        @param novi_korisnik_neautorizovan_fixture_stanovi: Obican Korisnik bez autorizacie.
        @return status code 401:  Unauthorized
        """

        url_svi_stanovi = reverse('stanovi:lista_stanova')

        response = client.get(url_svi_stanovi)

        assert response.status_code == 401  # (HTTP) 401 Unauthorized.

    def test_kreiraj_stan(self, client, novi_autorizovan_korisnik_fixture_stanovi, kreiraj_auriranje_cena):
        """
        Test poziv 'stanovi:kreiraj_stan' za API poziv Kreiranje Stanova sa autorizovanim Korisnikom.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (kreiraj_auriranje_cena)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Obican Korisnik sa autorizacijom.
        @return status code 201:  HTTP 201 CREATED
        """

        url_kreiraj_stan = reverse('stanovi:kreiraj_stan')

        novi_stan = json.dumps(
            {'id_stana': 3,
             'lamela': "L4.1.S2",
             'adresa_stana': "Adresa Stana L3.1.S2",
             'kvadratura': '48.02',
             'kvadratura_korekcija': 46.58,
             'iznos_za_korekciju_kvadrature': '0.97',
             'sprat': "1.0",
             'broj_soba': 2,
             'orijentisanost': "Jug",
             'broj_terasa': 0,
             'cena_stana': "73036.50",
             'cena_kvadrata': "1568.00",
             'napomena': 'Nema napomene',
             'status_prodaje': "dostupan"}
        )

        response = client.post(url_kreiraj_stan, data=novi_stan, content_type='application/json')

        assert response.status_code == 201

    def test_detalji_stana(self, client, novi_autorizovan_korisnik_fixture_stanovi,
                           novi_jedan_stan_fixture):  # puca zbog racunanja iz modela
        """
        Test poziv 'stanovi:detalji_stana' za API poziv Detalja Stana sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (novi_jedan_stan_fixture)

        @param client: A Django test client instance.
        @param novi_jedan_stan_fixture: Stanovi.
        @param novi_autorizovan_korisnik_fixture_stanovi: Obican Korisnik sa autorizacijom.
        @return status code 200: HTTP OK
        """

        detalji_stana_model = Stanovi.objects.all().values()
        print("############################################")
        print(f'STANO MODEL DATA {detalji_stana_model}')
        print("############################################")

        url_detalji_stana = reverse('stanovi:detalji_stana', args=[novi_jedan_stan_fixture.id_stana])

        response = client.get(url_detalji_stana)

        assert response.status_code == 200

        print("############################################")
        print(f'RESPONSE:  {response.data}')
        print("############################################")

        assert response.json() == {
            "id_stana": novi_jedan_stan_fixture.id_stana,
            "lamela": novi_jedan_stan_fixture.lamela,
            "adresa_stana": novi_jedan_stan_fixture.adresa_stana,
            "kvadratura": novi_jedan_stan_fixture.kvadratura,
            "kvadratura_korekcija": novi_jedan_stan_fixture.kvadratura_korekcija,
            "iznos_za_korekciju_kvadrature": novi_jedan_stan_fixture.iznos_za_korekciju_kvadrature,
            "sprat": novi_jedan_stan_fixture.sprat,
            "broj_soba": novi_jedan_stan_fixture.broj_soba,
            "orijentisanost": novi_jedan_stan_fixture.orijentisanost,
            "broj_terasa": novi_jedan_stan_fixture.broj_terasa,
            "cena_stana": Decimal(novi_jedan_stan_fixture.cena_stana),
            "cena_kvadrata": Decimal(novi_jedan_stan_fixture.cena_kvadrata),
            "napomena": novi_jedan_stan_fixture.napomena,
            "status_prodaje": novi_jedan_stan_fixture.status_prodaje,
            "lista_ponuda_stana": [],
            "broj_ponuda_za_stan": 0,
            'detalji_stana_url': '/stanovi/detalji-stana/1',
            "izmeni_stan_url": '/stanovi/izmeni-stan/1',
            "obrisi_stan_url": "/stanovi/obrisi-stan/1",
            'kreiraj_stan_url': '/stanovi/kreiraj-stan',
        }

    def test_izmeni_stan(self, client, novi_autorizovan_korisnik_fixture_stanovi,
                         # puca jer vraca dva obj Azuriranje cena
                         novi_jedan_stan_fixture, novi_jedan_stan_json_fixture):
        """
        Test poziv 'stanovi:izmeni_stan' za API poziv Izmeni Stan sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (novi_jedan_stan_fixture)
            * @see conftest.py (novi_jedan_stan_json_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Korisnik.
        @param novi_jedan_stan_fixture: Stanovi.
        @param novi_jedan_stan_json_fixture: Stanovi.
        @return status code 200: HTTP OK
        """

        url_izmeni_stan = reverse('stanovi:izmeni_stan', args=[novi_jedan_stan_fixture.id_stana])

        response = client.put(url_izmeni_stan, data=novi_jedan_stan_json_fixture, content_type='application/json')

        assert response.status_code == 200

        assert response.json()["lamela"] != novi_jedan_stan_fixture.lamela
        assert response.json()["adresa_stana"] != novi_jedan_stan_fixture.adresa_stana
        assert response.json()["kvadratura"] == novi_jedan_stan_fixture.kvadratura
        assert response.json()["kvadratura_korekcija"] == novi_jedan_stan_fixture.kvadratura_korekcija
        assert response.json()["iznos_za_korekciju_kvadrature"] == \
               novi_jedan_stan_fixture.iznos_za_korekciju_kvadrature
        assert response.json()["sprat"] == novi_jedan_stan_fixture.sprat
        assert response.json()["broj_soba"] != novi_jedan_stan_fixture.broj_soba
        assert response.json()["orijentisanost"] == novi_jedan_stan_fixture.orijentisanost
        assert response.json()["broj_terasa"] != novi_jedan_stan_fixture.broj_terasa
        assert response.json()["cena_stana"] == novi_jedan_stan_fixture.cena_stana
        assert response.json()["cena_kvadrata"] == novi_jedan_stan_fixture.cena_kvadrata
        assert response.json()["napomena"] == novi_jedan_stan_fixture.napomena
        assert response.json()["status_prodaje"] == novi_jedan_stan_fixture.status_prodaje

    def test_obrisi_stan(self, client, novi_autorizovan_korisnik_fixture_stanovi, novi_jedan_stan_fixture):
        """
        Test poziv 'stanovi:obrisi_stan' za API poziv Obrisi Stan sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (novi_jedan_stan_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Korisnik.
        @param novi_jedan_stan_fixture: Stanovi (Stan).
        @return status code 204: HTTP No Content
        """

        # Proveriti prvo da li je ID stana iz fixtura 'id_stana'
        assert novi_jedan_stan_fixture.id_stana == novi_jedan_stan_fixture.id_stana

        url_obrisi_stan = reverse('stanovi:obrisi_stan', args=[novi_jedan_stan_fixture.id_stana])
        print(f'REVERSE URLs: {url_obrisi_stan}')

        response = client.delete(url_obrisi_stan)

        assert response.status_code == 204

        # Proveri koliko je stanova u bazi (treba da ima 0 stanova)
        broj_stanova_u_bazi = Stanovi.objects.all().count()
        assert broj_stanova_u_bazi == 0

    def test_lista_svih_mesecnih_cena_kvadrata(self, novi_autorizovan_korisnik_fixture_stanovi):
        pass
