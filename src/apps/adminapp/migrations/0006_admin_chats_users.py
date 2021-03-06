# Generated by Django 3.2.4 on 2021-06-07 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0005_url_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(editable=False, max_length=32)),
                ('username', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Admins',
                'db_table': 'admin',
            },
        ),
        migrations.CreateModel(
            name='Chats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('title', models.CharField(default='', max_length=32)),
                ('black_list', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Chat',
                'verbose_name_plural': 'Chats',
                'db_table': 'chats',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(editable=False, max_length=32)),
                ('username', models.CharField(max_length=32)),
                ('black_list', models.BooleanField(default=False)),
                ('subscribe', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'users',
            },
        ),
    ]
