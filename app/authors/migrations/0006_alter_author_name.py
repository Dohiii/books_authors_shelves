# Generated by Django 4.1 on 2022-08-20 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0005_alter_author_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=225, unique=True),
        ),
    ]