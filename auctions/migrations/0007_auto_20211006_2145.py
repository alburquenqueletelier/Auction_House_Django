# Generated by Django 3.1.2 on 2021-10-07 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20211006_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='category',
            field=models.IntegerField(blank=True, choices=[(1, 'Sport'), (2, 'Electronic'), (3, 'Homelike'), (4, 'Food'), (5, 'Cars')], default=None, null=True),
        ),
    ]
