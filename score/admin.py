from django.contrib import admin
from score.models import Player, Hole, Course, Competition, Throw

@admin.register(Player)
class AddPlayer(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Course)
class AddCourse(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Hole)
class AddHole(admin.ModelAdmin):
    list_display = ('course', 'number', 'par',)

@admin.register(Competition)
class AddComp(admin.ModelAdmin):
    list_display = ('course', 'date', 'game_number', 'notes')

@admin.register(Throw)
class AddCourse(admin.ModelAdmin):
    list_display = ('competition', 'hole', 'throws', 'player')