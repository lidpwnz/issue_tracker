from django.contrib import admin


class TypeAndStatusAdminMixIn(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_filter = ['title']
    search_fields = ['title']
    fields = ['title']
