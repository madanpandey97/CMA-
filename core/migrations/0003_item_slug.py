# Generated by Django 3.0.3 on 2020-03-25 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200323_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='product-slug'),
            preserve_default=False,
        ),
    ]
