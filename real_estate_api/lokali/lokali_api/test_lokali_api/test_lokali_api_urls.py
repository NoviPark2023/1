import json
import ast
from collections import Counter
from rest_framework.reverse import reverse

from real_estate_api.lokali.lokali_api.models import Lokali


class TestRestApiUrlsLokali:
    """Testitanje API URLs Endpointa entiteta Lokali"""

    def test_sa_neautorizovanim_korisnikom(self, client):
        """
        Test poziv 'endpoint_svi_lokali' sa neautorizovanim Korisnikom.

        * @see conftest.py (novi_neautorizovan_korisnik_fixture_lokali)

        @param client: A Django test client instance.
        @return status code 401: Unauthorized
        """
        url_svi_lokali = reverse('lokali:lista_lokala')

        response = client.get(url_svi_lokali)

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self, client, novi_autorizovan_korisnik_fixture_lokali):
        """
        Test poziv 'endpoint_svi_lokali' sa autorizovanim Korisnikom.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_lokali)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_lokali: Obican Korisnik sa autorizacijom.
        @return status code 200: OK
        """
        url_svi_lokali = reverse('lokali:lista_lokala')

        response = client.get(url_svi_lokali)

        assert response.status_code == 200

    def test_lista_svih_lokala_url_autorizovan_korisnik(self, client, novi_autorizovan_korisnik_fixture_lokali):
        """
        Test poziv 'lista_lokala' sa autorizovanim Korisnikom.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_lokali)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_lokali: Autorizovan Korisnik .
        @return status code 200: OK
        """
        url_svi_lokali = reverse('lokali:lista_lokala')

        response = client.get(url_svi_lokali)

        assert response.status_code == 200  # (HTTP) 200 Authorized.

    def test_lista_svih_lokala_url_neautorizovan_korisnik(self, client, novi_neautorizovan_korisnik_fixture_lokali):
        """
        Test poziv 'lista_lokala' sa neautorizovanim Korisnikom ((HTTP) 401 Unauthorized).

        * @see conftest.py (novi_neautorizovan_korisnik_fixture_lokali)

        @param client: A Django test client instance.
        @param novi_neautorizovan_korisnik_fixture_lokali: Obican Korisnik bez autorizacie.
        @return status code 401:  Unauthorized
        """
        url_svi_lokali = reverse('lokali:lista_lokala')

        response = client.get(url_svi_lokali)

        assert response.status_code == 401  # (HTTP) 401 Unauthorized.

    def test_kreiraj_lokal(self, client, novi_autorizovan_korisnik_fixture_lokali):
        """
        Test poziv 'lokali:kreiraj_lokal' za API poziv Kreiranje Lokala sa autorizovanim Korisnikom.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_lokali)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_lokali: Obican Korisnik sa autorizacijom.
        @return status code 201:  HTTP 201 CREATED
        """
        url_kreiraj_lokal = reverse('lokali:kreiraj_lokal')

        novi_lokal = json.dumps(
            {
                'id_lokala': 3,
                'lamela_lokala': "L2.0.P1",
                'adresa_lokala': "Adresa Lokala L2.0.P1",
                'kvadratura_lokala': "40.0",
                'kvadratura_korekcija': "0.0",
                'iznos_za_korekciju_kvadrature': "0.0",
                'broj_prostorija': "1.0",
                'napomena_lokala': "nema",
                'orijentisanost_lokala': "Jug",
                'status_prodaje_lokala': "dostupan",
                'cena_lokala': "40000",
                'cena_kvadrata_lokala': "1000.0"
            }
        )

        response = client.post(url_kreiraj_lokal, data=novi_lokal, content_type='application/json')

        assert response.status_code == 201

    def test_detalji_lokala(self,
                            client,
                            novi_autorizovan_korisnik_fixture_lokali,
                            novi_jedan_lokal_fixture,
                            ):
        """
        Test poziv 'lokali:detalji_lokala' za API poziv Detalja Lokala sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_lokali)
            * @see conftest.py (novi_jedan_lokal_fixture)

        @param client: A Django test client instance.
        @param novi_jedan_lokal_fixture: Lokali.
        @param novi_autorizovan_korisnik_fixture_lokali: Obican Korisnik sa autorizacijom.
        @return status code 200: HTTP OK
        """

        url_detalji_lokala = reverse('lokali:detalji_lokala', args=[novi_jedan_lokal_fixture.id_lokala])

        response = client.get(url_detalji_lokala)

        assert response.status_code == 200

        assert response.json() == {
            "id_lokala": novi_jedan_lokal_fixture.id_lokala,
            "lamela_lokala": novi_jedan_lokal_fixture.lamela_lokala,
            "adresa_lokala": novi_jedan_lokal_fixture.adresa_lokala,
            "kvadratura_lokala": novi_jedan_lokal_fixture.kvadratura_lokala,
            "broj_prostorija": novi_jedan_lokal_fixture.broj_prostorija,
            "napomena_lokala": novi_jedan_lokal_fixture.napomena_lokala,
            "orijentisanost_lokala": novi_jedan_lokal_fixture.orijentisanost_lokala,
            "status_prodaje_lokala": novi_jedan_lokal_fixture.status_prodaje_lokala,
            "cena_lokala": novi_jedan_lokal_fixture.cena_lokala,
            "lista_ponuda_lokala": [],
            "broj_ponuda_za_lokal": 0,
            "detalji_lokala_url": '/lokali/detalji-lokala/1/'
        }

    def test_izmeni_lokal(self,
                          client,
                          novi_autorizovan_korisnik_fixture_lokali,
                          novi_jedan_lokal_fixture,
                          novi_jedan_lokal_json_fixture):
        """
        Test poziv 'lokali:izmeni_lokal' za API poziv Izmeni Lokal sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_lokali)
            * @see conftest.py (novi_jedan_lokal_fixture)
            * @see conftest.py (novi_jedan_lokal_json_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_lokali: Korisnik.
        @param novi_jedan_lokal_fixture: Lokali.
        @param novi_jedan_lokal_json_fixture: Lokali.
        @return status code 200: HTTP OK
        """
        url_izmeni_lokal = reverse('lokali:izmeni_lokal', args=[novi_jedan_lokal_fixture.id_lokala])

        response = client.put(url_izmeni_lokal, data=novi_jedan_lokal_json_fixture, content_type='application/json')

        assert response.status_code == 200

        assert response.json()["lamela_lokala"] != novi_jedan_lokal_fixture.lamela_lokala
        assert response.json()["adresa_lokala"] != novi_jedan_lokal_fixture.adresa_lokala
        assert response.json()["kvadratura_lokala"] != novi_jedan_lokal_fixture.kvadratura_lokala
        assert response.json()["broj_prostorija"] == novi_jedan_lokal_fixture.broj_prostorija
        assert response.json()["napomena_lokala"] != novi_jedan_lokal_fixture.napomena_lokala
        assert response.json()["orijentisanost_lokala"] != novi_jedan_lokal_fixture.orijentisanost_lokala
        assert response.json()["status_prodaje_lokala"] == novi_jedan_lokal_fixture.status_prodaje_lokala
        assert response.json()["cena_lokala"] != novi_jedan_lokal_fixture.cena_lokala

    def test_obrisi_lokal(self,
                          client,
                          novi_jedan_lokal_fixture,
                          novi_autorizovan_korisnik_fixture_lokali):
        """
        Test poziv 'lokali:obrisi_lokal' za API poziv Obrisi Lokal sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_lokali)
            * @see conftest.py (novi_jedan_lokal_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_lokali: Korisnik.
        @param novi_jedan_lokal_fixture: Lokali.
        @return status code 204: HTTP No Content
        """
        url_obrisi_lokal = reverse('lokali:obrisi_lokal', args=[novi_jedan_lokal_fixture.id_lokala])

        response = client.delete(url_obrisi_lokal)

        assert response.status_code == 204

        # Provera koliko je lokala u bazi (treba da ih ima 0)
        broj_lokala_u_bazi = Lokali.objects.all().count()
        assert broj_lokala_u_bazi == 0

    def test_broj_ponuda_za_lokal_po_mesecima(self,
                                              client,
                                              novi_autorizovan_korisnik_fixture_lokali,
                                              novi_jedan_lokal_fixture
                                              ):
        """
        Test poziv 'ponude-lokala-meseci' sa autorizovanim Korisnikom. Provera broja
        ponuda koje ima jedan Lokal po mesecima.
        - ast.literal_eval(built-in) to convert a String representation of a Dictionary to a dictionary.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_lokali)
        * @see conftest.py (novi_jedan_lokal_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_lokali: Autorizovan Korisnik.
        @param novi_jedan_lokal_fixture: Lokali (Lokal).
        @return status code 200: OK
        """
        url_sve_mesecne_ponude_za_lokal = reverse('lokali:ponude-lokala-meseci',
                                                 args=[novi_jedan_lokal_fixture.id_lokala])

        response = client.get(url_sve_mesecne_ponude_za_lokal)

        ponude_str = json.dumps(response.data["broj_ponuda_po_mesecima"])
        ponude = ast.literal_eval(ponude_str)
        dct = Counter()
        for d in ponude:
            for k, v in d.items():
                dct[k] += v

        print(dct)
        print(sum(dct.values()))

        assert response.status_code == 200  # (HTTP) 200 OK.
