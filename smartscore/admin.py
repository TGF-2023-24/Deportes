from django.contrib import admin

# Register your models here.

from .models import Player, Position, Squad, UserProfile

admin.site.register(Player)
admin.site.register(Position)
admin.site.register(Squad)
admin.site.register(UserProfile)
