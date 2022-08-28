# Generated by Django 4.1 on 2022-08-26 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shelf_name', models.CharField(default='Shelf', max_length=255, null=True)),
                ('description', models.TextField(blank=True)),
                ('access', models.CharField(choices=[('PRIVATE', 'PRIVATE'), ('PUBLIC', 'PUBLIC')], default='PRIVATE', max_length=7)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('books', models.ManyToManyField(blank=True, related_name='books', to='books.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelves', to='profiles.profile')),
            ],
        ),
    ]
