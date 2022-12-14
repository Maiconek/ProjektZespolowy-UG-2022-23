# Generated by Django 4.0.2 on 2022-12-04 11:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('UsersApp', '0008_remove_category_owner_remove_subcategory_id_category'),
        ('aplication', '0016_remove_subcategory_id_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UsersApp.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('id_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplication.category')),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplication.category'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id_subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='aplication.subcategory'),
        ),
    ]
