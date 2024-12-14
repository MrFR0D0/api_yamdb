from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
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
    CommentViewSet,
    basename='comments'
)
router.register('users', UsersViewSet, basename='users')

auth = [
    path('signup/', signup, name='user-registration'),
    path('token/', get_token, name='user_get_token'),
]

api = [
    path('auth/', include(auth)),
    path('', include(router.urls)),
]

urlpatterns = [path('v1/', include(api))]
