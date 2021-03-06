# Generated by Django 3.1.2 on 2021-10-19 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20211019_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='comment',
            field=models.ManyToManyField(blank=True, default=None, to='auctions.Comment'),
        ),
        migrations.AlterField(
            model_name='auctions',
            name='init_price',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='auctions',
            name='winner',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
