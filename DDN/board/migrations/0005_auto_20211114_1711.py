# Generated by Django 3.2.9 on 2021-11-14 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20211113_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board_model',
            name='modify_day',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='board_model',
            name='write_day',
            field=models.DateField(blank=True, null=True),
        ),
    ]