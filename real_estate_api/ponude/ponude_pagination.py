from rest_framework.pagination import PageNumberPagination


class StandardPaginationPonude(PageNumberPagination):
    """Standardna paginacija sa 5 prikaza po stranici za Ponude"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5
