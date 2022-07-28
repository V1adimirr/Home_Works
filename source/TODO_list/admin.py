from django.contrib import admin
from TODO_list.models import TaskModel, Type, Status, Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name_project', 'created_time', 'updated_time']
    list_filter = ['name_project']
    search_fields = ['name_project', 'created_time']
    fields = ['name_project', 'project_de', 'created_time', 'updated_time']


admin.site.register(Project, ProjectAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ['short_de', 'status']
    list_filter = ['status']
    search_fields = ['status', 'type']
    fields = ['short_de', 'description', 'status', 'created_at', 'updated_at', 'project']
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
