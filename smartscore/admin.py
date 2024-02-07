from django.contrib import admin

# Register your models here.

from .models import Player, Position

admin.site.register(Player)
admin.site.register(Position)
