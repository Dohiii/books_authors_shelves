# Generated by Django 4.1 on 2022-08-18 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0003_alter_author_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='user',
        ),
    ]