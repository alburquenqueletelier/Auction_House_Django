# Generated by Django 3.1.2 on 2021-10-19 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20211019_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='active',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='auctions',
            name='init_price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
