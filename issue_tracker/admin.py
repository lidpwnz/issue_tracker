from django.contrib import admin
from .models import Type, Status, Issue, Project
from .utils import TypeAndStatusAdminMixIn


class TypeAdmin(TypeAndStatusAdminMixIn):
    pass


class StatusAdmin(TypeAndStatusAdminMixIn):
    pass


class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status', 'created_at']
    list_filter = ['description', 'status', 'type', 'created_at', 'updated_at']
    search_fields = list_filter
    fields = ['summary', 'description', 'status', 'type', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Type, TypeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Project)
