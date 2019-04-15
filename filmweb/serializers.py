from rest_framework import serializers
from .models import Movie, MovieComment, MovieRate,MovieSubComment
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class MovieSubCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSubComment
        fields = '__all__'


class MovieCommentSerializer(serializers.ModelSerializer):
    subcomments = MovieSubCommentSerializer(many=True, required=False)

    class Meta:
        model = MovieComment
        fields = '__all__'


class MovieRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRate
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    comments = MovieCommentSerializer(many=True, required=False)
    rates = MovieRateSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'desc', 'created_by', 'pub_date', 'comments', 'rates')

