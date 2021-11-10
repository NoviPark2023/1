from rest_framework.pagination import PageNumberPagination


class StandardPaginationKorisnici(PageNumberPagination):
    """Standardna paginacija sa 5 prikaza po stranici za Korisnike"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5