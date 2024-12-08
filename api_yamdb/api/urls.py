from django.urls import include, path
<<<<<<< HEAD
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, get_token,
                    signup_new_user)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('users', UserViewSet)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup_new_user, name='auth_signup'),
    path('v1/auth/token/', get_token, name='auth_token')
]
=======
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UsersViewSet, get_token,
                       signup)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', signup, name='user-registration'),
    path('v1/auth/token/', get_token, name='user_get_token'),
    path('v1/', include(router.urls)),
]
>>>>>>> users
