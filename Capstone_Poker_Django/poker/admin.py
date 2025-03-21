from django.contrib import admin
from .models import StudentBot
from .models import BaseBot
from .models import Profile
from .models import Tournament
from .models import TournamentData
# Register your models here.
admin.site.register(StudentBot)
admin.site.register(BaseBot)

admin.site.register(Profile)

admin.site.register(Tournament)

admin.site.register(TournamentData)