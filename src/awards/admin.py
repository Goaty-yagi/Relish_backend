from django.contrib import admin

from .models import Award, BaseAward

admin.site.register(Award)
admin.site.register(BaseAward)
