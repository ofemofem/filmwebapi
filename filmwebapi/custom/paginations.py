from rest_framework import pagination
from rest_framework.response import Response

class BasePagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):

        return Response({
            'pagination': {
                'total': self.page.paginator.count,
                'per_page': self.page_size,
                'current': self.page.number
            },
            'results': data
        })