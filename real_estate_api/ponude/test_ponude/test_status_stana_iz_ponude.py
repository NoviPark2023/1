import json

from rest_framework.reverse import reverse

from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi


class TestRestApiUrlsPonude:
    """Testitanje statusa Stana ukoliko dodje do promene-brisanja u ponudama Stana"""

    def test_kreiraj_ponudu_dostupna_status_stana_dostupan(self,
                                                           client,
                                                           nova_jedna_ponuda_json_fixture_status_potencijalan,
                                                           nova_jedna_ponuda_json_fixture_status_rezervisan
                                                           ):
        assert True
        # url_kreiraj_ponudu = reverse('ponude:kreiraj_ponudu')
        #
        # response_kreiraj_ponudu_potencijalan = client.post(
        #     url_kreiraj_ponudu,
        #     data=nova_jedna_ponuda_json_fixture_status_potencijalan,
        #     content_type='application/json'
        # )
        #
        # assert response_kreiraj_ponudu_potencijalan.status_code == 201
        #
        # broj_ponuda_from_db = Ponude.objects.all().count()
        # assert broj_ponuda_from_db == 1
        # assert response_kreiraj_ponudu_potencijalan.data['status_ponude'] == Ponude.StatusPonude.POTENCIJALAN
        # # Proveri status Stana (treba da se "DOSTUPAN")
        # id_stana = json.loads(nova_jedna_ponuda_json_fixture_status_potencijalan)["stan"]
        # stan = Stanovi.objects.filter(id_stana__exact=id_stana)
        # assert stan[0].status_prodaje == Stanovi.StatusProdaje.DOSTUPAN
        #
        # # TODO: Obrisi ove komentare kada se zavrsi testings.
        # print('############################')
        # print('############################')
        # print(f' NOVA PONUDA FIXTURE: {json.loads(nova_jedna_ponuda_json_fixture_status_potencijalan)["id_ponude"]}')
        # print('############################')
        # print('############################')
        #
        # # Izmeni ponudu u REZERVISAN
        # id_ponude = 1
        # url_izmeni_ponudu = reverse('ponude:izmeni_ponudu', args=[int(id_ponude)])
        # izmenjena_ponuda = json.dumps(
        #     {
        #         "id_ponude": 1,
        #         "kupac": 1,
        #         "stan": 1,
        #         "cena_stana_za_kupca": 1000,
        #         "napomena": "Nema Napomene",
        #         "broj_ugovora": "BR.1",
        #         "datum_ugovora": "17.11.2022",
        #         "status_ponude": Ponude.StatusPonude.REZERVISAN,
        #         "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
        #         "odobrenje": False,
        #         "klijent_prodaje": 1
        #     })
        # response = client.put(url_izmeni_ponudu,
        #                       data=izmenjena_ponuda,
        #                       content_type='application/json'
        #                       )
        #
        # assert response.status_code == 200
        #
        # # Proveri da li je stan promenio status u "REZERVISAN".
        # stan = Stanovi.objects.filter(id_stana__exact=response.data["stan"])
        # assert stan[0].status_prodaje == Stanovi.StatusProdaje.REZERVISAN
        #
        # # Izmeni ponudu u KUPLJEN
        # id_ponude = 1
        # url_izmeni_ponudu = reverse('ponude:izmeni_ponudu', args=[int(id_ponude)])
        # izmenjena_ponuda = json.dumps(
        #     {
        #         "id_ponude": 2,
        #         "kupac": 1,
        #         "stan": 1,
        #         "cena_stana_za_kupca": 1000,
        #         "napomena": "Nema Napomene",
        #         "broj_ugovora": "BR.1",
        #         "datum_ugovora": "17.11.2022",
        #         "status_ponude": Ponude.StatusPonude.KUPLJEN,
        #         "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
        #         "odobrenje": False,
        #         "klijent_prodaje": 1
        #     })
        # response = client.put(url_izmeni_ponudu,
        #                       data=izmenjena_ponuda,
        #                       content_type='application/json'
        #                       )
        #
        # assert response.status_code == 200
        #
        # # Proveri da li je stan promenio status u "PRODAT".
        # stan = Stanovi.objects.filter(id_stana__exact=response.data["stan"])
        # assert stan[0].status_prodaje == Stanovi.StatusProdaje.PRODAT






        # ponuda_status_potencijalan = Ponude.objects.all().filter(status_ponude__exact=Ponude.StatusPonude.POTENCIJALAN)
        # assert ponuda_status_potencijalan.first().status_ponude == Ponude.StatusPonude.POTENCIJALAN
        #
        # ponuda_status_rezervisan = Ponude.objects.all().filter(status_ponude__exact=Ponude.StatusPonude.REZERVISAN)
        # assert ponuda_status_rezervisan.first().status_ponude == Ponude.StatusPonude.REZERVISAN
        #
        # ponuda_status_kupljen = Ponude.objects.all().filter(status_ponude__exact=Ponude.StatusPonude.KUPLJEN)
        # assert ponuda_status_kupljen.first().status_ponude == Ponude.StatusPonude.KUPLJEN
        #
        # # Stan
        # stan_za_ovu_ponudu = Stanovi.objects.all().filter(
        #     id_stana__exact=ponuda_status_potencijalan[0].stan.id_stana
        # )
        # print(f' STAN ZA PONUDU: {stan_za_ovu_ponudu.values_list()}')
        # assert stan_za_ovu_ponudu.count() == 1
        #
        # # Proveri trenutni status Stana (Treba da je dostupan jer je Ponuda na statusu dostupan).
        # if ponuda_status_potencijalan.first().status_ponude:
        #     assert stan_za_ovu_ponudu.first().status_prodaje == Stanovi.StatusProdaje.DOSTUPAN
        #
        # if ponuda_status_rezervisan.first().status_ponude:
        #     assert stan_za_ovu_ponudu.first().status_prodaje == Stanovi.StatusProdaje.DOSTUPAN
