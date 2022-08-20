# Generated by Django 4.0.6 on 2022-08-20 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_alter_media_htag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='htag',
            field=models.CharField(default='To be defined', max_length=32, verbose_name='htag'),
        ),
        migrations.AlterField(
            model_name='media',
            name='reply_to_screen_name',
            field=models.CharField(max_length=16, null=True, verbose_name='reply_to_screen_name'),
        ),
        migrations.AlterField(
            model_name='media',
            name='screen_name',
            field=models.CharField(max_length=16, verbose_name='screen_name'),
        ),
    ]
