# Generated by Django 3.1.7 on 2021-10-25 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delab', '0003_auto_20211022_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetauthor',
            name='twitter_id',
            field=models.BigIntegerField(unique=True),
        ),
    ]
