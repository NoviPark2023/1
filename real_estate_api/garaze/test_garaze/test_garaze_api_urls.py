from rest_framework.reverse import reverse
from rest_framework.utils import json

from real_estate_api.garaze.models import Garaze


class TestRestApiUrlsGaraze:
    """Testitanje API URLs Endpointa entiteta Garaze"""

    def test_sa_neautorizovanim_korisnikom(self, client):
        """
        Test poziv 'endpoint_sve_garaze' sa neautorizovanim Korisnikom.

        @param client: A Django test client instance.
        @return status code 401: Unauthorized
        """
        url_sve_garaze = reverse('garaze:lista_garaza')

        response = client.get(url_sve_garaze)

        assert response.status_code == 401

    def test_sa_autorizovanim_korisnikom(self, client, novi_autorizovan_korisnik_fixture_garaze):
        """
        Test poziv 'endpoint_sve_garaze' sa autorizovanim Korisnikom.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_garaze)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_garaze: Obican Korisnik sa autorizacijom.
        @return status code 200: OK
        """
        url_sve_garaze = reverse('garaze:lista_garaza')

        response = client.get(url_sve_garaze)

        assert response.status_code == 200

    def test_lista_svih_garaza_url_autorizovan_korisnik(self,
                                                        client,
                                                        novi_autorizovan_korisnik_fixture_garaze,
                                                        nova_jedna_garaza_fixture
                                                        ):
        """
        Test poziv 'lista_garaza' sa autorizovanim Korisnikom.

        * @see conftest.py (novi_autorizovan_korisnik_fixture_garaze)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_garaze: Autorizovan Korisnik.
        @return status code 200: OK
        """

        broj_garaza_u_bazi = Garaze.objects.all().count()

        assert broj_garaza_u_bazi == 1

        url_sve_garaze = reverse('garaze:lista_garaza')

        response = client.get(url_sve_garaze)

        assert response.status_code == 200  # (HTTP) 200 Authorized.

    def test_lista_svih_garaza_url_neautorizovan_korisnik(self,
                                                          client,
                                                          novi_korisnik_neautorizovan_fixture_garaze
                                                          ):
        """
        Test poziv 'lista_garaza' sa neautorizovanim Korisnikom ((HTTP) 401 Unauthorized).

        * @see conftest.py (novi_korisnik_neautorizovan_fixture_garaze)

        @param client: A Django test client instance.
        @param novi_korisnik_neautorizovan_fixture_garaze: Obican Korisnik bez autorizacie.
        @return status code 401:  Unauthorized
        """
        url_sve_garaze = reverse('garaze:lista_garaza')

        response = client.get(url_sve_garaze)

        assert response.status_code == 401  # (HTTP) 401 Unauthorized.

    def test_kreiraj_garazu(self,
                            client,
                            novi_autorizovan_korisnik_fixture_garaze,
                            nova_jedna_garaza_json_fixture
                            ):
        """
        Test poziv 'garaze:kreiraj_garazu' za API poziv Kreiranje Garaza sa autorizovanim Korisnikom.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_garaze)
            * @see conftest.py (nova_jedna_garaza_json_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_garaze: Autorizovan Korisnik.
        @param nova_jedna_garaza_json_fixture: Garaze.
        @return status code 201:  HTTP 201 CREATED
        """

        # Proveriti da li je DB prazna, tj. nema ni jedne Garaze.
        broj_ponuda_garaza_from_db = Garaze.objects.all().count()
        assert broj_ponuda_garaza_from_db == 0

        url_kreiraj_garazu = reverse('garaze:kreiraj_garazu')

        response = client.post(url_kreiraj_garazu, data=nova_jedna_garaza_json_fixture, content_type='application/json')

        assert response.status_code == 201

        # Nakon kreiranja Garaze, proveriti koliko ih ima u db, treba da bude 1.
        broj_ponuda_garaza_from_db = Garaze.objects.all().count()
        assert broj_ponuda_garaza_from_db == 1

    def test_detalji_garaze(self, client,
                            novi_autorizovan_korisnik_fixture_garaze,
                            nova_jedna_garaza_fixture):
        """
        Test poziv 'garaze:detalji_garaze' za API poziv Detalja Garaze sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_garaze)
            * @see conftest.py (nova_jedna_garaza_fixture)

        @param client: A Django test client instance.
        @param nova_jedna_garaza_fixture: Garaze.
        @param novi_autorizovan_korisnik_fixture_garaze: Obican Korisnik sa autorizacijom.
        @return status code 200: HTTP OK
        """
        url_detalji_garaze = reverse('garaze:detalji_garaze', args=[nova_jedna_garaza_fixture.id_garaze])

        response = client.get(url_detalji_garaze)

        assert response.status_code == 200

        assert response.json() == {
            "id_garaze": nova_jedna_garaza_fixture.id_garaze,
            "ime_kupca": nova_jedna_garaza_fixture.ime_kupca,
            "jedinstveni_broj_garaze": nova_jedna_garaza_fixture.jedinstveni_broj_garaze,
            "kupac": nova_jedna_garaza_fixture.kupac.id_kupca,
            "cena_garaze": nova_jedna_garaza_fixture.cena_garaze,
            "datum_ugovora_garaze": '05.02.2022',
            "broj_ugovora_garaze": "123",
            "napomena_garaze": nova_jedna_garaza_fixture.napomena_garaze,
            "status_prodaje_garaze": nova_jedna_garaza_fixture.status_prodaje_garaze,
            "nacin_placanja_garaze": nova_jedna_garaza_fixture.nacin_placanja_garaze
        }

    def test_izmeni_garazu(self,
                           client,
                           novi_autorizovan_korisnik_fixture_garaze,
                           nova_jedna_garaza_fixture,
                           ):
        """
        Test poziv 'garaze:izmeni_garazu' za API poziv Izmeni Garazu sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_garaze)
            * @see conftest.py (nova_jedna_garaza_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_garaze: Korisnik.
        @param nova_jedna_garaza_fixture: Jedna Garaza Fixture.
        @return status code 200: HTTP OK
        """

        # Nova izmenjena Garaza .
        nova_garaza_izmenjena = json.dumps(
            {
                "id_garaze": 1,
                "jedinstveni_broj_garaze": 1,
                "cena_garaze": 6000.0,
                "datum_ugovora_garaze": '8.2.2022',
                "broj_ugovora_garaze": 'No5',
                "napomena_garaze": 'Nema napomene',
                "status_prodaje_garaze": "dostupna",
                "nacin_placanja_garaze": 'Kredit',
                "kupac": 1,
                "ime_kupca": 'Mihajlo Pupin'
            }
        )

        url_izmeni_garazu = reverse('garaze:izmeni_garazu', args=[nova_jedna_garaza_fixture.id_garaze])

        response = client.put(url_izmeni_garazu, data=nova_garaza_izmenjena, content_type='application/json')

        assert response.status_code == 200

        assert response.json()["id_garaze"] == nova_jedna_garaza_fixture.id_garaze
        assert response.json()["jedinstveni_broj_garaze"] != nova_jedna_garaza_fixture.jedinstveni_broj_garaze
        assert response.json()["cena_garaze"] != nova_jedna_garaza_fixture.cena_garaze
        assert response.json()["datum_ugovora_garaze"] != nova_jedna_garaza_fixture.datum_ugovora_garaze
        assert response.json()["broj_ugovora_garaze"] != nova_jedna_garaza_fixture.broj_ugovora_garaze
        assert response.json()["napomena_garaze"] == nova_jedna_garaza_fixture.napomena_garaze
        assert response.json()["status_prodaje_garaze"] == nova_jedna_garaza_fixture.status_prodaje_garaze
        assert response.json()["nacin_placanja_garaze"] == nova_jedna_garaza_fixture.nacin_placanja_garaze
        assert response.json()["kupac"] == nova_jedna_garaza_fixture.kupac.id_kupca
        assert response.json()["ime_kupca"] == nova_jedna_garaza_fixture.kupac.ime_prezime

    def test_obrisi_garazu(self,
                           client,
                           novi_autorizovan_korisnik_fixture_garaze,
                           nova_jedna_garaza_fixture):
        """
        Test poziv 'garaze:obrisi_garazu' za API poziv Obrisi Garazu sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture_garaze)
            * @see conftest.py (nova_jedna_garaza_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_garaze: Korisnik.
        @param nova_jedna_garaza_fixture: Garaze.
        @return status code 204: HTTP No Content
        """
        url_obrisi_garazu = reverse('garaze:obrisi_garazu', args=[nova_jedna_garaza_fixture.id_garaze])

        response = client.delete(url_obrisi_garazu)

        assert response.status_code == 204

        # Proveri koliko je garaza u bazi (treba da ima 0 garaza)
        broj_garaza_u_bazi = Garaze.objects.all().count()
        assert broj_garaza_u_bazi == 0
