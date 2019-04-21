from django.contrib.auth.models import User
from .models import Movie, MovieComment, MovieRate, MovieSubComment, MovieCategory
from rest_framework import viewsets
from .serializers import (
    UserSerializer,
    MovieSubCommentSerializer,
    MovieCommentSerializer,
    MovieRateSerializer,
    MovieSerializer,
    MovieCategorySerializer
    )
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters



class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('categories',)
    search_fields = ('title', 'year',)


    # def list(self, request):
    #
    #     queryset = Movie.objects.all()
    #     serializer = MovieSerializer(queryset, many=True)
    #
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #
    #     queryset = Movie.objects.all()
    #     movie = get_object_or_404(queryset, pk=pk)
    #     serializer = MovieSerializer(movie)
    #
    #     return Response(serializer.data)
    #     # rates = movie.rates.all()
    #     #
    #     # rates_sum = 0
    #     #
    #     # for r in rates:
    #     #     rates_sum += r.rate
    #     # rates_average = round(rates_sum / len(rates), 1)
    #     # return Response({'data': serializer.data, 'meta': {"rates_average": rates_average}})
    #
    #
    #
    # def create(self, request, *args, **kwargs):
    #
    #     serializer = MovieSerializer(data=request.data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #
    #         return Response()
    #
    #     return Response(serializer.errors, 400)
    #
    # def destroy(self, request, pk=None):
    #
    #     queryset = Movie.objects.get(pk=pk)
    #     queryset.delete()
    #
    #     return Response(204)

    @action(detail=True)
    def comments(self, request, pk=None):
        movie = Movie.objects.get(pk=pk)
        comments = MovieCommentSerializer(movie.comments.all(), many=True)
        return Response(comments.data)





class MovieCommentViewSet(viewsets.ModelViewSet):

    queryset = MovieComment.objects.all()
    serializer_class = MovieCommentSerializer

    @action(detail=True)
    def subcomments(self, request, pk=None):
        moviecomment = MovieComment.objects.get(pk=pk)
        subcomments = MovieSubCommentSerializer(moviecomment.subcomments.all(), many=True)
        return Response(subcomments.data)

class MovieSubCommentViewSet(viewsets.ModelViewSet):

    queryset = MovieSubComment.objects.all()
    serializer_class = MovieSubCommentSerializer

class RateViewSet(viewsets.ModelViewSet):
    queryset = MovieRate.objects.all()
    serializer_class = MovieRateSerializer

class MovieCategoryViewSet(viewsets.ModelViewSet):
    queryset = MovieCategory.objects.all()
    serializer_class = MovieCategorySerializer
