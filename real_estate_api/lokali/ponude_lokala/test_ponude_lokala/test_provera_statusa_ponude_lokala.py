from rest_framework.reverse import reverse
from real_estate_api.lokali.ponude_lokala.models import PonudeLokala


class TestPonudeLokalaStatusPonudeLokala:
    """Testiranje promene Statusa Ponude Lokala u PONUDAMA LOKALA"""

    def test_status_ponude_lokala_potencijalan(self, client, nova_jedna_ponuda_lokala_json_fixture):

        url_kreiraj_ponudu_lokala = reverse('ponude-lokali:kreiraj_ponudu_lokala')

        response = client.post(
            url_kreiraj_ponudu_lokala,
            data=nova_jedna_ponuda_lokala_json_fixture,
            content_type='application/json'
        )

        assert response.status_code == 201
        assert response.json()["status_ponude_lokala"] == 'potencijalan'

        # provera Statusa Prodaje Lokala (Lokali), treba da je Dostupan.

        ponude_lokala  = PonudeLokala.objects.first()
        lokal_status = ponude_lokala.lokali.status_prodaje_lokala
        assert lokal_status == 'dostupan'


    def test_status_ponude_lokala_rezervisan(self, client, nova_jedna_ponuda_lokala_status_rezervisan_json_fixture):

        url_kreiraj_ponudu_lokala = reverse('ponude-lokali:kreiraj_ponudu_lokala')

        response = client.post(
            url_kreiraj_ponudu_lokala,
            data=nova_jedna_ponuda_lokala_status_rezervisan_json_fixture,
            content_type='application/json'
        )

        assert response.status_code == 201
        assert response.json()["status_ponude_lokala"] == 'rezervisan'

        # provera Odobrenja kupovine lokala (Ponude Lokala), treba da iz False predje u True.

        assert response.json()["odobrenje_kupovine_lokala"] == True

        # provera Statusa Prodaje Lokala (Lokali), treba da iz Dostupan predje u Rezervisan.

        ponude_lokala  = PonudeLokala.objects.first()
        lokal_status = ponude_lokala.lokali.status_prodaje_lokala
        assert lokal_status == 'rezervisan'

    def test_status_ponude_lokala_kupljen(self, client, nova_jedna_ponuda_lokala_status_kupljen_json_fixture):

        url_kreiraj_ponudu_lokala = reverse('ponude-lokali:kreiraj_ponudu_lokala')

        response = client.post(
            url_kreiraj_ponudu_lokala,
            data=nova_jedna_ponuda_lokala_status_kupljen_json_fixture,
            content_type='application/json'
        )

        assert response.status_code == 201
        assert response.json()["status_ponude_lokala"] == 'kupljen'

        # provera Odobrenja kupovine lokala (Ponude Lokala), treba da iz False predje u True.

        assert response.json()["odobrenje_kupovine_lokala"] == True

        # provera Statusa Prodaje Lokala (Lokali), treba da iz Dostupan/Rezervisan  predje u Prodat.

        ponude_lokala  = PonudeLokala.objects.first()
        lokal_status = ponude_lokala.lokali.status_prodaje_lokala
        assert lokal_status == 'prodat'

