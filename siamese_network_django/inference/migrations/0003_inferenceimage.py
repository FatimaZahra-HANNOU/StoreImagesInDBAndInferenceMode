# Generated by Django 4.2.3 on 2023-07-23 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inference', '0002_alter_carrimtype_options_alter_carrimtype_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='InferenceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inferenceImage', models.ImageField(upload_to='inference/')),
            ],
        ),
    ]
