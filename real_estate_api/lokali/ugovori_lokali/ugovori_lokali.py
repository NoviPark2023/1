import threading
from smtplib import SMTPException

import boto3
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from docxtpl import DocxTemplate


class ContractLokali:
    """Generisanje Ugovora za prodaju Lokala sa predefinisanim parametrima ia CRM sistema"""

    @staticmethod
    def create_contract(ponude_lokala, lokal, kupac_lokala):
        session_boto_lokali = boto3.session.Session()

        client_lokali = session_boto_lokali.client('s3',
                                                   region_name='fra1',
                                                   endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                                   )

        template_ugovora_lokala = 'real_estate_api/static/ugovori-lokali/ugovor_lokali_tmpl.docx'

        document_lokali = DocxTemplate(template_ugovora_lokala)

        # Ako je status Ponude Lokala "REZERVISAN" ili "KUPLJEN", generisi ugovor.
        if (
            ponude_lokala.status_ponude_lokala == ponude_lokala.StatusPonudeLokala.REZERVISAN
            or
            ponude_lokala.status_ponude_lokala == ponude_lokala.StatusPonudeLokala.KUPLJEN
        ):
            context = {
                'id_lokala': lokal.id_lokala,
                'datum_ugovora_lokala': ponude_lokala.datum_ugovora_lokala.strftime("%d.%m.%Y."),
                'broj_ugovora_lokala': ponude_lokala.broj_ugovora_lokala,
                'kupac_lokala': kupac_lokala.ime_prezime,
                'adresa_kupaca_lokala': kupac_lokala.adresa,
                'kvadratura_lokala': lokal.kvadratura_lokala,
                'cena_lokala': ponude_lokala.cena_lokala_za_kupca,
                'nacin_placanja_lokala': ponude_lokala.nacin_placanja_lokala
            }

            document_lokali.render(context)

            # Sacuvaj generisani Ugovor.
            document_lokali.save(
                'real_estate_api/static/ugovori-lokali/' +
                'ugovor-lokala-br-' + str(ponude_lokala.id_ponude_lokala) + '-' + str(lokal.lamela_lokala) + '.docx'
            )

            # Ucitaj na Digital Ocean Space
            client_lokali.upload_file(
                'real_estate_api/static/ugovori-lokali/' +
                'ugovor-lokala-br-' + str(ponude_lokala.id_ponude_lokala) + '-' + str(lokal.lamela_lokala) + '.docx',
                'ugovori-lokali',
                'ugovor-lokala-br-' + str(ponude_lokala.id_ponude_lokala) + '-' + str(lokal.lamela_lokala) + '.docx'
            )

            if ponude_lokala.status_ponude_lokala == ponude_lokala.StatusPonudeLokala.REZERVISAN:
                # Posalji Email-s da je LOKAL REZERVISAN.
                SendEmailThreadRezervisanLokal(ponude_lokala).start()
            else:
                # Posalji Email-s da je LOKAL KUPLJEN.
                SendEmailThreadKupljenLokal(ponude_lokala).start()

    @staticmethod
    def delete_contract(ponude_lokala):
        session_boto_lokali = boto3.session.Session()

        client_lokali = session_boto_lokali.client(
            's3',
            region_name='fra1',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        # Obrisi ugovor jer je Lokal presao u status "DOSTUPAN".
        client_lokali.delete_object(
            Bucket='ugovori-lokali',
            Key='ugovor-lokala-br-' +
                str(ponude_lokala.id_ponude_lokala) +
                '-' +
                str(ponude_lokala.lokali.lamela_lokala) +
                '.docx'
        )


class SendEmailThreadKupljenLokal(threading.Thread):
    """Posalji Email pretplacenim Korisnicima kada je LOKAL KUPLJEN"""

    def __init__(self, ponuda_lokala):
        self.ponuda_lokala = ponuda_lokala
        threading.Thread.__init__(self)

    def run(self):
        subject = f'Kupovina Lokala ID: {str(self.ponuda_lokala.lokali.id_lokala)}.'
        message = (
            f'Lokal ID: {str(self.ponuda_lokala.lokali.id_lokala)}.\n'
            f'Adresa lokala: {str(self.ponuda_lokala.lokali.adresa_lokala)}.\n'
            f'Lamela lokala: {str(self.ponuda_lokala.lokali.lamela_lokala)}.\n'
            f'Kvadratura lokala: {str(self.ponuda_lokala.lokali.kvadratura_lokala)}.\n'
            f'Kupac lokala: {str(self.ponuda_lokala.kupac_lokala.ime_prezime)}.\n'
            f'Cena lokala: {round(self.ponuda_lokala.lokali.cena_lokala, 2)}\n'
            f'Cena lokala za kupca: {round(self.ponuda_lokala.cena_lokala_za_kupca, 2)}.'
        )
        from_email_lokali = settings.EMAIL_HOST_USER
        html_message_lokali = loader.render_to_string(
            'receipt_email-lokali.html',
            {
                'id_lokala': self.ponuda_lokala.lokali.id_lokala,
                'adresa_lokala': self.ponuda_lokala.lokali.adresa_lokala,
                'lamela_lokala': self.ponuda_lokala.lokali.lamela_lokala,
                'kvadratura_lokala': self.ponuda_lokala.lokali.kvadratura_lokala,
                'kupac_lokala': self.ponuda_lokala.kupac_lokala.ime_prezime,
                'cena_lokala': round(self.ponuda_lokala.lokali.cena_lokala, 2),
                'cena_lokala_za_kupca': round(self.ponuda_lokala.cena_lokala_za_kupca, 2),
                'url_ponude_lokala': f'https://stanovi.biz/ponude-lokala?id={self.ponuda_lokala.id_ponude_lokala}',
            }
        )
        try:
            for korisnici_email in settings.RECIPIENT_ADDRESS:
                send_mail(
                    subject,
                    message,
                    from_email_lokali,
                    [korisnici_email],
                    fail_silently=True,
                    html_message=html_message_lokali
                )
        except SMTPException as e:
            print(f"failed to send mail: {e}")


class SendEmailThreadRezervisanLokal(threading.Thread):
    """Posalji Email pretplacenim Korisnicima kada je LOKAL REZERVISAN"""

    def __init__(self, ponuda_lokala):
        self.ponuda_lokala = ponuda_lokala
        threading.Thread.__init__(self)

    def run(self):
        subject = f'Rezervacija Lokala ID: {str(self.ponuda_lokala.lokali.id_lokala)}.'
        message = (
            f'Lokal ID: {str(self.ponuda_lokala.lokali.id_lokala)}.\n'
            f'Adresa lokala: {str(self.ponuda_lokala.lokali.adresa_lokala)}.\n'
            f'Lamela lokala: {str(self.ponuda_lokala.lokali.lamela_lokala)}.\n'
            f'Kvadratura lokala: {str(self.ponuda_lokala.lokali.kvadratura_lokala)}.\n'
            f'Kupac lokala: {str(self.ponuda_lokala.kupac_lokala.ime_prezime)}.\n'
            f'Cena lokala: {round(self.ponuda_lokala.lokali.cena_lokala, 2)}\n'
            f'Cena lokala za kupca: {round(self.ponuda_lokala.cena_lokala_za_kupca, 2)}.'
        )
        from_email_lokali = settings.EMAIL_HOST_USER
        html_message_lokali = loader.render_to_string(
            'receipt_email-lokali.html',
            {
                'id_lokala': self.ponuda_lokala.lokali.id_lokala,
                'adresa_lokala': self.ponuda_lokala.lokali.adresa_lokala,
                'lamela_lokala': self.ponuda_lokala.lokali.lamela_lokala,
                'kvadratura_lokala': self.ponuda_lokala.lokali.kvadratura_lokala,
                'kupac_lokala': self.ponuda_lokala.kupac_lokala.ime_prezime,
                'cena_lokala': round(self.ponuda_lokala.lokali.cena_lokala, 2),
                'cena_lokala_za_kupca': round(self.ponuda_lokala.cena_lokala_za_kupca, 2),
                'url_ponude_lokala': f'https://stanovi.biz/ponude-lokala?id={self.ponuda_lokala.id_ponude_lokala}',
            }
        )
        try:
            for korisnici_email in settings.RECIPIENT_ADDRESS:
                send_mail(
                    subject,
                    message,
                    from_email_lokali,
                    [korisnici_email],
                    fail_silently=True,
                    html_message=html_message_lokali
                )
        except SMTPException as e:
            print(f"failed to send mail: {e}")
