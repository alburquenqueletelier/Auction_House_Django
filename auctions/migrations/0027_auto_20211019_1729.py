# Generated by Django 3.1.2 on 2021-10-19 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_auto_20211019_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]