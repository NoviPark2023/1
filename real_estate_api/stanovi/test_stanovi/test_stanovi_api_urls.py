import ast
import json
from collections import Counter
from decimal import Decimal

from rest_framework.reverse import reverse

from real_estate_api.stanovi.models import Stanovi, AzuriranjeCena


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

    def test_kreiraj_stan(self, client, novi_autorizovan_korisnik_fixture_stanovi, kreiraj_tri_auriranja_cena_stanovi):
        """
        Test poziv 'stanovi:kreiraj_stan' za API poziv Kreiranje Stanova sa autorizovanim Korisnikom.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (kreiraj_tri_auriranja_cena_stanovi)

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
                           novi_jedan_stan_fixture_stanovi):
        """
        Test poziv 'stanovi:detalji_stana' za API poziv Detalja Stana sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (novi_jedan_stan_fixture)

        @param client: A Django test client instance.
        @param novi_jedan_stan_fixture_stanovi: Stanovi.
        @param novi_autorizovan_korisnik_fixture_stanovi: Obican Korisnik sa autorizacijom.
        @return status code 200: HTTP OK
        """

        url_detalji_stana = reverse('stanovi:detalji_stana', args=[novi_jedan_stan_fixture_stanovi.id_stana])

        response = client.get(url_detalji_stana)

        assert response.status_code == 200

        # Radimo konverziju poja u Decimal kompatibilne reprezentacije.
        # * str(round(Decimal(novi_jedan_stan_fixture_stanovi.kvadratura_korekcija), 2))
        # * str(round(Decimal(novi_jedan_stan_fixture_stanovi.cena_stana), 2))
        # * str(round(Decimal(novi_jedan_stan_fixture_stanovi.cena_kvadrata) ,2))
        assert response.json() == {
            "id_stana": novi_jedan_stan_fixture_stanovi.id_stana,
            "lamela": novi_jedan_stan_fixture_stanovi.lamela,
            "adresa_stana": novi_jedan_stan_fixture_stanovi.adresa_stana,
            "kvadratura": novi_jedan_stan_fixture_stanovi.kvadratura,
            "kvadratura_korekcija": str(round(Decimal(novi_jedan_stan_fixture_stanovi.kvadratura_korekcija), 2)),
            "iznos_za_korekciju_kvadrature": novi_jedan_stan_fixture_stanovi.iznos_za_korekciju_kvadrature,
            "sprat": novi_jedan_stan_fixture_stanovi.sprat,
            "broj_soba": novi_jedan_stan_fixture_stanovi.broj_soba,
            "orijentisanost": novi_jedan_stan_fixture_stanovi.orijentisanost,
            "broj_terasa": novi_jedan_stan_fixture_stanovi.broj_terasa,
            "cena_stana": str(round(Decimal(novi_jedan_stan_fixture_stanovi.cena_stana), 2)),
            "cena_kvadrata": str(round(Decimal(novi_jedan_stan_fixture_stanovi.cena_kvadrata), 2)),
            "napomena": novi_jedan_stan_fixture_stanovi.napomena,
            "status_prodaje": novi_jedan_stan_fixture_stanovi.status_prodaje,
            "lista_ponuda_stana": [],
            "broj_ponuda_za_stan": 0,
            'detalji_stana_url': '/stanovi/detalji-stana/1',
            "izmeni_stan_url": '/stanovi/izmeni-stan/1',
            "obrisi_stan_url": "/stanovi/obrisi-stan/1",
            'kreiraj_stan_url': '/stanovi/kreiraj-stan',
        }

    def test_izmeni_stan(self,
                         client,
                         novi_autorizovan_korisnik_fixture_stanovi,
                         novi_jedan_stan_fixture_stanovi,
                         novi_jedan_stan_json_fixture):
        """
        Test poziv 'stanovi:izmeni_stan' za API poziv Izmeni Stan sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (novi_jedan_stan_fixture)
            * @see conftest.py (novi_jedan_stan_json_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Korisnik.
        @param novi_jedan_stan_fixture_stanovi: Stanovi.
        @param novi_jedan_stan_json_fixture: Stanovi.
        @return status code 200: HTTP OK
        """

        url_izmeni_stan = reverse('stanovi:izmeni_stan', args=[novi_jedan_stan_fixture_stanovi.id_stana])

        response = client.put(url_izmeni_stan, data=novi_jedan_stan_json_fixture, content_type='application/json')

        assert response.status_code == 200

        assert response.json()["lamela"] != novi_jedan_stan_fixture_stanovi.lamela
        assert response.json()["adresa_stana"] != novi_jedan_stan_fixture_stanovi.adresa_stana
        assert response.json()["kvadratura"] == novi_jedan_stan_fixture_stanovi.kvadratura
        assert response.json()["kvadratura_korekcija"] == (
            str(round(Decimal(novi_jedan_stan_fixture_stanovi.kvadratura_korekcija), 2))
        )
        assert response.json()["iznos_za_korekciju_kvadrature"] == (
            novi_jedan_stan_fixture_stanovi.iznos_za_korekciju_kvadrature
        )
        assert response.json()["sprat"] == novi_jedan_stan_fixture_stanovi.sprat
        assert response.json()["broj_soba"] == novi_jedan_stan_fixture_stanovi.broj_soba
        assert response.json()["orijentisanost"] == novi_jedan_stan_fixture_stanovi.orijentisanost
        assert response.json()["broj_terasa"] != novi_jedan_stan_fixture_stanovi.broj_terasa
        assert response.json()["cena_stana"] == str(round(Decimal(novi_jedan_stan_fixture_stanovi.cena_stana), 2))
        assert response.json()["cena_kvadrata"] == str(round(Decimal(novi_jedan_stan_fixture_stanovi.cena_kvadrata), 2))
        assert response.json()["napomena"] == novi_jedan_stan_fixture_stanovi.napomena
        assert response.json()["status_prodaje"] == novi_jedan_stan_fixture_stanovi.status_prodaje

    def test_obrisi_stan(self,
                         client,
                         novi_jedan_stan_fixture_stanovi,
                         novi_autorizovan_korisnik_fixture_stanovi
                         ):
        """
        Test poziv 'stanovi:obrisi_stan' za API poziv Obrisi Stan sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (novi_jedan_stan_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Korisnik.
        @param novi_jedan_stan_fixture_stanovi: Stanovi (Stan).
        @return status code 204: HTTP No Content
        """

        url_obrisi_stan = reverse('stanovi:obrisi_stan', args=[novi_jedan_stan_fixture_stanovi.id_stana])

        response = client.delete(url_obrisi_stan)

        assert response.status_code == 204

        # Proveri koliko je stanova u bazi (treba da ima 0 stanova)
        broj_stanova_u_bazi = Stanovi.objects.all().count()
        assert broj_stanova_u_bazi == 0

    def test_lista_svih_mesecnih_cena_kvadrata(self,
                                               client,
                                               novi_autorizovan_korisnik_fixture_stanovi,
                                               kreiraj_tri_auriranja_cena_stanovi):
        """
        Test poziv 'stanovi:kreiraj-cenu-kvadrata' sa autorizovanim Korisnikom.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Autorizovan Korisnik .
        @return status code 200: OK
        """

        broj_azuriranja_cena = AzuriranjeCena.objects.all().count()
        assert broj_azuriranja_cena == 3

        url_sve_mesecne_cene_kvadrata = reverse('stanovi:lista-cena-kvadrata')

        response = client.get(url_sve_mesecne_cene_kvadrata)
        print(f'RESPONSE LISTA AZURIRANJA CENA: {response.data}')

        assert response.status_code == 200  # (HTTP) 200 Authorized.

    def test_kreiranje_mesecne_cene_kvadrata(self, client, novi_autorizovan_korisnik_fixture_stanovi):
        """
        Test poziv 'stanovi:kreiraj-cenu-kvadrata' za API poziv Kreiranje mesecne cene kvadrata sa autorizovanim Korisnikom.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Obican Korisnik sa autorizacijom.
        @return status code 201:  HTTP 201 CREATED
        """

        url_kreiraj_mesecnu_cenu_kvadrata = reverse('stanovi:kreiraj-cenu-kvadrata')

        nove_cene = json.dumps(
            {'id_azur_cene': 1,
             'sprat': "1.0",
             'broj_soba': 2,
             'orijentisanost': "Jug",
             'cena_kvadrata': 1568.00}
        )

        response = client.post(url_kreiraj_mesecnu_cenu_kvadrata, data=nove_cene, content_type='application/json')

        assert response.status_code == 201

    def test_promena_mesecne_cene_kvadrata(self, client,
                                           novi_autorizovan_korisnik_fixture_stanovi,
                                           novo_azuriranje_cena_fixture,
                                           novo_azuriranje_cena_json_fixture):
        """
        Test poziv 'stanovi:promeni-cenu-kvadrata' za API poziv Mesecna izmena
        cene kvadrata po id-ju sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (novo_azuriranje_cena_fixture)
            * @see conftest.py (novo_azuriranje_cena_json_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Korisnik.
        @param novo_azuriranje_cena_fixture: AzuriranjeCena.
        @param novo_azuriranje_cena_json_fixture: AzuriranjeCena.
        @return status code 200: HTTP OK
        """
        url_izmeni_mesecne_cene_kvadrata = reverse('stanovi:promeni-cenu-kvadrata',
                                                   args=[novo_azuriranje_cena_fixture.id_azur_cene])

        response = client.put(url_izmeni_mesecne_cene_kvadrata,
                              data=novo_azuriranje_cena_json_fixture,
                              content_type='application/json')

        assert response.status_code == 200

        assert response.json()["sprat"] != novo_azuriranje_cena_fixture.sprat
        assert response.json()["broj_soba"] != novo_azuriranje_cena_fixture.broj_soba
        assert response.json()["orijentisanost"] == novo_azuriranje_cena_fixture.orijentisanost
        assert response.json()["cena_kvadrata"] != novo_azuriranje_cena_fixture.cena_kvadrata

    def test_brisanje_mesecne_cene_kvadrata(self, client,
                                            novi_autorizovan_korisnik_fixture_stanovi,
                                            novo_azuriranje_cena_fixture):
        """
        Test poziv 'stanovi:izbrisi-cenu-kvadrata' za API poziv Brisanje cena kvadrata po id-ju sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
            * @see conftest.py (novo_azuriranje_cena_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Korisnik.
        @param novo_azuriranje_cena_fixture: AzuriranjeCena.
        @return status code 204: HTTP No Content
        """
        url_obrisi_cenu_kvadrata = reverse('stanovi:izbrisi-cenu-kvadrata',
                                           args=[novo_azuriranje_cena_fixture.id_azur_cene])

        response = client.delete(url_obrisi_cenu_kvadrata)

        assert response.status_code == 204

        # Proveri koliko je azuriranja cena u bazi (treba da ima 0)
        broj_azuriranja_cena_u_bazi = AzuriranjeCena.objects.all().count()
        assert broj_azuriranja_cena_u_bazi == 0

    def test_broj_ponuda_za_stan_po_mesecima(self, client,
                                             novi_autorizovan_korisnik_fixture_stanovi,
                                             novi_jedan_stan_fixture_stanovi):
        """
        Test poziv 'ponude-stana-meseci' sa autorizovanim Korisnikom. Provera broja
        ponuda koji ima jedan Stan po mesecima.
        - ast.literal_eval(built-in) to convert a String representation of a Dictionary to a dictionary.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_stanovi)
        * @see conftest.py (novi_jedan_stan_fixture_stanovi)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_stanovi: Autorizovan Korisnik.
        @param novi_jedan_stan_fixture_stanovi: Stanovi (Stan).
        @return status code 200: OK
        """
        url_sve_mesecne_ponude_za_stan = reverse('stanovi:ponude-stana-meseci',
                                                 args=[novi_jedan_stan_fixture_stanovi.id_stana])

        response = client.get(url_sve_mesecne_ponude_za_stan)

        ponude_str = json.dumps(response.data["broj_ponuda_po_mesecima"])
        ponude = ast.literal_eval(ponude_str)
        dct = Counter()
        for d in ponude:
            for k, v in d.items():
                dct[k] += v

        print(dct)
        print(sum(dct.values()))

        assert response.status_code == 200  # (HTTP) 200 OK.
