from django.db import models
from django.contrib.auth.models import User


class MovieCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    desc = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models. CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(MovieCategory)

    def __str__(self):
        return self.title


class MovieComment(models.Model):
    desc = models.TextField()
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)


class MovieSubComment(models.Model):

    desc = models.TextField()
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_comment = models.ForeignKey(MovieComment, related_name='subcomments', on_delete=models.CASCADE)


class MovieRate(models.Model):

    rate = models.FloatField()
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='rates', on_delete=models.CASCADE)


