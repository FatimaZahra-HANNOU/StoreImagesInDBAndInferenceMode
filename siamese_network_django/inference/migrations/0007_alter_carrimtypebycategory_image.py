# Generated by Django 4.2.3 on 2023-07-24 12:01

from django.db import migrations, models
import inference.models


class Migration(migrations.Migration):

    dependencies = [
        ('inference', '0006_alter_carrimtypebycategory_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrimtypebycategory',
            name='image',
            field=models.ImageField(upload_to=inference.models.getImagePath),
        ),
    ]
