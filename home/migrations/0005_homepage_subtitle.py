# Generated by Django 3.0.6 on 2020-05-30 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20200529_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='subtitle',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]