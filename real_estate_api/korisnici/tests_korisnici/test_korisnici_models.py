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

    def test_promeni_ime_super_user_korisniku(self,novi_jedan_auth_korisnik_fixture):

        ime_korisnika = Korisnici.objects.get(ime=novi_jedan_auth_korisnik_fixture.ime).ime
        ime_iz_fixture_korisnika = novi_jedan_auth_korisnik_fixture.ime

        # Proveri prvo da li je ime iz FIXTURE korisnika isto kao i iz baze
        assert ime_korisnika == ime_iz_fixture_korisnika

        # Promena imena Korisnika
        novi_jedan_auth_korisnik_fixture.ime = 'Test Ime'
        novi_jedan_auth_korisnik_fixture.save()

        novo_ime_korisnika = Korisnici.objects.get(ime=novi_jedan_auth_korisnik_fixture.ime).ime

        assert novo_ime_korisnika == 'Test Ime'








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
