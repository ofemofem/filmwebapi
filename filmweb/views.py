
from .models import Movie, MovieComment, MovieRate, MovieSubComment, MovieCategory, MovieReview
from rest_framework import viewsets
from .serializers import (
    MovieSubCommentSerializer,
    MovieCommentSerializer,
    MovieRateSerializer,
    MovieSerializer,
    MovieCategorySerializer,
    MovieReviewSerializer
    )
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from django.db.models import Avg


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('categories',)
    search_fields = ('title', 'year',)
    ordering_fields = ('year', 'rates_avg', 'rates_count')
    # permission_classes = (IsAuthenticated,)

    # def rates_average(self):
    #     return Movie.annotate(rates_average=Avg('Movie__rates'))


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

        # serializer = MovieSerializer(data=request.data)
        #
        # if serializer.is_valid():
        #     serializer.save()
        #
        #     return Response()
        #
        # return Response(serializer.errors, 400)

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

    @action(detail=True)
    def reviews(self, request, pk=None):
        movie = Movie.objects.get(pk=pk)
        reviews = MovieReviewSerializer(movie.reviews.all(), many=True)
        return Response(reviews.data)


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

class MovieRateViewSet(viewsets.ViewSet):

    def list(self, request):
        rates = MovieRate.objects.all()
        serializer = MovieRateSerializer(rates, many=True)

        return Response(serializer.data)

    def create(self, request):
        serializer = MovieRateSerializer(data=request.data)

        if serializer.is_valid():

            try:
                current_rate = MovieRate.objects.get(movie=request.data['movie'], rated_by=request.data['rated_by'])
                # SELECT * FROM movie_rate WHERE movie = 8 AND rated_by = 1
            except MovieRate.DoesNotExist:
                current_rate = False

            rated_movie = Movie.objects.get(pk=request.data['movie'])

            if current_rate:
                 if current_rate.rate == request.data['rate']:

                    # usunac ten glos z bazy
                    current_rate.delete()
                    if rated_movie.rates_count == 1:
                        rated_movie.rates_avg = 0
                        rated_movie.rates_count = 0

                    else:
                        rated_movie.rates_avg = (rated_movie.rates_count * rated_movie.rates_avg - request.data['rate']) / (rated_movie.rates_count - 1)
                        rated_movie.rates_count -= 1

                    rated_movie.save()
                    return Response({'message': 'Twoj glos zostal usuniety!'})
                 else:
                     # update glos

                    rated_movie.rates_avg = (rated_movie.rates_count * rated_movie.rates_avg - current_rate.rate + request.data['rate']) / rated_movie.rates_count
                    rated_movie.save()

                    current_rate.rate = request.data['rate']
                    current_rate.save()
                    return Response({'message': 'Twoj glos zostal zaktualizowny!'})

            if not current_rate:
                # INSERT INTO movie_rate VALUES ...
                serializer.save()

                rated_movie.rates_avg = (rated_movie.rates_count * rated_movie.rates_avg + request.data['rate'])/(rated_movie.rates_count +1)
                rated_movie.rates_count += 1
                rated_movie.save()

                return Response({'message': 'Your rating has been saved'})

            # return Response({'errors': 'You can not vote again'}, 403)

        return Response(serializer.errors, 400)

    @action(methods=['post'], detail=False)
    def destroy_all(self, request):

        queryset = MovieRate.objects.all()
        queryset.delete()

        return Response(204)

class MovieCategoryViewSet(viewsets.ModelViewSet):
    queryset = MovieCategory.objects.all()
    serializer_class = MovieCategorySerializer


class MovieReviewViewSet(viewsets.ModelViewSet):

    queryset = MovieReview.objects.all()
    serializer_class = MovieReviewSerializer

    @action(methods=['post'], detail=True)
    def votes(self, request, pk=None):
        movie_review = MovieReview.objects.get(pk=pk)
        if request.data['vote'] == 1:
            movie_review.yes_votes += 1
        else:
            movie_review.no_votes += 1

        movie_review.save()
        return Response(204)