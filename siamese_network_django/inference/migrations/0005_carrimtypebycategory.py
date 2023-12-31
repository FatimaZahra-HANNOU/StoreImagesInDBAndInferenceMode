# Generated by Django 4.2.3 on 2023-07-24 11:34

from django.db import migrations, models
import inference.models


class Migration(migrations.Migration):

    dependencies = [
        ('inference', '0004_delete_inferenceimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarRimTypeByCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=3)),
                ('image', models.ImageField(upload_to=inference.models.getImagePath)),
                ('count', models.IntegerField()),
            ],
        ),
    ]
