# Generated by Django 3.0.3 on 2020-03-25 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='This is a test desciption'),
            preserve_default=False,
        ),
    ]
