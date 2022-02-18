from rest_framework.reverse import reverse

from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi


class TestRestApiUrlsPonude:
    """Testitanje statusa Stana ukoliko dodje do promene-brisanja u ponudama Stana"""

    def test_kreiraj_ponudu_dostupna_status_stana_dostupan(self,
                                                           client,
                                                           nove_tri_ponude_fixture,
                                                           nova_jedna_ponuda_json_fixture_status_potencijalan
                                                           ):
        url_kreiraj_ponudu = reverse('ponude:kreiraj_ponudu')

        response_kreiraj_ponudu = client.post(
            url_kreiraj_ponudu,
            data=nova_jedna_ponuda_json_fixture_status_potencijalan,
            content_type='application/json'
        )

        assert response_kreiraj_ponudu.status_code == 201

        broj_ponuda_from_db = Ponude.objects.all().count()
        assert broj_ponuda_from_db == 4

        ponuda_status_potencijalan = Ponude.objects.all().filter(status_ponude__exact=Ponude.StatusPonude.POTENCIJALAN)
        assert ponuda_status_potencijalan.first().status_ponude == Ponude.StatusPonude.POTENCIJALAN

        ponuda_status_rezervisan = Ponude.objects.all().filter(status_ponude__exact=Ponude.StatusPonude.REZERVISAN)
        assert ponuda_status_rezervisan.first().status_ponude == Ponude.StatusPonude.REZERVISAN

        ponuda_status_kupljen = Ponude.objects.all().filter(status_ponude__exact=Ponude.StatusPonude.KUPLJEN)
        assert ponuda_status_kupljen.first().status_ponude == Ponude.StatusPonude.KUPLJEN

        # Stan
        stan_za_ovu_ponudu = Stanovi.objects.all().filter(
            id_stana__exact=ponuda_status_potencijalan[0].stan.id_stana
        )
        print(f' STAN ZA PONUDU: {stan_za_ovu_ponudu.values_list()}')
        assert stan_za_ovu_ponudu.count() == 1

        # Proveri trenutni status Stana (Treba da je dostupan jer je Ponuda na statusu dostupan).
        if ponuda_status_potencijalan.first().status_ponude:
            assert stan_za_ovu_ponudu.first().status_prodaje == Stanovi.StatusProdaje.DOSTUPAN

        if ponuda_status_rezervisan.first().status_ponude:
            assert stan_za_ovu_ponudu.first().status_prodaje == Stanovi.StatusProdaje.DOSTUPAN


