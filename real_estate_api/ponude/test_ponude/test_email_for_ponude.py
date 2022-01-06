from django.core import mail
from django.core.mail import send_mail
from django.conf import settings


# TODO: napisati TESTove

def test_email_for_ponude():
    send_mail(
        subject='A cool subject',
        message='A stunning message',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.RECIPIENT_ADDRESS]
    )


def test_send_mail_for_rezervisan_stan():
    # Posalji svim preplatnicima EMAIL da je Stan REZERVISAN.
    for korisnici_email in settings.RECIPIENT_ADDRESS:
        send_mail(f'Potrebno ODOBRENJE za Stan ID: {str(1)}.',
                  f'Stan ID: {str(1)}, Adresa: {str("test adresa 1")} je rezervisan.\n'
                  f'Cena stana: {round(250000)}\n'
                  f'Cena Ponude je: {round(190000, 2)}.',
                  settings.EMAIL_HOST_USER, [korisnici_email])

        # assert len(mail.outbox) == 2, "Inbox is not empty"
        assert mail.outbox[0].subject == 'Potrebno ODOBRENJE za Stan ID: 1.'
    # Now you can test delivery and email contents

    # assert mail.outbox[0].body == 'A stunning message'
    # assert mail.outbox[0].from_email == 'stanovicrm@gmail.com'
    # assert mail.outbox[0].to == ['deanchugall@gmail.com']
