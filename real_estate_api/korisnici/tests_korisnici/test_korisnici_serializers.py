from rest_framework.reverse import reverse


class TestKorisniciSerijalizers:
    """Tesritanje Serijalizers KORISNICI"""

    def test_serializers_svi_korisnici(self, client, nova_tri_korisnika_fixture, novi_jedan_auth_korisnik_fixture):
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
