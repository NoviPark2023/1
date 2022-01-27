import boto3
from django.conf import settings
from docxtpl import DocxTemplate



class CreateContract:
    """Generisanje Ugovora sa predefinisanim parametrima ia CRM sistema"""

    @staticmethod
    def create_contract(ponuda, stan, kupac):
        """
        * U trenutku setovanja statusa ponuda na 'Rezervisan', Stan se smatra kaparisan.
        * Potrebno je odobrenje vlasnika-administratora sistema ove ponude @see(ponuda.odobrenje = True).
        * Takodje se setuje status Stana na 'rezervisan', @see(stan.status_prodaje = 'rezervisan').

        * Generisani Ugovor se ucitava na Digital Ocean Space.
        :param request: Ponude
        """

        session = boto3.session.Session()
        client = session.client('s3',
                                region_name='fra1',
                                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                )

        if ponuda.status_ponude == 'rezervisan':
            # Kada je status Ponude rezervisan generisi ugovor.
            # Postavi polje odobrenje na True *(ide na odobrenje).
            template = 'real_estate_api/static/ugovor/ugovor_tmpl.docx'
            document = DocxTemplate(template)
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
            document.save('real_estate_api/static/ugovor/' + 'ugovor-br-' + str(ponuda.broj_ugovora) + '.docx')


            # Ucitaj na Digital Ocean Space
            client.upload_file('real_estate_api/static/ugovor' + '/ugovor-br-' + str(ponuda.broj_ugovora) + '.docx',
                               'ugovori',
                               'ugovor-br-' + str(ponuda.broj_ugovora) + '.docx')

            # Posalji svim preplatnicima EMAIL da je Stan REZERVISAN.

            # for korisnici_email in settings.RECIPIENT_ADDRESS:
            #     send_mail(f'Potrebno ODOBRENJE za Stan ID: {str(stan.id_stana)}.',
            #               f'Stan ID: {str(stan.id_stana)}, Adresa: {str(stan.adresa_stana)} je rezervisan.\n'
            #               f'Cena stana: {round(stan.cena_stana, 2)}\n'
            #               f'Cena Ponude je: {round(ponuda.cena_stana_za_kupca, 2)}.',
            #               settings.EMAIL_HOST_USER, [korisnici_email])

        elif ponuda.status_ponude == 'kupljen':
            # Kada Ponuda predje u status 'kupljen' automatski mapiraj polje 'prodat' u modelu Stana.
            # stan.status_prodaje = 'prodat'

            pass

            # stan.save()
            # ponuda.save()

        else:
            # Kada Ponuda predje u status 'potencijalan' automatski mapiraj polje 'dostupan' u modelu Stana.
            # stan.status_prodaje = 'dostupan'

            # Obrisi ugovor jer je Stan presao u status dostupan.
            client.delete_object(Bucket='ugovori',
                                 Key='ugovor-br-' + str(ponuda.broj_ugovora) + '.docx')
            print(f' BRISANJE UGOVORA: {str(ponuda.broj_ugovora)}')
            # Stan je presao u status 'Dostupa'...nije potrebno odobrenje
            # ponuda.odobrenje = False

            # stan.save()
            # ponuda.save()

    # stan.save()
    # ponuda.save()

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
        client.delete_object(Bucket='ugovori',
                             Key='ugovor-br-' + str(ponuda.broj_ugovora) + '.docx')
        print(f' BRISANJE UGOVORA: {str(ponuda.broj_ugovora)}')
