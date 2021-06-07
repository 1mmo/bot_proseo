from django.db import models


STATUS_CHOICES = (
    ('admin', 'Admin'),
    ('user', 'User'),
 )

class Users(models.Model):
    chat_id = models.CharField(max_length=32, editable=False)
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=32, blank=True, null=True)
    surname = models.CharField(max_length=32, blank=True, null=True)
    black_list = models.BooleanField(default=False)
    subscribe = models.BooleanField(default=False)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='user')

    def __str__(self):
        return '{} {}'.format(self.name, self.surname)

    class Meta:
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Users"


class Url(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=32, default="")
    black_list = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'urls'
        verbose_name = 'Url'
        verbose_name_plural = 'Urls'


class Chats(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=32, default="")
    black_list = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'chats'
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
