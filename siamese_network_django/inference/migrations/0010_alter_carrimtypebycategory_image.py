# Generated by Django 4.2.3 on 2023-07-24 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inference', '0009_alter_carrimtypebycategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrimtypebycategory',
            name='image',
            field=models.CharField(max_length=100),
        ),
    ]
