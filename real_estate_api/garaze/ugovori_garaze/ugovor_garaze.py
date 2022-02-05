import threading
from smtplib import SMTPException

import boto3
from django.conf import settings
from django.core.mail import send_mail
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

        if garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.REZERVISANA:
            # Kada je status Ponude Garaze 'rezervisan' generisi ugovor.
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
                'real_estate_api/static/ugovori-garaze/' + 'ugovor-garaze-br-' + str(garaza.id_garaze) + '.docx'
            )

            # Ucitaj na Digital Ocean Space
            client_garaze.upload_file(
                'real_estate_api/static/ugovori-garaze' + '/ugovor-garaze-br-' + str(garaza.id_garaze) + '.docx',
                'ugovori-garaze',
                'ugovor-garaze-br-' + str(garaza.id_garaze) + '.docx'
            )

            # Posalji svim preplatnicima EMAIL da je Stan REZERVISAN.
            # SendEmailThreadRezervisanStan(ponuda).start()

        elif garaza.status_prodaje_garaze == Garaze.StatusProdajeGaraze.PRODATA:
            # Kada je status Ponude Garaze kupjena, generisi ugovor.
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
                'real_estate_api/static/ugovori-garaze/' + 'ugovor-garaze-br-' + str(garaza.id_garaze) + '.docx'
            )

            # Ucitaj na Digital Ocean Space
            client_garaze.upload_file(
                'real_estate_api/static/ugovori-garaze' + '/ugovor-garaze-br-' + str(garaza.id_garaze) + '.docx',
                'ugovori-garaze',
                'ugovor-garaze-br-' + str(garaza.id_garaze) + '.docx'
            )

            # Posalji Email da je Stan kupljen.
            # SendEmailThreadKupljenStan(ponuda).start()

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
