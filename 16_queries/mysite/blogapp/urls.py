from django.urls import path, include

from .views import (
    ArticleListView,
)

app_name = "blogapp"


urlpatterns = [
    path("", ArticleListView.as_view(), name="blog"),
]
