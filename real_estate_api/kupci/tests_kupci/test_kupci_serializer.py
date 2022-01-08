import json

from rest_framework.reverse import reverse

from real_estate_api.kupci.models import Kupci


class TestKupciSerijalizers:

    def test_serializers_svi_kupci(self, client, nova_dva_kupaca_fixture, novi_autorizovan_korisnik_fixture):
        """
        Testiranje serijalizera za pregled svih Klijenata(Kupaca) sa fixturom od dva kreirana nova Kupca.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (nova_dva_kupaca_fixture)

        @param client: A Django test client instance.
        @param nova_dva_kupaca_fixture: Kupci
        @param novi_autorizovan_korisnik_fixture: Korisnik
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

    def test_serializers_detalji_jednog_kupca(self,
                                              client,
                                              nova_dva_kupaca_fixture,
                                              novi_autorizovan_korisnik_fixture
                                              ):
        """
        Testiranje serijalizera za pregled deatalja Klijenata(Kupaca) sa fixturom od dva kreirana nova Kupca.
        Testiranje se vrsi sa autorizovanim Korisnikom sistema.

            * @see conftest.py (novi_autorizovan_korisnik_fixture)
            * @see conftest.py (nova_dva_kupaca_fixture)

        @param client: A Django test client instance.
        @param nova_dva_kupaca_fixture: Kupci
        @param novi_autorizovan_korisnik_fixture: Korisnik
        """

        # First check how many Kupcaca in DB is *(should be 2)
        broj_kupaca = Kupci.objects.all().count()
        assert broj_kupaca == 2

        # Get valid one Kupaca from Response
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

    def test_serializers_kreiraj_jednog_kupca(self,
                                              client,
                                              nova_dva_kupaca_fixture,
                                              novi_autorizovan_korisnik_fixture
                                              ):
        # TODO: test_serializers_kreiraj_jednog_kupca *(POST)
        # #see https://realpython.com/test-driven-development-of-a-django-restful-api/
        pass

    def test_serializers_izmeni_jednog_kupca(self,
                                             client,
                                             nova_dva_kupaca_fixture,
                                             novi_autorizovan_korisnik_fixture
                                             ):
        # TODO: test_serializers_izmeni_jednog_kupca *(PUT)
        # #see https://realpython.com/test-driven-development-of-a-django-restful-api/
        pass

    def test_serializers_obrisi_jednog_kupca(self,
                                             client,
                                             nova_dva_kupaca_fixture,
                                             novi_autorizovan_korisnik_fixture
                                             ):
        # TODO: test_serializers_obrisi_jednog_kupca *(DELETE)
        # #see https://realpython.com/test-driven-development-of-a-django-restful-api/
        pass
