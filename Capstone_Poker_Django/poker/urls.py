from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib  import admin
from .views import RegisterView
from django.contrib.auth import views as auth_views
from poker.views import CustomLoginView  
from poker.forms import LoginForm
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [    
    path("index/", views.index, name="index"),
    path("logtest/", views.logtest, name="logtest"),
    path("game/", views.game, name="game"),
    path("gamechoice/", views.gamechoice, name="game"),
    path("download/", views.download, name="download"),
    path("logtext/", views.logtext, name="logtext"),
    path("custom/", views.custom, name="custom"),
    path("customgame/", views.customgame, name="customgame"),
    path('admin/', admin.site.urls,),
    path("profile/", views.profile, name="profile"),
    path("adminprofile/", views.adminprofile, name="adminprofile"),
    path("runtourney/", views.runtourney, name="runtourney"),
    path("profilechoice/", views.profilechoice, name="profilechoice"),
    path('',views.begin,name="begin"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='loginstu.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('tournament-history/', views.tournament_history, name='tourney_history'),
    path('run-student/', views.runstudent, name='run-student'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
    path('redirect_shortener/', views.redirect_shortener, name='redirect_shortener'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)