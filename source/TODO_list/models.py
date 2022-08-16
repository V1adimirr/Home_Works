from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class TaskModel(BaseModel):
    short_de = models.CharField(max_length=100, verbose_name='Краткое описание')
    description = models.TextField(max_length=2000, null=False, blank=False, verbose_name='Описание')
    status = models.ForeignKey("TODO_list.Status", related_name='Status', on_delete=models.PROTECT,
                               verbose_name='Статус')
    types = models.ManyToManyField("TODO_list.Type", related_name='Type', through='TODO_list.TaskType',
                                   through_fields=('task_name', 'type_name'))
    project = models.ForeignKey("TODO_list.Project", null=True, blank=True, related_name="project",
                                on_delete=models.CASCADE, verbose_name="Проект")

    def __str__(self):
        return f"{self.id}. {self.short_de} : {self.status}"

    class Meta:
        db_table = 'Tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Project(models.Model):
    name_project = models.CharField(max_length=50, verbose_name="Имя проекта")
    project_de = models.TextField(max_length=1000, verbose_name="Описание проекта")
    created_time = models.DateField(verbose_name="Дата создания")
    updated_time = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    users = models.ManyToManyField(get_user_model(), related_name='user', verbose_name='Пользователи')

    def __str__(self):
        return f"{self.id}. {self.name_project} : {self.created_time}"

    class Meta:
        db_table = 'Projects'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class TaskType(models.Model):
    task_name = models.ForeignKey('TODO_list.TaskModel', related_name='task_type', on_delete=models.CASCADE,
                                  verbose_name='Задача')
    type_name = models.ForeignKey('TODO_list.Type', related_name='name_type', on_delete=models.CASCADE,
                                  verbose_name='Имя типа')

    def __str__(self):
        return "{} | {}".format(self.task_name, self.type_name)


class Type(BaseModel):
    type = models.CharField(max_length=30, verbose_name='Тип')

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'Type'
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Status(BaseModel):
    status = models.CharField(max_length=30, verbose_name='Статус')

    def __str__(self):
        return self.status

    class Meta:
        db_table = 'Status'
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
