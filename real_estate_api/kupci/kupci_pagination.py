from rest_framework.pagination import PageNumberPagination


class StandardPaginationKupci(PageNumberPagination):
    """Standart paginacija sa 5 prikaza po stranici za Kupce"""
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 5
