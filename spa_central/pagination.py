from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Project-wide pagination that honors ?page_size and defaults to 30.

    Frontend can provide ?page and ?page_size. We cap at a safe maximum.
    """

    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 10000


