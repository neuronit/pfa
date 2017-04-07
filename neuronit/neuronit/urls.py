from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views
import spirit.urls

from django.contrib import admin

urlpatterns = [
    url(r"^play/", include("play.urls")),
    url(r"^$", views.homepage, name="home"),
    url(r"^8c6976e5b5410415bde/", include(admin.site.urls)),
    url(r"^accounts/", include("account.urls")),
    # have change account => accounts for spirit, !! Do everything still work ? !!
    url(r"^contact/", include("contact.urls"), name="contact"),
    url(r"^learn/", views.learn, name="learn"),
    url(r"^about/", include("about-us.urls"), name="about-us"),
    url(r"^leaderboard/", include("leaderboard.urls"), name="leaderboard"),
    url(r"^load/", include("load.urls"), name="load"),
    url(r"^forum/", include("spirit.urls"), name="forum"),
    url(r"^tutorial/", include("tutorial.urls"), name="tutorial"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
