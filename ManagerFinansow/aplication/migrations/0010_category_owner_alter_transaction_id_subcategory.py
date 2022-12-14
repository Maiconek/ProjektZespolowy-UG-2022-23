# Generated by Django 4.1.3 on 2022-12-03 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("UsersApp", "0003_remove_profile_id_currency"),
        ("aplication", "0009_account_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="UsersApp.profile",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="id_subcategory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="aplication.subcategory",
            ),
        ),
    ]
