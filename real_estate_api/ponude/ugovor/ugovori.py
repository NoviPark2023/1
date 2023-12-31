import threading
from smtplib import SMTPException

import boto3
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from docxtpl import DocxTemplate


class Contract:
    """Generisanje Ugovora sa predefinisanim parametrima ia CRM sistema"""

    @staticmethod
    def create_contract(ponuda, stan, kupac):
        """
        * U trenutku setovanja statusa ponuda na 'Rezervisan', Stan se smatra kaparisan.
        * Potrebno je odobrenje vlasnika-administratora sistema ove ponude @see(ponuda.odobrenje = True).
        * Takodje se setuje status Stana na 'rezervisan', @see(stan.status_prodaje = 'rezervisan').

        * Generisani Ugovor se ucitava na Digital Ocean Space.
        :param ponuda: Entitet Ponuda
        :param stan: Entitet Stan
        :param kupac: Entitet Kupac
        """

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                )

        template = 'real_estate_api/static/ugovor/ugovor_tmpl.docx'
        document = DocxTemplate(template)

        # Ako je status Ponude "REZERVISAN" ili "KUPLJEN", generisi ugovor.
        if (
            ponuda.status_ponude == ponuda.StatusPonude.REZERVISAN
            or
            ponuda.status_ponude == ponuda.StatusPonude.KUPLJEN
        ):
            context = {
                'id_stana': stan.id_stana,
                'datum_ugovora': ponuda.datum_ugovora.strftime("%d.%m.%Y."),
                'broj_ugovora': ponuda.broj_ugovora,
                'kupac': kupac.ime_prezime,
                'adresa_kupaca': kupac.adresa,
                'kvadratura': stan.kvadratura,
                'cena_stana': ponuda.cena_stana_za_kupca,
                # 'nacin_placanja': nacin_placanja
            }

            document.render(context)

            # Sacuvaj generisani Ugovor.
            document.save(
                'real_estate_api/static/ugovor/' +
                'ugovor-br-' + str(ponuda.id_ponude) + '-' + str(stan.lamela) + '.docx'
            )

            # Ucitaj na Digital Ocean Space
            client.upload_file(
                'real_estate_api/static/ugovor/' +
                'ugovor-br-' + str(ponuda.id_ponude) + '-' + str(stan.lamela) + '.docx',
                'ugovori',
                'ugovor-br-' + str(ponuda.id_ponude) + '-' + str(stan.lamela) + '.docx'
            )

        if ponuda.status_ponude == ponuda.StatusPonude.REZERVISAN:
            # Posalji svim preplatnicima EMAIL da je Stan REZERVISAN.
            SendEmailThreadRezervisanStan(ponuda).start()
        else:
            # Posalji Email da je Stan KUPLJEN.
            SendEmailThreadKupljenStan(ponuda).start()

    @staticmethod
    def delete_contract(ponuda):
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                )

        # Obrisi ugovor jer je Stan presao u status dostupan.
        client.delete_object(
            Bucket='ugovori',
            Key='ugovor-br-' + str(ponuda.id_ponude) + '-' + str(ponuda.stan.lamela) + '.docx'
        )


class SendEmailThreadKupljenStan(threading.Thread):
    """Posalji Email pretplacenim Korisnicima kada je Stan KUPLJEN"""

    def __init__(self, ponuda):
        self.ponuda = ponuda
        threading.Thread.__init__(self)

    def run(self):
        subject = f'Kupovina Stana ID: {str(self.ponuda.stan.id_stana)}.'
        message = (
            f'Stan ID: {str(self.ponuda.stan.id_stana)}.\n'
            f'Adresa stana: {str(self.ponuda.stan.adresa_stana)}.\n'
            f'Lamela stana: {str(self.ponuda.stan.lamela)}.\n'
            f'Kvadratura stana: {str(self.ponuda.stan.kvadratura)}.\n'
            f'Kvadratura stana (sa korekcijom): {str(self.ponuda.stan.kvadratura_korekcija)}.\n'
            f'Cena kvadrata: {str(self.ponuda.stan.cena_kvadrata)}.\n'
            f'Sprat stana: {str(self.ponuda.stan.sprat)}.\n'
            f'Kupac stana: {str(self.ponuda.kupac.ime_prezime)}.\n'
            f'Cena stana: {round(self.ponuda.stan.cena_stana, 2)}\n'
            f'Cena stana za kupca: {round(self.ponuda.cena_stana_za_kupca, 2)}.'
        )
        from_email = settings.EMAIL_HOST_USER
        html_message = loader.render_to_string(
            'receipt_email-stanovi.html',
            {
                'id_stana': self.ponuda.stan.id_stana,
                'adresa': self.ponuda.stan.adresa_stana,
                'lamela': self.ponuda.stan.lamela,
                'kvadratura': self.ponuda.stan.kvadratura,
                'kvadratura_korekcija': self.ponuda.stan.kvadratura_korekcija,
                'cena_kvadrata': self.ponuda.stan.cena_kvadrata,
                'sprat': self.ponuda.stan.sprat,
                'kupac': self.ponuda.kupac.ime_prezime,
                'cena_stana': round(self.ponuda.stan.cena_stana, 2),
                'cena_ponude': round(self.ponuda.cena_stana_za_kupca, 2),
                'url_ponude': f'https://stanovi.biz/ponude?id={self.ponuda.id_ponude}',
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


class SendEmailThreadRezervisanStan(threading.Thread):
    """Posalji Email pretplacenim Korisnicima kada je Stan REZERVISAN"""

    def __init__(self, ponuda):
        self.ponuda = ponuda
        threading.Thread.__init__(self)

    def run(self):
        subject = f'Rezervacija Stana ID: {str(self.ponuda.stan.id_stana)}.'
        message = (
            f'Stan ID: {str(self.ponuda.stan.id_stana)}.\n'
            f'Adresa stana: {str(self.ponuda.stan.adresa_stana)} je kupljen.\n'
            f'Lamela stana: {str(self.ponuda.stan.lamela)}.\n'
            f'Kvadratura stana: {str(self.ponuda.stan.kvadratura)}.\n'
            f'Kvadratura stana (sa korekcijom): {str(self.ponuda.stan.kvadratura_korekcija)}.\n'
            f'Cena kvadrata: {str(self.ponuda.stan.cena_kvadrata)}.\n'
            f'Sprat stana: {str(self.ponuda.stan.sprat)}.\n'
            f'Kupac stana: {str(self.ponuda.kupac.ime_prezime)}.\n'
            f'Cena stana: {round(self.ponuda.stan.cena_stana, 2)}\n'
            f'Cena stana za kupca: {round(self.ponuda.cena_stana_za_kupca, 2)}.'
        )
        from_email = settings.EMAIL_HOST_USER
        html_message = loader.render_to_string(
            'receipt_email-stanovi.html',
            {
                'id_stana': self.ponuda.stan.id_stana,
                'adresa': self.ponuda.stan.adresa_stana,
                'lamela': self.ponuda.stan.lamela,
                'kvadratura': self.ponuda.stan.kvadratura,
                'kvadratura_korekcija': self.ponuda.stan.kvadratura_korekcija,
                'cena_kvadrata': self.ponuda.stan.cena_kvadrata,
                'sprat': self.ponuda.stan.sprat,
                'kupac': self.ponuda.kupac.ime_prezime,
                'cena_stana': round(self.ponuda.stan.cena_stana, 2),
                'cena_ponude': round(self.ponuda.cena_stana_za_kupca, 2),
                'url_ponude': f'https://stanovi.biz/ponude?id={self.ponuda.id_ponude}',
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
