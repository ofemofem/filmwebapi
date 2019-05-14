from .models import Movie, MovieComment, MovieRate, MovieSubComment, MovieCategory, MovieReview
from django.db.models import Avg
from django.contrib.auth import get_user_model
from rest_framework import serializers


class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReview
        fields = '__all__'

class MovieCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieCategory
        fields = '__all__'

class MovieSubCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSubComment
        fields = '__all__'


class MovieCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieComment
        fields = '__all__'


class MovieRateSerializer(serializers.ModelSerializer):
    rate = serializers.FloatField(max_value=10, min_value=1)

    class Meta:
        model = MovieRate
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    # comments = MovieCommentSerializer(many=True, required=False)
    # rates = MovieRateSerializer(many=True, required=False)
    categories = MovieCategorySerializer(read_only=True, many=True)
    # rates_average = serializers.SerializerMethodField()
    #
    # def get_rates_average(self, obj):
    #
    #     r = obj.rates.all().aggregate(Avg('rate'))['rate__avg']
    #     if r is not None:
    #         return round(r, 1)
    #     return 0


    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'desc', 'created_by', 'pub_date', 'categories', 'rates_avg', 'rates_count')



