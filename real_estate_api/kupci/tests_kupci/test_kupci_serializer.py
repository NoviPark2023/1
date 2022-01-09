import json

from rest_framework.reverse import reverse

from conftest import fake
from real_estate_api.kupci.models import Kupci


class TestKupciSerijalizers:

    def test_serializers_svi_kupci(self, client, nova_dva_kupaca_fixture, novi_autorizovan_korisnik_fixture_kupci):
        """
        Testiranje serijalizera za pregled svih Klijenata(Kupaca) sa fixturom od dva kreirana nova Kupca.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (nova_dva_kupaca_fixture)

        @param client: A Django test client instance.
        @param nova_dva_kupaca_fixture: Kupci
        @param novi_autorizovan_korisnik_fixture_kupci: Korisnik
        """

        response = client.get(reverse('kupci:lista_kupaca'))
        print(f'RESPONSE: {response}')
        print(f'RESPONSE CONTENT: {response.json()}')

        kupci = Kupci.objects.all().order_by('id_kupca')
        kupci_broj = Kupci.objects.all().count()

        # Lokalno import 'KupciSerializer'.
        from real_estate_api.kupci.serializers import KupciSerializer

        serializer = KupciSerializer(kupci, many=True)

        print(f'RESPONSE DATA: {json.dumps(serializer.data)}')
        print(f'RESPONSE DATA: {json.dumps(response.json()["results"])}')

        assert json.dumps(serializer.data) == json.dumps(response.json()["results"])
        assert response.status_code == 200
        assert kupci_broj == 2

    def test_valid_serializers_detalji_jednog_kupca(self,
                                                    client,
                                                    nova_dva_kupaca_fixture,
                                                    novi_autorizovan_korisnik_fixture_kupci
                                                    ):
        """
        Testiranje serijalizera za pregled deatalja Klijenata(Kupaca) sa fixturom od dva kreirana nova Kupca.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (nova_dva_kupaca_fixture)

        @param client: A Django test client instance.
        @param nova_dva_kupaca_fixture: Kupci
        @param novi_autorizovan_korisnik_fixture_kupci: Korisnik
        """

        # First check how many Kupcaca in DB is *(should be 2)
        broj_kupaca = Kupci.objects.all().count()
        assert broj_kupaca == 2

        # Get valid two Kupaca from Response
        url_detalji_kupca_jedan = reverse('kupci:detalji_kupca', args=[nova_dva_kupaca_fixture[0].id_kupca])
        url_detalji_kupca_dva = reverse('kupci:detalji_kupca', args=[nova_dva_kupaca_fixture[1].id_kupca])

        response_kupac_jedan = client.get(url_detalji_kupca_jedan)
        response_kupac_dva = client.get(url_detalji_kupca_dva)

        kupac_jedan_from_response = Kupci.objects.get(id_kupca=nova_dva_kupaca_fixture[0].id_kupca)
        kupac_dva_from_response = Kupci.objects.get(id_kupca=nova_dva_kupaca_fixture[1].id_kupca)

        print(f'KUPAC ONE FROM RESPONSE: {kupac_jedan_from_response}')
        print(f'KUPAC TWO FROM RESPONSE: {kupac_dva_from_response}')

        # Lokalno import 'KupciSerializer'.
        from real_estate_api.kupci.serializers import KupciSerializer

        serializer_kupac_one = KupciSerializer(kupac_jedan_from_response)
        serializer_kupac_two = KupciSerializer(kupac_dva_from_response)

        assert json.dumps(serializer_kupac_one.data) == json.dumps(response_kupac_jedan.json())
        assert json.dumps(serializer_kupac_two.data) == json.dumps(response_kupac_dva.json())

    def test_invalid_serializers_detalji_jednog_kupca(self,
                                                      client,
                                                      nova_dva_kupaca_fixture,
                                                      novi_autorizovan_korisnik_fixture_kupci
                                                      ):
        """
        Testiranje serijalizera za pregled deatalja Klijenata(Kupaca) koji ne postoji
        sa fixturom od dva kreirana nova Kupca.

        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (nova_dva_kupaca_fixture)

        @param client: A Django test client instance.
        @param nova_dva_kupaca_fixture: Kupci
        @param novi_autorizovan_korisnik_fixture_kupci: Korisnik
        """

        # Get invalid one Kupaca from Response
        url_detalji_kupca_jedan = reverse('kupci:detalji_kupca', args=[nova_dva_kupaca_fixture[0].id_kupca + 1000])
        response = client.get(url_detalji_kupca_jedan)
        assert response.status_code == 404

    def test_serializers_kreiraj_validnog_jednog_kupca(self,
                                                       client,
                                                       novi_autorizovan_korisnik_fixture_kupci
                                                       ):
        """
        Testiranje serijalizera za kreiranje Klijenata(Kupaca) koji je validan,
        sa fixturom od dva kreirana nova Kupca.

        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_kupci: Korisnik
        """
        url_kreiraj_validnog_kupca = reverse('kupci:kreiraj_kupca')

        # Podaci za izmenu Kupca
        test_novi_kupac = json.dumps(
            {
                "lice": "Pravno",
                "ime_prezime": fake.name(),
                "email": fake.email(),
                "broj_telefona": "+381 63 136 90 988",
                "Jmbg_Pib": "0102030605",
                "adresa": "Milenke Dravica 54"
            }
        )

        response = client.post(url_kreiraj_validnog_kupca, data=test_novi_kupac, content_type='application/json')

        assert response.status_code == 201

    def test_serializers_kreiraj_nevalidnog_jednog_kupca(self,
                                                         client,
                                                         novi_autorizovan_korisnik_fixture_kupci
                                                         ):
        """
        Testiranje serijalizera za kreiranje Klijenata(Kupaca) koji je nije validan *(status.HTTP_400_BAD_REQUEST),
        sa fixturom od dva kreirana nova Kupca.

        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_kupci: Korisnik
        """
        url_kreiraj_validnog_kupca = reverse('kupci:kreiraj_kupca')

        # Podaci za izmenu Kupca
        test_novi_kupac = json.dumps(
            {
                "lice_ne_validno": "Pravno",
                "ime_prezime_ne_validno": fake.name(),
                "email_ne_validno": fake.email(),
                "broj_telefona_ne_validno": "+381 63 136 90 988",
                "Jmbg_Pib_ne_validno": "0102030605",
                "adresa_ne_validno": "Milenke Dravica 54"
            }
        )

        response = client.post(url_kreiraj_validnog_kupca, data=test_novi_kupac, content_type='application/json')

        assert response.status_code == 400

    def test_serializers_kreiraj_validnog_jednog_kupca_401(self, client):
        """
        Testiranje serijalizera za kreiranje Klijenata(Kupaca) koji je validan,
        sa fixturom od dva kreirana nova Kupca ali nije autorizovan.


        @param client: A Django test client instance.
        """
        url_kreiraj_validnog_kupca = reverse('kupci:kreiraj_kupca')

        # Podaci za izmenu Kupca
        test_novi_kupac = json.dumps(
            {
                "lice": "Pravno",
                "ime_prezime": fake.name(),
                "email": fake.email(),
                "broj_telefona": "+381 63 136 90 988",
                "Jmbg_Pib": "0102030605",
                "adresa": "Milenke Dravica 54"
            }
        )

        response = client.post(url_kreiraj_validnog_kupca, data=test_novi_kupac, content_type='application/json')

        assert response.status_code == 401

    def test_serializers_izmeni_jednog_kupca_validan(self,
                                                     client,
                                                     novi_kupac_fixture,
                                                     novi_autorizovan_korisnik_fixture_kupci
                                                     ):
        """
        Test poziv 'kupci:izmeni_kupca' za API poziv Izmeni Kupca *(VALIDAN) sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (novi_kupac_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_kupci: Korisnik.
        @param novi_kupac_fixture: Klijent (Kupac).
        """

        # Podaci za izmenu Kupca
        test_novi_kupac = json.dumps(
            {
                "lice": "Pravno",
                "ime_prezime": fake.name(),
                "email": fake.email(),
                "broj_telefona": "+381 63 136 90 988",
                "Jmbg_Pib": "0102030605",
                "adresa": "Milenke Dravica 54"
            }
        )

        url_izmeni_kupca = reverse('kupci:izmeni_kupca', args=[novi_kupac_fixture.id_kupca])

        response = client.put(url_izmeni_kupca, data=test_novi_kupac, content_type='application/json')

        assert response.status_code == 200

    def test_serializers_izmeni_jednog_kupca_nije_validan(self,
                                                          client,
                                                          novi_kupac_fixture,
                                                          novi_autorizovan_korisnik_fixture_kupci
                                                          ):
        """
        Test poziv 'kupci:izmeni_kupca' za API poziv Izmeni Kupca *(NIJE VALIDAN) sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (novi_kupac_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_kupci: Korisnik.
        @param novi_kupac_fixture: Klijent (Kupac).
        """

        # Podaci za izmenu Kupca
        test_novi_kupac = json.dumps(
            {
                "lice_ne_validno": "Pravno",
                "ime_prezime_ne_validno": fake.name(),
                "email_ne_validno": fake.email(),
                "broj_telefona_ne_validno": "+381 63 136 90 988",
                "Jmbg_Pib_ne_validno": "0102030605",
                "adresa_ne_validno": "Milenke Dravica 54"
            }
        )

        url_izmeni_kupca = reverse('kupci:izmeni_kupca', args=[novi_kupac_fixture.id_kupca])

        response = client.put(url_izmeni_kupca, data=test_novi_kupac, content_type='application/json')

        assert response.status_code == 400

    def test_serializers_obrisi_jednog_kupca_validan(self,
                                                     client,
                                                     novi_kupac_fixture,
                                                     novi_autorizovan_korisnik_fixture_kupci
                                                     ):
        """
        Test poziv 'kupci:obrisi_kupca' za API poziv Obrisi Kupca *(VALIDAN) sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (novi_kupac_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_kupci: Korisnik.
        @param novi_kupac_fixture: Klijent (Kupac).
        """

        url_delete_kupca = reverse('kupci:obrisi_kupca', args=[novi_kupac_fixture.id_kupca])

        response = client.delete(url_delete_kupca)

        # HTTP 204 No Content success status
        assert response.status_code == 204

    def test_serializers_obrisi_jednog_kupca_nije_validan(self,
                                                          client,
                                                          novi_kupac_fixture,
                                                          novi_autorizovan_korisnik_fixture_kupci
                                                          ):
        """
        Test poziv 'kupci:obrisi_kupca' za API poziv Obrisi Kupca *(NIJE VALIDAN) sa autorizovanim Korisnikom.
        Takodje se proverava i Response sadrzaj.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (novi_kupac_fixture)

        @param client: A Django test client instance.
        @param novi_autorizovan_korisnik_fixture_kupci: Korisnik.
        @param novi_kupac_fixture: Klijent (Kupac).
        """

        url_delete_kupca = reverse('kupci:obrisi_kupca', args=[novi_kupac_fixture.id_kupca + 1000])

        response = client.delete(url_delete_kupca)

        # HTTP 404 Not Found
        assert response.status_code == 404
