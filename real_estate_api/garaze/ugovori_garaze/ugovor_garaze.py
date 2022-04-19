import threading
from smtplib import SMTPException

import boto3
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from docxtpl import DocxTemplate

from real_estate_api.garaze.models import Garaze


class ContractGaraze:
    """Generisanje Ugovora za prodaju Garaza sa predefinisanim parametrima ia CRM sistema"""

    @staticmethod
    def create_contract(garaza, kupac):

        session_boto_garaze = boto3.session.Session()

        client_garaze = session_boto_garaze.client('s3',
                                                   region_name='fra1',
                                                   endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                                   )

        template_ugovora_garaze = 'real_estate_api/static/ugovori-garaze/ugovor_garaze_tmpl.docx'

        document_garaze = DocxTemplate(template_ugovora_garaze)

        # Ako je status Ponude Garaze 'REZERVISAN' ili 'PRODATA', generisi ugovor.
        if (
            garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.REZERVISANA
            or
            garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.PRODATA
        ):
            context = {
                'id_garaze': garaza.id_garaze,
                'datum_ugovora_garaze': garaza.datum_ugovora_garaze,
                'broj_ugovora_garaze': garaza.broj_ugovora_garaze,
                'kupac': kupac.ime_prezime,
                'adresa_kupaca': kupac.adresa,
                'cena_garaze': garaza.cena_garaze,
                # 'nacin_placanja': nacin_placanja
            }

            document_garaze.render(context)

            # Sacuvaj generisani Ugovor.
            document_garaze.save(
                'real_estate_api/static/ugovori-garaze/' + 'ugovor-garaze-br-' + str(
                    garaza.jedinstveni_broj_garaze) + '.docx'
            )

            # Ucitaj na Digital Ocean Space
            client_garaze.upload_file(
                'real_estate_api/static/ugovori-garaze' + '/ugovor-garaze-br-' + str(
                    garaza.jedinstveni_broj_garaze) + '.docx',
                'ugovori-garaze',
                'ugovor-garaze-br-' + str(garaza.jedinstveni_broj_garaze) + '.docx'
            )

        if garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.REZERVISANA:
            # Posalji svim preplatnicima EMAIL da je Garaza REZERVISAN.
            SendEmailThreadRezervisanaGaraza(garaza).start()
        else:
            # Posalji Email da je Garaza kupljena.
            SendEmailThreadKupljenaGaraza(garaza).start()

    @staticmethod
    def delete_contract(garaza):
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                )

        # Obrisi ugovor jer je Stan presao u status dostupan.
        client.delete_object(Bucket='ugovori-garaze',
                             Key='ugovor-garaze-br-' + str(garaza.id_garaze) + '.docx')


class SendEmailThreadKupljenaGaraza(threading.Thread):
    """Posalji Email pretplacenim Korisnicima kada je garaza KUPLJENA"""

    def __init__(self, garaza):
        self.garaza = garaza
        threading.Thread.__init__(self)

    def run(self):
        subject = f'Kupovina Garaže ID: {str(self.garaza.jedinstveni_broj_garaze)}.'
        message = (
            f'Garaža ID: {str(self.garaza.id_garaze)}.\n'
            f'Jedinstveni broj garaže: {str(self.garaza.jedinstveni_broj_garaze)}.\n'
            f'Cena garaže: {str(self.garaza.cena_garaze)}.\n'
            f'Kupac garaže: {str(self.garaza.kupac.ime_prezime)}.\n'
        )
        from_email = settings.EMAIL_HOST_USER
        html_message = loader.render_to_string(
            'receipt_email-garaze.html',
            {
                'id_garaze': self.garaza.id_garaze,
                'jedinstveni_broj_garaze': self.garaza.jedinstveni_broj_garaze,
                'cena_garaze': self.garaza.cena_garaze,
                'kupac': self.garaza.kupac.ime_prezime,

            }
        )
        try:
            for korisnici_email in settings.RECIPIENT_ADDRESS:
                send_mail(
                    subject,
                    message,
                    from_email,
                    [korisnici_email],
                    fail_silently=True,
                    html_message=html_message
                )
        except SMTPException as e:
            print(f"failed to send mail: {e}")

class SendEmailThreadRezervisanaGaraza(threading.Thread):
    """Posalji Email pretplacenim Korisnicima kada je garaza REZERVISANA"""

    def __init__(self, garaza):
        self.garaza = garaza
        threading.Thread.__init__(self)

    def run(self):
        subject = f'Rezervacija Garaže ID: {str(self.garaza.jedinstveni_broj_garaze)}.'
        message = (
            f'Garaža ID: {str(self.garaza.id_garaze)}.\n'
            f'Jedinstveni broj garaže: {str(self.garaza.jedinstveni_broj_garaze)}.\n'
            f'Cena garaže: {str(self.garaza.cena_garaze)}.\n'
            f'Kupac garaže: {str(self.garaza.kupac.ime_prezime)}.\n'
        )
        from_email = settings.EMAIL_HOST_USER
        html_message = loader.render_to_string(
            'receipt_email-garaze.html',
            {
                'id_garaze': self.garaza.id_garaze,
                'jedinstveni_broj_garaze': self.garaza.jedinstveni_broj_garaze,
                'cena_garaze': self.garaza.cena_garaze,
                'kupac': self.garaza.kupac.ime_prezime,

            }
        )
        try:
            for korisnici_email in settings.RECIPIENT_ADDRESS:
                send_mail(
                    subject,
                    message,
                    from_email,
                    [korisnici_email],
                    fail_silently=True,
                    html_message=html_message
                )
        except SMTPException as e:
            print(f"failed to send mail: {e}")
