# Generated by Django 3.2.4 on 2021-06-08 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0009_auto_20210608_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file_field',
            field=models.FileField(blank=True, help_text='Enter file', null=True, upload_to='files/', verbose_name='File'),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Enter image', null=True, upload_to='images/', verbose_name='image'),
        ),
    ]
