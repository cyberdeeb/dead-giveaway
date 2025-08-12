from django.contrib import admin
from .models import Case, Suspect


@admin.register(Suspect)
class SuspectAdmin(admin.ModelAdmin):
    list_display = ['name', 'occupation', 'case', 'is_culprit']
    list_filter = ['is_culprit', 'occupation', 'case']
    search_fields = ['name', 'occupation', 'motive']
    ordering = ['case', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('case', 'name', 'occupation', 'is_culprit')
        }),
        ('Character Details', {
            'fields': ('traits', 'motive')
        }),
    )


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'status', 'culprit_id', 'created_at']
    list_filter = ['difficulty', 'status', 'created_at']
    search_fields = ['title', 'seed']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'difficulty', 'status')
        }),
        ('Case Details', {
            'fields': ('seed', 'culprit_id', 'timeline')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
