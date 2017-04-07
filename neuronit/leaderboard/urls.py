from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.leaderboard, name="leaderboard"),
    url(r'^(\d+)$', views.leaderboard, name="leaderboard")
]
