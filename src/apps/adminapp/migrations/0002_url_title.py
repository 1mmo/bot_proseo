# Generated by Django 3.2.4 on 2021-06-07 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]