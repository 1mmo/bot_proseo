# Generated by Django 3.2.4 on 2021-06-07 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_remove_url_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='title',
            field=models.CharField(default='', max_length=32),
        ),
    ]