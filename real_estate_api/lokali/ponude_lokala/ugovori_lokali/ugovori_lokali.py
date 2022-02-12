import boto3
from django.conf import settings
from docxtpl import DocxTemplate


class ContractLokali:
    """Generisanje Ugovora za prodaju Lokala sa predefinisanim parametrima ia CRM sistema"""

    @staticmethod
    def create_contract(lokal, kupac):
        session_boto_lokali = boto3.session.Session()

        client_lokali = session_boto_lokali.client('s3',
                                                   region_name='fra1',
                                                   endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                                                   )

        template_ugovora_lokala = 'real_estate_api/static/ugovori-lokali/ugovor_lokali_tmpl.docx'

        document_lokali = DocxTemplate(template_ugovora_lokala)

        # TODO(Dex): Implement rest of creating Ugovor for Lokali.
