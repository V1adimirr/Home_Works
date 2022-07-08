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
    type = models.ForeignKey("TODO_list.Type", related_name='Type', on_delete=models.PROTECT,
                             verbose_name='Тип')

    def __str__(self):
        return f"{self.id}. {self.short_de} : {self.status}"

    class Meta:
        db_table = 'Tasks'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


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
