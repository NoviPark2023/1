from rest_framework.reverse import reverse


class TestPonudeSerijalizers:
    """Tesritanje Serijalizers PONUDE"""

    def test_serializers_sve_ponude(self, client, nove_tri_ponude_fixture):
        response = client.get(reverse('ponude:lista_ponuda'))

        print(f' RESPONSE: {response.data}')
        pass
