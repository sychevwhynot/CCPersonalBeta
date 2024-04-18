from django.db import models
from users.models import CoffeeUsers


class Feedlist(models.Model):
    title = models.CharField('Тема', max_length=1000, blank=False)
    content = models.CharField('Новость', max_length=5000, blank=False)
    time_create = models.DateTimeField('Дата поста', auto_now_add=True)
    time_update = models.DateTimeField('Изменено', auto_now=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.SET_NULL, blank=True, null=True, default=None)
    user = models.ForeignKey(CoffeeUsers, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, editable=False)

 
    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user = kwargs.pop('user', None)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
    


class Category(models.Model):
    name = models.CharField(max_length=256, blank=False)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'