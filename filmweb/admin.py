from django.contrib import admin
from .models import Movie, MovieComment, MovieRate

admin.site.register(Movie)
admin.site.register(MovieComment)
admin.site.register(MovieRate)