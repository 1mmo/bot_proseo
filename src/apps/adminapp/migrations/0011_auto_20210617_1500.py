# Generated by Django 3.2.4 on 2021-06-17 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0010_auto_20210608_1235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='url',
            options={'verbose_name': 'Web-Site', 'verbose_name_plural': 'Web-Sites'},
        ),
        migrations.AddField(
            model_name='chats',
            name='is_pub_black',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='url',
            name='is_pub_black',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='users',
            name='is_pub_black',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
