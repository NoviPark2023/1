import self as self
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTestCase(TestCase):

    def test_kupce_sa_ispravnim_emailmo(self):
        """Testiranje kreiranje kupaca ako je email ispravane"""
        email = 'test@example.com'
        password = 'testpassword'
        korisnik = get_user_model().objects.create(
            email=email,
            password=password
        )

        self.assertEqual(korisnik.email, email)
        self.assertTrue(korisnik.check_password(password))

