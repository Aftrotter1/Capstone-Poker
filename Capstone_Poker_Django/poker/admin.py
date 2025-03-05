from django.contrib import admin
from .models import StudentBot
from .models import BaseBot
from .models import Profile
# Register your models here.
admin.site.register(StudentBot)
admin.site.register(BaseBot)

admin.site.register(Profile)