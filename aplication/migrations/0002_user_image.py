# Generated by Django 3.2.5 on 2022-11-04 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
