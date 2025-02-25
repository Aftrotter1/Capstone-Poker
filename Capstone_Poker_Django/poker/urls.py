from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib  import admin

urlpatterns = [
    path("", views.index, name="index"),
    path("logtest/", views.logtest, name="logtest"),
    path("game/", views.game, name="game"),
    path("gamechoice/", views.gamechoice, name="game"),
    path("download/", views.download, name="download"),
    path("logtext/", views.logtext, name="logtext"),
    path("custom/", views.custom, name="custom"),
    path("customgame/", views.customgame, name="customgame"),
    path('admin/', admin.site.urls,),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)