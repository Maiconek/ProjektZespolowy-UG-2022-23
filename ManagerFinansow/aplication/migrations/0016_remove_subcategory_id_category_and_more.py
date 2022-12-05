# Generated by Django 4.0.2 on 2022-12-04 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UsersApp', '0007_category_subcategory'),
        ('aplication', '0015_alter_user_account_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='id_category',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UsersApp.category'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id_subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UsersApp.subcategory'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Subcategory',
        ),
    ]