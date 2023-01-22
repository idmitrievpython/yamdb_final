from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (CategoriesViewSet, UserViewSet, TitleViewSet,
                    ReviewsViewSet, GenreViewSet, CommentsViewSet,
                    create_confirmation_code, signup, create_token)


router_v1 = SimpleRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', create_token, name='login'),
    path('v1/auth/code/', create_confirmation_code, name='code'),
]
