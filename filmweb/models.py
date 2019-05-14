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
    created_by = models.ForeignKey(User, on_delete=models. CASCADE, related_name='created')
    pub_date = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(MovieCategory)
    rates_avg = models.FloatField(default=0)
    rates_count = models.IntegerField(default=0)
    favorites = models.ManyToManyField(User)

    def __str__(self):
        return self.title


   # def get_rates_average(self, obj):
    #
    #     r = obj.rates.all().aggregate(Avg('rate'))['rate__avg']
    #     if r is not None:
    #         return round(r, 1)
    #     return 0

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


class MovieReview(models.Model):

    title = models.CharField(max_length=200, null=True)
    reviewed_by = models.ForeignKey(User, related_name='reviewed_by', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE)
    desc = models.TextField()
    rate = models.FloatField(default=0)
    helped = models.ManyToManyField(User, blank=True)
    yes_votes = models.IntegerField(default=0)
    no_votes = models.IntegerField(default=0)

