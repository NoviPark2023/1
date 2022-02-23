import json

from rest_framework.reverse import reverse

from real_estate_api.ponude.models import Ponude
from real_estate_api.stanovi.models import Stanovi


class TestPromenaStatusStanaIzPonudeStana:
    """Testitanje statusa Stana ukoliko dodje do promene-brisanja u Ponudama Stana"""

    def test_da_li_su_tri_ponuda_stana_kreirane(self, nove_tri_ponude_fixture):
        """ Test da li je samo jedana Ponuda kreirana u bazi. """

        broj_ponuda_from_db = Ponude.objects.all().count()
        assert broj_ponuda_from_db == 3

    def test_izmeni_ponudu_potencijalna_status_stana_dostupan(self,
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

    def test_kreiraj_ponudu_potencijalan_status_stana_rezervisan(self,
                                                                 client,
                                                                 nova_jedna_ponuda_fixture_status_rezervisan,
                                                                 novi_kupac_fixture_ponude
                                                                 ):
        """
        Kreiranje nove Ponude za Stan statusa 'POTENCIJALAN', da bi se proverilo da li ce se promeniti
        prvobitni Status Prodaje Stana iz 'REZERVISAN' u 'DOSTUPAN', sto ne sme da se desi
        """
        id_stana = nova_jedna_ponuda_fixture_status_rezervisan.stan.id_stana

        nova_ponuda_stana_potencijalan = json.dumps(
            {
                "kupac": novi_kupac_fixture_ponude.id_kupca,
                "stan": id_stana,
                "cena_stana_za_kupca": 100000,
                "napomena": "Nema Napomene",
                "broj_ugovora": "BR.1",
                "datum_ugovora": "17.1.2022",
                "status_ponude": Ponude.StatusPonude.POTENCIJALAN,
                "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
                "odobrenje": False,
            }
        )

        # Prvobitna ponuda
        ponuda = Ponude.objects.all().first()
        stan = Stanovi.objects.filter(id_stana__exact=ponuda.stan.id_stana).first()

        # Status prvobitne Ponude za stan (Treba da je "REZERVISAN") i odobrenje (True)
        # Status prvobitne Prodaje stana (Treba da je: "REZERVISAN")
        assert ponuda.status_ponude == Ponude.StatusPonude.REZERVISAN
        assert ponuda.odobrenje == True
        assert stan.status_prodaje == Stanovi.StatusProdaje.REZERVISAN

        url_kreiraj_novu_ponudu_stana = reverse('ponude:kreiraj_ponudu')

        response_kreiraj_novu_ponudu_stana = client.post(
            url_kreiraj_novu_ponudu_stana,
            data=nova_ponuda_stana_potencijalan,
            content_type='application/json'
        )
        assert response_kreiraj_novu_ponudu_stana.status_code == 201

        # Nova Ponuda za stan - POTENCIJALAN
        nova_ponuda = Ponude.objects.first()
        izmenjen_stan = Stanovi.objects.filter(id_stana__exact=nova_ponuda.stan.id_stana).first()

        # Provera statusa nove Ponude za stan (Treba da je: "POTENCIJALAN"),
        # odobrenja (False)
        # i Statusa Prodaje stana (Treba da ostane: "REZERVISAN")
        assert nova_ponuda.status_ponude == Ponude.StatusPonude.POTENCIJALAN
        assert nova_ponuda.odobrenje == False
        assert izmenjen_stan.status_prodaje == Stanovi.StatusProdaje.REZERVISAN

    def test_obrisi_ponudu_potencijalan_status_stana_prodat(self,
                                                            client,
                                                            nova_jedna_ponuda_fixture_status_kupljen,
                                                            novi_kupac_fixture_ponude
                                                            ):
        """
        Kreiranje Ponude za Stan statusa 'KUPLJEN', da bi Status Prodaje stana bio 'PRODAT'.
        Kreiranje nove Ponude za Stan statusa 'POTENCIJALAN', a zatim njeno brisanje
        da bi se proverilo da li Status Prodaje stana ostaje PRODAT.
        """
        id_stana = nova_jedna_ponuda_fixture_status_kupljen.stan.id_stana

        nova_ponuda_stana_potencijalan = json.dumps(
            {
                "kupac": novi_kupac_fixture_ponude.id_kupca,
                "stan": id_stana,
                "cena_stana_za_kupca": 100000,
                "napomena": "Nema Napomene",
                "broj_ugovora": "BR.1",
                "datum_ugovora": "17.1.2022",
                "status_ponude": Ponude.StatusPonude.POTENCIJALAN,
                "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
                "odobrenje": False,
            }
        )

        # Prvobitna ponuda
        ponuda = Ponude.objects.all().first()
        stan = Stanovi.objects.filter(id_stana__exact=ponuda.stan.id_stana).first()

        # Status prvobitne Ponude za stan (Treba da je "KUPLJEN") i odobrenje (True)
        # Status prvobitne Prodaje stana (Treba da je: "PRODAT")
        assert ponuda.status_ponude == Ponude.StatusPonude.KUPLJEN
        assert ponuda.odobrenje == True
        assert stan.status_prodaje == Stanovi.StatusProdaje.PRODAT

        url_kreiraj_novu_ponudu_stana = reverse('ponude:kreiraj_ponudu')

        response_kreiraj_novu_ponudu_stana = client.post(
            url_kreiraj_novu_ponudu_stana,
            data=nova_ponuda_stana_potencijalan,
            content_type='application/json'
        )
        assert response_kreiraj_novu_ponudu_stana.status_code == 201

        # Nova Ponuda za stan - POTENCIJALAN
        nova_ponuda = Ponude.objects.first()
        izmenjen_stan = Stanovi.objects.filter(id_stana__exact=nova_ponuda.stan.id_stana).first()

        # Provera statusa nove Ponude za stan (Treba da je: "POTENCIJALAN"),
        # odobrenja (False)
        # i Statusa Prodaje stana (Treba da ostane: "PRODAT")
        assert nova_ponuda.status_ponude == Ponude.StatusPonude.POTENCIJALAN
        assert nova_ponuda.odobrenje == False
        assert izmenjen_stan.status_prodaje == Stanovi.StatusProdaje.PRODAT

        url_obrisi_novu_ponudu = reverse(
            'ponude:obrisi_ponudu',
            args=[nova_ponuda.id_ponude]
        )

        response = client.delete(url_obrisi_novu_ponudu)

        assert response.status_code == 204

        # Preostala prvobitna ponuda
        ponuda = Ponude.objects.all().first()
        stan = Stanovi.objects.filter(id_stana__exact=ponuda.stan.id_stana).first()

        # Provera Statusa Prodaje stana (Treba da je ostao: "PRODAT")
        assert stan.status_prodaje == Stanovi.StatusProdaje.PRODAT

    def test_obrisi_ponudu_rezervisan_status_stana_prodat(self,
                                                          client,
                                                          nova_jedna_ponuda_fixture_status_kupljen,
                                                          novi_kupac_fixture_ponude
                                                          ):
        """
        Kreiranje Ponude za Stan statusa 'KUPLJEN', da bi Status Prodaje stana bio 'PRODAT'.
        Kreiranje nove Ponude za Stan statusa 'REZERVISAN', a zatim njeno brisanje
        da bi se proverilo da li Status Prodaje stana ostaje PRODAT.
        """
        id_stana = nova_jedna_ponuda_fixture_status_kupljen.stan.id_stana

        nova_ponuda_stana_rezervisan = json.dumps(
            {
                "kupac": novi_kupac_fixture_ponude.id_kupca,
                "stan": id_stana,
                "cena_stana_za_kupca": 100000,
                "napomena": "Nema Napomene",
                "broj_ugovora": "BR.2",
                "datum_ugovora": "17.1.2022",
                "status_ponude": Ponude.StatusPonude.REZERVISAN,
                "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
                "odobrenje": True,
            }
        )

        # Prvobitna ponuda
        ponuda = Ponude.objects.all().first()
        stan = Stanovi.objects.filter(id_stana__exact=ponuda.stan.id_stana).first()

        # Status prvobitne Ponude za stan (Treba da je "KUPLJEN") i odobrenje (True)
        # Status prvobitne Prodaje stana (Treba da je: "PRODAT")
        assert ponuda.status_ponude == Ponude.StatusPonude.KUPLJEN
        assert ponuda.odobrenje == True
        assert stan.status_prodaje == Stanovi.StatusProdaje.PRODAT

        url_kreiraj_novu_ponudu_stana = reverse('ponude:kreiraj_ponudu')

        response_kreiraj_novu_ponudu_stana = client.post(
            url_kreiraj_novu_ponudu_stana,
            data=nova_ponuda_stana_rezervisan,
            content_type='application/json'
        )
        assert response_kreiraj_novu_ponudu_stana.status_code == 201

        # Nova Ponuda za stan - REZERVISAN
        nova_ponuda = Ponude.objects.first()
        izmenjen_stan = Stanovi.objects.filter(id_stana__exact=nova_ponuda.stan.id_stana).first()

        # Provera statusa nove Ponude za stan (Treba da je: "REZERVISAN"),
        # odobrenja (True)
        # i Statusa Prodaje stana (Treba da ostane: "PRODAT")
        assert nova_ponuda.status_ponude == Ponude.StatusPonude.REZERVISAN
        assert nova_ponuda.odobrenje == True
        assert izmenjen_stan.status_prodaje == Stanovi.StatusProdaje.PRODAT

        url_obrisi_novu_ponudu = reverse(
            'ponude:obrisi_ponudu',
            args=[nova_ponuda.id_ponude]
        )

        response = client.delete(url_obrisi_novu_ponudu)

        assert response.status_code == 204

        # Preostala prvobitna ponuda
        ponuda = Ponude.objects.all().first()
        stan = Stanovi.objects.filter(id_stana__exact=ponuda.stan.id_stana).first()

        # Provera Statusa Prodaje stana (Treba da je ostao: "PRODAT")
        assert stan.status_prodaje == Stanovi.StatusProdaje.PRODAT

    def test_obrisi_ponudu_kupljen_status_stana_rezervisan(self,
                                                           client,
                                                           nova_jedna_ponuda_fixture_status_kupljen,
                                                           novi_kupac_fixture_ponude
                                                           ):
        """
        Kreiranje Ponude za Stan statusa 'KUPLJEN', da bi Status Prodaje stana bio 'PRODAT'.
        Kreiranje nove Ponude za Stan statusa 'REZERVISAN', Status Prodaje stana ostaje 'PRODAT'.
        Brisanje prve Ponude da bi se proverilo da li Status Prodaje stana prelazi u 'REZERVISAN'.
        """
        id_stana = nova_jedna_ponuda_fixture_status_kupljen.stan.id_stana

        nova_ponuda_stana_rezervisan = json.dumps(
            {
                "kupac": novi_kupac_fixture_ponude.id_kupca,
                "stan": id_stana,
                "cena_stana_za_kupca": 100000,
                "napomena": "Nema Napomene",
                "broj_ugovora": "BR.3",
                "datum_ugovora": "17.1.2022",
                "status_ponude": Ponude.StatusPonude.REZERVISAN,
                "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
                "odobrenje": True,
            }
        )

        # Prvobitna ponuda
        ponuda = Ponude.objects.all().first()
        stan = Stanovi.objects.filter(id_stana__exact=ponuda.stan.id_stana).first()

        # Status prvobitne Ponude za stan (Treba da je "KUPLJEN") i odobrenje (True)
        # Status prvobitne Prodaje stana (Treba da je: "PRODAT")
        assert ponuda.status_ponude == Ponude.StatusPonude.KUPLJEN
        assert ponuda.odobrenje == True
        assert stan.status_prodaje == Stanovi.StatusProdaje.PRODAT

        url_kreiraj_novu_ponudu_stana = reverse('ponude:kreiraj_ponudu')

        response_kreiraj_novu_ponudu_stana = client.post(
            url_kreiraj_novu_ponudu_stana,
            data=nova_ponuda_stana_rezervisan,
            content_type='application/json'
        )
        assert response_kreiraj_novu_ponudu_stana.status_code == 201

        # Nova Ponuda za stan - REZERVISAN
        nova_ponuda = Ponude.objects.first()
        izmenjen_stan = Stanovi.objects.filter(id_stana__exact=nova_ponuda.stan.id_stana).first()

        # Provera statusa nove Ponude za stan (Treba da je: "REZERVISAN"),
        # odobrenja (True)
        # i Statusa Prodaje stana (Treba da ostane: "PRODAT")
        assert nova_ponuda.status_ponude == Ponude.StatusPonude.REZERVISAN
        assert nova_ponuda.odobrenje == True
        assert izmenjen_stan.status_prodaje == Stanovi.StatusProdaje.PRODAT

        url_obrisi_prvu_ponudu = reverse(
            'ponude:obrisi_ponudu',
            args=[ponuda.id_ponude]
        )

        response = client.delete(url_obrisi_prvu_ponudu)

        assert response.status_code == 204

        # Preostala druga ponuda
        nova_ponuda = Ponude.objects.all().first()
        stan = Stanovi.objects.filter(id_stana__exact=nova_ponuda.stan.id_stana).first()

        # Provera Statusa Prodaje stana (Treba da predje u: "REZERVISAN")
        assert stan.status_prodaje == Stanovi.StatusProdaje.REZERVISAN

    def test_obrisi_sve_ponude_stana_status_stana_dostupan(self,
                                                           client,
                                                           nova_jedna_ponuda_fixture,
                                                           novi_kupac_fixture_ponude,
                                                           novi_jedan_stan_fixture_ponude_status_dostupan
                                                           ):
        """
        Brisanje svih Ponuda za Stan, kako bi se Status Prodaje stana vratio na 'DOSTUPAN'.
        """
        nova_ponuda_stana_rezervisan = json.dumps(
            {
                "kupac": novi_kupac_fixture_ponude.id_kupca,
                "stan": novi_jedan_stan_fixture_ponude_status_dostupan.id_stana,
                "cena_stana_za_kupca": 90000,
                "napomena": "Nema Napomene",
                "broj_ugovora": "BR.33",
                "datum_ugovora": "17.1.2022",
                "status_ponude": Ponude.StatusPonude.REZERVISAN,
                "nacin_placanja": Ponude.NacinPlacanja.U_CELOSTI,
                "odobrenje": True,
            }
        )

        url_kreiraj_novu_ponudu_stana = reverse('ponude:kreiraj_ponudu')

        response_kreiraj_novu_ponudu_stana = client.post(
            url_kreiraj_novu_ponudu_stana,
            data=nova_ponuda_stana_rezervisan,
            content_type='application/json'
        )

        druga_ponuda_stana = Ponude.objects.all().first()
        stan = Stanovi.objects.filter(id_stana__exact=druga_ponuda_stana.stan.id_stana).first()

        prva_ponuda_stana = Ponude.objects.last()
        izmenjen_stan = Stanovi.objects.filter(id_stana__exact=prva_ponuda_stana.stan.id_stana).first()

        # Provera statusa prve i druge ponude
        assert druga_ponuda_stana.status_ponude == Ponude.StatusPonude.REZERVISAN
        assert stan.status_prodaje == Stanovi.StatusProdaje.REZERVISAN

        assert prva_ponuda_stana.status_ponude == Ponude.StatusPonude.POTENCIJALAN
        assert izmenjen_stan.status_prodaje == Stanovi.StatusProdaje.REZERVISAN

        url_obrisi_drugu_ponudu_stana = reverse(
            'ponude:obrisi_ponudu',
            args=[druga_ponuda_stana.id_ponude]
        )

        response = client.delete(url_obrisi_drugu_ponudu_stana)
        assert response.status_code == 204

        url_obrisi_prvu_ponudu_stana = reverse(
            'ponude:obrisi_ponudu',
            args=[prva_ponuda_stana.id_ponude]
        )

        response = client.delete(url_obrisi_prvu_ponudu_stana)
        assert response.status_code == 204

        # Provera Statusa Prodaje stana nakon brisanja svih ponuda (Treba da je: "DOSTUPAN")
        stan = Stanovi.objects.filter(id_stana__exact=novi_jedan_stan_fixture_ponude_status_dostupan.id_stana).first()

        assert stan.status_prodaje == Stanovi.StatusProdaje.DOSTUPAN
