# Generated by Django 4.2.2 on 2023-07-23 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarRimType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=3)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
