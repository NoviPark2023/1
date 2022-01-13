from django.conf import settings
from django.core import mail
from django.core.mail import send_mail


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

        assert mail.outbox[0].subject == 'Potrebno ODOBRENJE za Stan ID: 1.'

    assert len(mail.outbox) == 3, "Inbox is not empty"
    assert mail.outbox[0].body == (
        "Stan ID: 1, Adresa: test adresa 1 je rezervisan.\n"
        "Cena stana: 250000\n"
        "Cena Ponude je: 190000."
    )
    assert mail.outbox[0].from_email == settings.EMAIL_HOST_USER

    print("\n")
    print(f' REC 1: {settings.RECIPIENT_ADDRESS[0]}')
    print(f' REC 1: {settings.RECIPIENT_ADDRESS[1]}')
    print(f' REC 1: {settings.RECIPIENT_ADDRESS[2]}')
    print('############################')
    print(f" mail.outbox[0].to: {(', '.join(mail.outbox[0].to))}")
    print(f" mail.outbox[0].to: {(', '.join(mail.outbox[1].to))}")
    print(f" mail.outbox[0].to: {(', '.join(mail.outbox[2].to))}")

    assert (', '.join(mail.outbox[0].to)) == settings.RECIPIENT_ADDRESS[0]
    assert (', '.join(mail.outbox[1].to)) == settings.RECIPIENT_ADDRESS[1]
    assert (', '.join(mail.outbox[2].to)) == settings.RECIPIENT_ADDRESS[2]
