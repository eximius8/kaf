# Generated by Django 3.0.6 on 2020-05-29 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20200529_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personlistpage',
            name='subtitle',
            field=models.CharField(max_length=300, verbose_name='Наш девиз'),
        ),
    ]
