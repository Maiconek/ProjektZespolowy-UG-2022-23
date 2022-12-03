# Generated by Django 4.1.3 on 2022-12-03 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("UsersApp", "0004_profile_currency"),
        ("aplication", "0010_category_owner_alter_transaction_id_subcategory"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="currency",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="UsersApp.currency",
            ),
        ),
    ]