"""filmwebapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from filmweb import views

from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()
router.register('movies', views.MovieViewSet, base_name='Movie')
router.register('comments', views.MovieCommentViewSet, base_name='MovieComment')
router.register('subcomments', views.MovieSubCommentViewSet)
router.register('rates', views.MovieRateViewSet, base_name='MovieRate')
router.register('category', views.MovieCategoryViewSet)
router.register('reviews', views.MovieReviewViewSet, base_name='MovieReview')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]






