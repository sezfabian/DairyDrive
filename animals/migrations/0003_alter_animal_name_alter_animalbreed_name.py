# Generated by Django 4.2.13 on 2024-07-11 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0002_alter_animaltype_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='animalbreed',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
