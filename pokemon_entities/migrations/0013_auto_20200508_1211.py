# Generated by Django 2.2.3 on 2020-05-08 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0012_auto_20200508_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='description',
            field=models.TextField(blank=True, default='', max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='name_en',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Название (англ.)'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='name_jp',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Название (яп.)'),
        ),
    ]
