# Generated by Django 4.1.7 on 2023-03-03 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(default='', max_length=180),
        ),
        migrations.AlterField(
            model_name='amenity',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
