from django.contrib import admin
from TODO_list.models import TaskModel, Type, Status


class TaskAdmin(admin.ModelAdmin):
    list_display = ['short_de', 'status', 'type']
    list_filter = ['status', 'type']
    search_fields = ['status', 'type']
    fields = ['short_de', 'description', 'status', 'type', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(TaskModel, TaskAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ['type']
    fields = ['type']


admin.site.register(Type, TypeAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ['status']
    fields = ['status']


admin.site.register(Status, StatusAdmin)
