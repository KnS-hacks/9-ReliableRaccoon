# Generated by Django 3.2.9 on 2021-11-13 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board_model',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='board_model',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='board_model',
            name='modify_day',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='board_model',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='board_model',
            name='write_day',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]