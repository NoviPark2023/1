from django.template.defaulttags import csrf_token
from django.test import TestCase, Client
import json
from real_estate_api.korisnici.models import Korisnici


class TestModelaKorisnici(TestCase):

    @classmethod
    def setUp(cls):
        # Kreiraj TEST Korisnika
        cls.korisnik = Korisnici.objects.create_user(
            ime='Test_Prodavac',
            prezime='Test_Prezime',
            role='Prodavac',
            username='test_user_name',
            password='test',
            email='test@example.com'
        )

    def test_queryset_exists(self):
        qs = Korisnici.objects.all()
        self.assertTrue(qs.exists())

    def test_id_korisnika_exist(self):
        # Da li postoji ID Korisnika
        korisnik_id = self.korisnik.id
        print('ID Korisnika u testnoj bazi: ' + str(korisnik_id))
        print('---------------')
        self.assertEqual(1, korisnik_id)

    def test_ime_korisnika_exist(self):
        # Da li postoji Ime Korisnika
        korisnik_ime = self.korisnik.ime
        print('IME Korisnika u testnoj bazi: ' + str(korisnik_ime))
        print('---------------')
        self.assertEqual('Test_Prodavac', korisnik_ime)

    def test_prezime_korisnika_exist(self):
        # Da li postoji prezime Korisnika
        korsinik_prezime = self.korisnik.prezime
        print('PREZIME Korisnika u testnoj bazi: ' + str(korsinik_prezime))
        print('---------------')
        self.assertEqual('Test_Prezime', korsinik_prezime)


class PasswordChange(TestCase):
    def test_change_password(self):
        c = Client()
        url = 'http://0.0.0.0:8000/korisnici/izmeni-korisnika/14/'
        payload = {'csrf_token': csrf_token, 'payload': json.dumps({'password': 'test2'})}
        headers = {'Cookie': 'csrftoken=' + csrf_token}

        res = c.post(url, payload, headers=headers)
        res = res.json()
        self.assertEqual(res['password_changed'], True)
        korisnik = Korisnici.objects.get(username='ivana')
        self.assertEqual(korisnik.check_password('test2'), True)
