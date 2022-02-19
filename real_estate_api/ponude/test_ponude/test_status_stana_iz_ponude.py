import json

from rest_framework.reverse import reverse

from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi


class TestPromenaStatusStanaIzPonudeStana:
    """Testitanje statusa Stana ukoliko dodje do promene-brisanja u ponudama Stana"""

    def test_da_li_su_tri_ponuda_stana_kreirane(self, nove_tri_ponude_fixture):
        """ Test da li je samo jedana Ponuda kreirana u bazi. """

        broj_ponuda_from_db = Ponude.objects.all().count()
        assert broj_ponuda_from_db == 3

    def test_kreiraj_ponudu_potencijalna_status_stana_dostupan(self,
                                                               client,
                                                               nova_jedna_ponuda_fixture,
                                                               ):
        """
        Kada se Ponuda kreira i postavi na status: "POTENCIJALAN", tada i Stan
        treba da ostane u statusu: "DOSTUPAN".

        :param client: A Django test client instance.
        :param nova_jedna_ponuda_fixture: Nova Ponuda Fixture.
        """
        id_stana = nova_jedna_ponuda_fixture.stan.id_stana

        nova_ponuda_potencijalna = json.dumps(
            {
                "id_ponude": 1,
                "kupac": nova_jedna_ponuda_fixture.kupac.id_kupca,
                "stan": nova_jedna_ponuda_fixture.stan.id_stana,
                "cena_stana_za_kupca": 1000,
                "napomena": "Nema Napomene",
                "broj_ugovora": "BR.1",
                "datum_ugovora": "19.11.2022",
                "status_ponude": Ponude.StatusPonude.POTENCIJALAN,
                "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
                "odobrenje": False,
                "klijent_prodaje": nova_jedna_ponuda_fixture.kupac.id_kupca
            }
        )

        # Proveri status Stana, posto je tek kreiran, treba da bude "DOSTUPAN".
        status_stana_dostupan = Stanovi.StatusProdaje.DOSTUPAN
        trenutni_status_stana = Stanovi.objects.filter(id_stana__exact=id_stana)[0].status_prodaje
        assert status_stana_dostupan == trenutni_status_stana

        # Izmeni Ponudu i postavi na status: "REZERVISAN".
        url_izmeni_ponudu = reverse('ponude:izmeni_ponudu', args=[nova_jedna_ponuda_fixture.id_ponude])
        response = client.put(url_izmeni_ponudu,
                              data=nova_ponuda_potencijalna,
                              content_type='application/json'
                              )
        assert response.status_code == 200

        # Proveri Odobrenje, posto je status Ponude sada: "POTENCIJALAN", treba da bude FALSE.
        assert response.data["odobrenje"] is False

        # Proveri status Stana, posto je ponuda izmenjena, treba da bude "DOSTUPAN".
        status_stana_dostupan = Stanovi.StatusProdaje.DOSTUPAN
        trenutni_status_stana = Stanovi.objects.filter(id_stana__exact=id_stana)[0].status_prodaje
        assert status_stana_dostupan == trenutni_status_stana

    def test_izmeni_ponudu_u_rezervisan_status_stana_rezervisan(self,
                                                                client,
                                                                nova_jedna_ponuda_fixture,
                                                                ):
        """
        Kada se Ponuda kreira i postavi na status: "REZERVISAN", tada i Stan
        treba da predje u statusu: "REZERVISAN", ako Stan vec nije u statusu: "KUPLJEN".

        :param client: A Django test client instance.
        :param nova_jedna_ponuda_fixture: Nova Ponuda Fixture.
        """

        id_stana = nova_jedna_ponuda_fixture.stan.id_stana

        nova_ponuda_potencijalna = json.dumps(
            {
                "kupac": nova_jedna_ponuda_fixture.kupac.id_kupca,
                "stan": nova_jedna_ponuda_fixture.stan.id_stana,
                "cena_stana_za_kupca": 1000,
                "napomena": "Nema Napomene",
                "broj_ugovora": "BR.1",
                "datum_ugovora": "17.11.2022",
                "status_ponude": Ponude.StatusPonude.REZERVISAN,
                "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
                "klijent_prodaje": nova_jedna_ponuda_fixture.kupac.id_kupca
            }
        )

        # Proveri status Stana, posto je ponuda kreirana, treba da bude "DOSTUPAN".
        status_stana_dostupan = Stanovi.StatusProdaje.DOSTUPAN
        trenutni_status_stana = Stanovi.objects.filter(id_stana__exact=id_stana)[0].status_prodaje
        assert status_stana_dostupan == trenutni_status_stana

        # Izmeni Ponudu i postavi na status: "REZERVISAN".
        url_izmeni_ponudu = reverse('ponude:izmeni_ponudu', args=[nova_jedna_ponuda_fixture.id_ponude])
        response = client.put(url_izmeni_ponudu,
                              data=nova_ponuda_potencijalna,
                              content_type='application/json'
                              )
        assert response.status_code == 200

        # Proveri Odobrenje, posto je status Ponude sada: "REZERVISAN", treba da bude TRUE.
        assert response.data["odobrenje"] is True

        # Proveri status Stana, posto je status Ponude: "REZERVISAN" treba da bude "REZERVISAN".
        status_stana_rezervisan = Stanovi.StatusProdaje.REZERVISAN
        status_stana_nakon_zmene_ponude = Stanovi.objects.filter(id_stana__exact=id_stana)[0].status_prodaje
        assert status_stana_rezervisan == status_stana_nakon_zmene_ponude

    def test_izmeni_ponudu_u_kupljen_status_stana_prodat(self,
                                                         client,
                                                         nova_jedna_ponuda_fixture,
                                                         ):
        """
        Kada se Ponuda kreira i postavi na status: "KUPLJEN", tada i Stan
        treba da predje u statusu: "PRODAT", bez obzira na sve.

        :param client: A Django test client instance.
        :param nova_jedna_ponuda_fixture: Nova Ponuda Fixture.
        """

        id_stana = nova_jedna_ponuda_fixture.stan.id_stana

        nova_ponuda_status_kupljen = json.dumps(
            {
                "kupac": nova_jedna_ponuda_fixture.kupac.id_kupca,
                "stan": nova_jedna_ponuda_fixture.stan.id_stana,
                "cena_stana_za_kupca": 1000,
                "napomena": "Nema Napomene",
                "broj_ugovora": "BR.1",
                "datum_ugovora": "17.11.2022",
                "status_ponude": Ponude.StatusPonude.KUPLJEN,
                "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
                "klijent_prodaje": nova_jedna_ponuda_fixture.kupac.id_kupca
            }
        )

        # Proveri status Stana, posto je ponuda kreirana, treba da bude "DOSTUPAN".
        status_stana_dostupan = Stanovi.StatusProdaje.DOSTUPAN
        trenutni_status_stana = Stanovi.objects.filter(id_stana__exact=id_stana)[0].status_prodaje
        assert status_stana_dostupan == trenutni_status_stana

        # Izmeni Ponudu i postavi na status: "KUPLJEN".
        url_izmeni_ponudu = reverse('ponude:izmeni_ponudu', args=[nova_jedna_ponuda_fixture.id_ponude])
        response = client.put(url_izmeni_ponudu,
                              data=nova_ponuda_status_kupljen,
                              content_type='application/json'
                              )
        assert response.status_code == 200

        # Proveri Odobrenje, posto je status Ponude sada: "KUPLJEN", treba da bude TRUE.
        assert response.data["odobrenje"] is True

        # Proveri status Stana, posto je status Ponude: "KUPLJEN" treba da bude "PRODAT".
        status_stana_rezervisan = Stanovi.StatusProdaje.PRODAT
        status_stana_nakon_zmene_ponude = Stanovi.objects.filter(id_stana__exact=id_stana)[0].status_prodaje
        assert status_stana_rezervisan == status_stana_nakon_zmene_ponude

    def test_dodaj_ponudu_potencijalan_status_stana_rezervisan(self,
                                                               client,
                                                               nove_tri_ponude_fixture,
                                                               ):
        # TODO(Ivana): Implementirati situaciju kada se obrise POTENCIJALNA ponuda:
        # TODO(Ivana): PONUDA -> POTENCIJALNA  ||  STAN -> REZERVISAN

        stan = Stanovi.objects.all().values().first()

        print("\n")
        print(f' ID STANA: {stan["id_stana"]}')
        print(f' STATUS PRODAJE STANA: {stan["status_prodaje"]}')
        print("\n")
        print('############################')
        print('############################')
        print('############################')
        print("\n")

        # Pristup pojedinacnoj Ponudi.
        ponuda = Ponude.objects.all().values()[0]

        print(f' PONUDA: {ponuda}')


        # TODO(Ivana): 1. Kreirati Ponudu koja je rezervisana da bi status Stana bio "REZERVISAN".
        # TODO(Ivana): 2. Kreirati Ponudu status "POTENCIJALAN", i proveriti da li je Stan ostao REZERVISAN.
        # TODO(Ivana): 3. Takodje proveriti "ODOBRENJE PONUDE".

        assert True

    def test_dodaj_ponudu_potencijalan_status_stana_prodat(self,
                                                           client,
                                                           nove_tri_ponude_fixture,
                                                           ):
        # TODO(Ivana): 1. Kreirati Ponudu koja je u statusu: "KUPLJEN" da bi status Stana bio "PRODAT".
        # TODO(Ivana): 2. Kreirati Ponudu status "POTENCIJALAN", i proveriti da li je Stan ostao "PRODAT".
        # TODO(Ivana): 3. Takodje proveriti "ODOBRENJE PONUDE".

        assert True

    def test_obrisi_ponudu_rezervisan_status_stana_prodat(self,
                                                          client,
                                                          nove_tri_ponude_fixture,
                                                          ):
        # TODO(Ivana): 1. Kreirati Ponudu koja je u statusu: "KUPLJEN" da bi status Stana bio "PRODAT".
        # TODO(Ivana): 2. Obrisati Ponudu status "POTENCIJALAN", i proveriti da li je Stan ostao "PRODAT".

        assert True

    def test_obrisi_ponudu_kupljen_status_stana_rezervisan(self,
                                                           client,
                                                           nove_tri_ponude_fixture,
                                                           ):
        # TODO(Ivana): 1. Kreirati Ponudu koja je u statusu: "REZERVISAN" da bi status Stana bio "REZERVISAN".
        # TODO(Ivana): 2. Obrisati Ponudu status "POTENCIJALAN", i proveriti da li je Stan ostao "REZERVISAN".
        assert True
