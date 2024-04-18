from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
            
        email = self.normalize_email(email)
        
        user = self.model(username=username, email=email, **extra_fields)  # Здесь используется переданный email
        if password is not None:
            user.set_password(password)
        
        user.avatar = 'img/ava/default.jpg'
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if password is None:
            raise ValueError('Superuser must have a password.')

        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class CoffeeUsers(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField('Имя', max_length=20, null=True)
    last_name = models.CharField('Фамилия', max_length=20, null=True)
    middle_name = models.CharField('Отчество', max_length=30, null=True)
    birth_day = models.DateField('Дата рождения', null=True, blank=True, default=None)
    phone = models.CharField('Телефон', max_length=15, unique=True, null=True)
    email = models.EmailField('Рабочая почта', max_length=100, unique=True, null=True)
    otdel = models.ForeignKey('OtdelClass', verbose_name='Отдел', on_delete=models.SET_NULL, max_length=100, null=True, blank=True, default=None)
    position = models.CharField('Должность', max_length=50, null=True, blank=True, default=None)
    avatar = models.ImageField('Фото профиля', blank = True, null=True, default='ava/default.jpg', upload_to='avatar/')
    nachalnik = models.BooleanField('Руководитель', default=False)
    is_staff = models.BooleanField('Админ', default=False)
    is_active = models.BooleanField('Активность', default=True)
    is_superuser = models.BooleanField('SuperMega', default=False)
    username = models.CharField('Логин', max_length=256, unique=True)
    telegram_code = models.CharField('Код', max_length=6, null=True, blank=True, default=None)
    code_creation_time = models.DateTimeField(null=True, blank=True, default=None)
    chat_id = models.CharField('ID Телеграмм', max_length=150, unique=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"
    
    def __str__(self):
        return self.username
    
    def avatar_delete_handler(self, **kwargs):
        # Установка дефолтного аватара при удалении текущего
        if 'avatar' in kwargs and kwargs['avatar'] is None:
            self.avatar = 'static/ava/default.jpg'
            self.save()

    def delete(self, *args, **kwargs):
        # Перехватываем удаление аватара
        self.avatar_delete_handler(**kwargs)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Перехватываем удаление аватара
        self.avatar_delete_handler(**kwargs)
        super().save(*args, **kwargs)

    @staticmethod
    @receiver(pre_save, sender='users.CoffeeUsers')
    def delete_avatar_file(sender, instance, **kwargs):
        # Удаление файла аватара при удалении пользователя
        if instance.pk:
            try:
                old_instance = CoffeeUsers.objects.get(pk=instance.pk)
            except CoffeeUsers.DoesNotExist:
                return False

            old_avatar = old_instance.avatar
            new_avatar = instance.avatar
            if old_avatar and old_avatar != new_avatar:
                if os.path.isfile(old_avatar.path):
                    os.remove(old_avatar.path)

    @staticmethod
    @receiver(pre_save, sender='users.CoffeeUsers')
    def delete_old_avatar_file(sender, instance, **kwargs):
        # Удаление старого файла аватара при обновлении
        if instance.pk:
            try:
                old_instance = CoffeeUsers.objects.get(pk=instance.pk)
            except CoffeeUsers.DoesNotExist:
                return False

            old_avatar = old_instance.avatar
            new_avatar = instance.avatar
            if old_avatar and old_avatar != new_avatar:
                if os.path.isfile(old_avatar.path):
                    os.remove(old_avatar.path)
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class OtdelClass(models.Model):
    title = models.CharField('Название отдела', max_length=100, blank=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
