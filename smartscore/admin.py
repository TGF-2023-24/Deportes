from django.contrib import admin

# Register your models here.

from .models import Player, Position, Squad, UserProfile, League, Shortlist

admin.site.register(Player)
admin.site.register(Position)
admin.site.register(Squad)
admin.site.register(UserProfile)
admin.site.register(League)
admin.site.register(Shortlist)