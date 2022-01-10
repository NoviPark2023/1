from real_estate_api.korisnici.models import Korisnici


class TestEntitetaKorisnici:
    """Testitanje entiteta Korisnici"""

    def test_kreiranje_jednog_novog_korisnika(self, novi_jedan_auth_korisnik_fixture):
        """
        Testiranje kreiranja novog jednog Korisnika i provera podataka nakon kreiranja.
            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture
        ---
        @param novi_jedan_auth_korisnik_fixture: entitet Korisnici
        """

        korisnik_from_db = Korisnici.objects.all()
        email = korisnik_from_db[0].email
        username = korisnik_from_db[0].username
        password = korisnik_from_db[0].password
        ime = korisnik_from_db[0].ime
        prezime = korisnik_from_db[0].prezime
        role = korisnik_from_db[0].role
        about = korisnik_from_db[0].about
        is_staff = korisnik_from_db[0].is_staff
        is_active = korisnik_from_db[0].is_active
        is_superuser = korisnik_from_db[0].is_superuser

        assert novi_jedan_auth_korisnik_fixture.email == email
        assert novi_jedan_auth_korisnik_fixture.username == username
        assert novi_jedan_auth_korisnik_fixture.password == password
        assert novi_jedan_auth_korisnik_fixture.ime == ime
        assert novi_jedan_auth_korisnik_fixture.prezime == prezime
        assert novi_jedan_auth_korisnik_fixture.role == role
        assert novi_jedan_auth_korisnik_fixture.about == about
        assert novi_jedan_auth_korisnik_fixture.is_staff == is_staff
        assert novi_jedan_auth_korisnik_fixture.is_active == is_active
        assert novi_jedan_auth_korisnik_fixture.is_superuser == is_superuser

    def test_broj_novih_korisnika_u_bazi(self, novi_jedan_auth_korisnik_fixture):
        """
        Test da li je samo jedan Korisnik kreiran u bazi.
            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture
        ---
        @param novi_jedan_auth_korisnik_fixture: Korisnici
        """

        broj_korisnika_u_bazi = Korisnici.objects.all().count()
        assert broj_korisnika_u_bazi == 1

    def test_is_korsnik_super_user(self, novi_jedan_auth_korisnik_fixture):
        """
        Test da li je kreiran Korisnik u bazi "SUPERUSER".
            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture
        ---
        @param novi_jedan_auth_korisnik_fixture: Korisnici
        """
        assert Korisnici.objects.filter(is_superuser=True).exists()

    def test_kreiranje_tri_nova_korisnika(self, nova_tri_korisnika_fixture):
        """
        Testiranje kreiranja nova tri Korisnika i provera podataka nakon kreiranja.
            * @see /test_korisnici/conftest.py : nova_tri_korisnika_fixture
        ---
        @param nova_tri_korisnika_fixture: entitet Korisnici
        """
        korisnici = Korisnici.objects.all().values()
        print(f'KORISNIK IZ DBa: {korisnici}')

        broj_korisnika_u_bazi = Korisnici.objects.all().count()

        # Ovde je 4 jer u bazi pored ova tri ima i jedn registrovan super-user Korisnik.
        assert broj_korisnika_u_bazi == 4

    def test_filteri_korisnika_po_atributima(self, nova_tri_korisnika_fixture):
        """
        Testiranje filter po nekim od polja i to:
            - id
            - ime
            - prezime

            * @see /test_korisnici/conftest.py : nova_tri_korisnika_fixture
        ---
        @param nova_tri_korisnika_fixture: entitet Korisnici
        """

        # Po Id-u
        assert Korisnici.objects.filter(id=1).exists()
        assert Korisnici.objects.filter(id=2).exists()
        assert Korisnici.objects.filter(id=3).exists()

        # Po Imenu
        assert Korisnici.objects.filter(ime="Dejan").exists()
        assert Korisnici.objects.filter(ime="Slobodan").exists()
        assert Korisnici.objects.filter(ime="Ivana").exists()

        # Po Prezimenu
        assert Korisnici.objects.filter(prezime="Cugalj").exists()
        assert Korisnici.objects.filter(prezime="Tomic").exists()
        assert Korisnici.objects.filter(prezime="Tepavac").exists()

    def test_promeni_ime_super_user_korisniku(self, novi_jedan_auth_korisnik_fixture):
        """
        Promena IMENA Korisnika i test po raznim parametrima.

            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture
        ---
        @param novi_jedan_auth_korisnik_fixture: entitet Korisnici
        """
        ime_korisnika = Korisnici.objects.get(ime=novi_jedan_auth_korisnik_fixture.ime).ime
        ime_iz_fixture_korisnika = novi_jedan_auth_korisnik_fixture.ime

        # Proveri prvo da li je IME iz FIXTURE korisnika isto kao i iz baze
        assert ime_korisnika == ime_iz_fixture_korisnika

        # Promena imena Korisnika
        novi_jedan_auth_korisnik_fixture.ime = 'Test Ime'
        novi_jedan_auth_korisnik_fixture.save()

        novo_ime_korisnika = Korisnici.objects.get(ime=novi_jedan_auth_korisnik_fixture.ime).ime

        assert novo_ime_korisnika == 'Test Ime'
        assert novo_ime_korisnika == Korisnici.objects.get(ime=novi_jedan_auth_korisnik_fixture.ime).ime
        assert Korisnici.objects.filter(ime=novo_ime_korisnika).count() == 1
        assert Korisnici.objects.filter(ime=novo_ime_korisnika).exists()

    def test_promeni_prezime_super_user_korisniku(self, novi_jedan_auth_korisnik_fixture):
        """
        Promena PREZIMENA Korisnika i test po raznim parametrima.

            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture
        ---
        @param novi_jedan_auth_korisnik_fixture: entitet Korisnici
        """
        prezime_korisnika = Korisnici.objects.get(prezime=novi_jedan_auth_korisnik_fixture.prezime).prezime
        prezime_iz_fixture_korisnika = novi_jedan_auth_korisnik_fixture.prezime

        # Proveri prvo da li je PREZIME iz FIXTURE korisnika isto kao i iz baze
        assert prezime_korisnika == prezime_iz_fixture_korisnika

        # Promena prezimena Korisnika
        novi_jedan_auth_korisnik_fixture.prezime = 'Test Prezime'
        novi_jedan_auth_korisnik_fixture.save()

        novo_prezime_korisnika = Korisnici.objects.get(prezime=novi_jedan_auth_korisnik_fixture.prezime).prezime

        assert novo_prezime_korisnika == 'Test Prezime'
        assert novo_prezime_korisnika == Korisnici.objects.get(prezime=novi_jedan_auth_korisnik_fixture.prezime).prezime
        assert Korisnici.objects.filter(prezime=novo_prezime_korisnika).count() == 1
        assert Korisnici.objects.filter(prezime=novo_prezime_korisnika).exists()

    def test_promeni_role_super_user_korisniku(self, novi_jedan_auth_korisnik_fixture):
        """
        Promena ROLE Korisnika i test po raznim parametrima.

            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture
        ---
        @param novi_jedan_auth_korisnik_fixture: entitet Korisnici
        """
        rola_korisnika = Korisnici.objects.get(role=novi_jedan_auth_korisnik_fixture.role).role
        rola_iz_fixture_korisnika = novi_jedan_auth_korisnik_fixture.role

        # Proveri prvo da li je ROLE iz FIXTURE korisnika isto kao i iz baze
        assert rola_korisnika == rola_iz_fixture_korisnika

        # Promena ROLE Korisnika
        novi_jedan_auth_korisnik_fixture.role = Korisnici.PrivilegijeKorisnika.FINANSIJE
        novi_jedan_auth_korisnik_fixture.save()

        nova_rola_korisnika = Korisnici.objects.get(role=novi_jedan_auth_korisnik_fixture.role).role

        assert nova_rola_korisnika == Korisnici.PrivilegijeKorisnika.FINANSIJE
        assert nova_rola_korisnika == Korisnici.objects.get(role=novi_jedan_auth_korisnik_fixture.role).role
        assert Korisnici.objects.filter(role=nova_rola_korisnika).count() == 1
        assert Korisnici.objects.filter(role=nova_rola_korisnika).exists()

    def test_promeni_about_super_user_korisniku(self, novi_jedan_auth_korisnik_fixture):
        """
        Promena ABOUT Korisnika i test po raznim parametrima.

            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture
        ---
        @param novi_jedan_auth_korisnik_fixture: entitet Korisnici
        """
        about_korisnika = Korisnici.objects.get(about=novi_jedan_auth_korisnik_fixture.about).about
        about_iz_fixture_korisnika = novi_jedan_auth_korisnik_fixture.about

        # Proveri prvo da li je ABOUT iz FIXTURE korisnika isto kao i iz baze
        assert about_korisnika == about_iz_fixture_korisnika

        # Promena ABOUT Korisnika
        novi_jedan_auth_korisnik_fixture.about = "TEST ABOUT KORISNIKA."
        novi_jedan_auth_korisnik_fixture.save()

        novi_about_korisnika = Korisnici.objects.get(about=novi_jedan_auth_korisnik_fixture.about).about

        assert novi_about_korisnika == "TEST ABOUT KORISNIKA."
        assert novi_about_korisnika == Korisnici.objects.get(about=novi_jedan_auth_korisnik_fixture.about).about
        assert Korisnici.objects.filter(about=novi_about_korisnika).count() == 1
        assert Korisnici.objects.filter(about=novi_about_korisnika).exists()

    def test_promeni_is_staff_super_user_korisniku(self, novi_jedan_auth_korisnik_fixture):
        """
        Promena IS_STAF Korisnika i test po raznim parametrima.

            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture
        ---
        @param novi_jedan_auth_korisnik_fixture: entitet Korisnici
        """
        is_staff_korisnika = Korisnici.objects.get(is_staff=novi_jedan_auth_korisnik_fixture.is_staff).is_staff
        is_staff_iz_fixture_korisnika = novi_jedan_auth_korisnik_fixture.is_staff

        # Proveri prvo da li je IS_STAF iz FIXTURE korisnika isto kao i iz baze
        assert is_staff_korisnika == is_staff_iz_fixture_korisnika

        # Promena IS_STAF Korisnika
        novi_jedan_auth_korisnik_fixture.is_staff = False
        novi_jedan_auth_korisnik_fixture.save()

        novi_is_staff_korisnika = Korisnici.objects.get(is_staff=novi_jedan_auth_korisnik_fixture.is_staff).is_staff

        assert not novi_is_staff_korisnika
        assert novi_is_staff_korisnika == Korisnici.objects.get(
            is_staff=novi_jedan_auth_korisnik_fixture.is_staff
        ).is_staff
        assert Korisnici.objects.filter(is_staff=novi_is_staff_korisnika).count() == 1
        assert Korisnici.objects.filter(is_staff=novi_is_staff_korisnika).exists()

    def test_promeni_is_active_super_user_korisniku(self, novi_jedan_auth_korisnik_fixture):
        """
        Promena IS_ACTIVE Korisnika i test po raznim parametrima.

            * @see /test_korisnici/conftest.py : novi_jedan_auth_korisnik_fixture
        ---
        @param novi_jedan_auth_korisnik_fixture: entitet Korisnici
        """
        is_active_korisnika = Korisnici.objects.get(is_active=novi_jedan_auth_korisnik_fixture.is_active).is_active
        is_active_iz_fixture_korisnika = novi_jedan_auth_korisnik_fixture.is_active

        # Proveri prvo da li je IS_ACTIVE iz FIXTURE korisnika isto kao i iz baze
        assert is_active_korisnika == is_active_iz_fixture_korisnika

        # Promena IS_ACTIVE Korisnika
        novi_jedan_auth_korisnik_fixture.is_active = False
        novi_jedan_auth_korisnik_fixture.save()

        novi_is_active_korisnika = Korisnici.objects.get(is_active=novi_jedan_auth_korisnik_fixture.is_active).is_active

        assert not novi_is_active_korisnika
        assert novi_is_active_korisnika == Korisnici.objects.get(
            is_active=novi_jedan_auth_korisnik_fixture.is_active
        ).is_active
        assert Korisnici.objects.filter(is_active=novi_is_active_korisnika).count() == 1
        assert Korisnici.objects.filter(is_active=novi_is_active_korisnika).exists()

# class PasswordChange(TestCase):
#     def test_change_password(self):
#         c = Client()
#         url = 'http://0.0.0.0:8000/korisnici/izmeni-korisnika/14/'
#         payload = {'csrf_token': csrf_token, 'payload': json.dumps({'password': 'test2'})}
#         headers = {'Cookie': 'csrftoken=' + csrf_token}
#
#         res = c.post(url, payload, headers=headers)
#         res = res.json()
#         self.assertEqual(res['password_changed'], True)
#         korisnik = Korisnici.objects.get(username='ivana')
#         self.assertEqual(korisnik.check_password('test2'), True)
