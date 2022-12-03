# Generated by Django 4.1.3 on 2022-12-03 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("UsersApp", "0003_remove_profile_id_currency"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="currency",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="UsersApp.currency",
            ),
        ),
    ]