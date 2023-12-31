# Generated by Django 4.2.3 on 2023-07-23 10:00

from django.db import migrations, models
import inference.models


class Migration(migrations.Migration):

    dependencies = [
        ('inference', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carrimtype',
            options={'ordering': ['category']},
        ),
        migrations.AlterField(
            model_name='carrimtype',
            name='image',
            field=models.ImageField(upload_to=inference.models.getImagePath),
        ),
    ]
