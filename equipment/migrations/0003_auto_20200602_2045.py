# Generated by Django 3.0.6 on 2020-06-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0002_auto_20200602_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentcategory',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]