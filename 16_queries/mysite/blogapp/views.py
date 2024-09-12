from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView

from .models import Article


class ArticleListView(ListView):
    queryset = (
        Article.objects
        .defer("content", "author__bio")
        .select_related("author", "category")
        .prefetch_related("tags")
    )