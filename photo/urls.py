
from django.urls import path
from .views import (PhotoList,PhotoCreate,PhotoDelete,PhotoDetail,PhotoUpdate,PhotoLike,PhotoFavorite,PhotoLikeList,
                    PhotoFavoriteList,PhotoFeed,CommentDelete)

app_name = 'photo'
urlpatterns = [
    path("all_view/",PhotoList.as_view(),name="all_view"),
    path("",PhotoFeed.as_view(),name="index"),
    path("detail/<int:pk>/", PhotoDetail.as_view(), name="detail"),
    path("update/<int:pk>/",PhotoUpdate.as_view(),name="update"),
    path("create/" ,PhotoCreate.as_view(), name="create"),
    path("delete/<int:pk>/", PhotoDelete.as_view(), name="delete"),
    path("like/<int:photo_id>/",PhotoLike.as_view(),name="like"),
    path("favorite/<int:photo_id>/", PhotoFavorite.as_view(), name="favorite"),
    path("like/",PhotoLikeList.as_view(),name="like_list"),
    path("favorite/", PhotoFavoriteList.as_view(), name="favorite_list"),
    path("comment/delete/<int:pk>/", CommentDelete.as_view(), name="comment_delete"),
]
