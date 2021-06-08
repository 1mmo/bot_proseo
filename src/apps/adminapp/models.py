import PIL

from django.db import models
from django.utils import timezone


STATUS_CHOICES = (
    ('admin', 'Admin'),
    ('user', 'User'),
 )

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


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
    description = models.TextField(max_length=200, blank=True, null = True)
    category = models.ManyToManyField(Category, blank=True, verbose_name='Category')

    def __str__(self):
        return self.titl

    def get_categories(self):
        return "\n".join([p.title for p in self.category.all()])

    class Meta:
        db_table = 'urls'
        verbose_name = 'Url'
        verbose_name_plural = 'Urls'


class Chats(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=32, default="")
    black_list = models.BooleanField(default=False)
    description = models.TextField(max_length=200,blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True, verbose_name='Category',)

    def __str__(self):
        return self.title

    def get_category(self):
        return "\n".join([p.title for p in self.category.all()])

    class Meta:
        db_table = 'chats'
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'


class Post(models.Model):
    created_at = models.DateTimeField(auto_now=True, verbose_name='created at')
    is_published = models.BooleanField(default=False, verbose_name='Is published?')
    title = models.CharField(max_length=200, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    file_field = models.FileField(
         upload_to='files/', verbose_name='File',
         blank=True, null=True, help_text='Enter file'
    )
    image = models.ImageField(
        upload_to='images/', verbose_name='image',
        blank=True, null=True, help_text='Enter image'
    )

    class Meta:
        db_table = "post"
        verbose_name = "Post"
        verbose_name_plural = "Post"

    def __str__(self):
        return self.title
