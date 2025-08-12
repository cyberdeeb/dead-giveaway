from django.contrib import admin
from .models import Case, Suspect, Clue, ClueImplication, RedHerring


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'setting', 'difficulty', 'num_suspects', 'num_clues', 'created_at']
    list_filter = ['difficulty', 'created_at']
    search_fields = ['title', 'setting']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Suspect)
class SuspectAdmin(admin.ModelAdmin):
    list_display = ['sid', 'name', 'case', 'bio']
    list_filter = ['case']
    search_fields = ['name', 'sid', 'bio']
    ordering = ['case', 'sid']


@admin.register(Clue)
class ClueAdmin(admin.ModelAdmin):
    list_display = ['cid', 'category', 'text', 'case']
    list_filter = ['category', 'case']
    search_fields = ['cid', 'text']
    ordering = ['case', 'cid']


@admin.register(ClueImplication)
class ClueImplicationAdmin(admin.ModelAdmin):
    list_display = ['clue', 'suspect_sid', 'case']
    list_filter = ['case']
    search_fields = ['suspect_sid']
    ordering = ['case', 'clue']


@admin.register(RedHerring)
class RedHerringAdmin(admin.ModelAdmin):
    list_display = ['rid', 'text', 'case']
    list_filter = ['case']
    search_fields = ['rid', 'text']
    ordering = ['case', 'rid']
