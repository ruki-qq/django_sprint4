# Generated by Django 3.2.16 on 2023-09-11 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Биография'),
        ),
    ]
