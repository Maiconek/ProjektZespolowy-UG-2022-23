# Generated by Django 3.2.5 on 2022-10-31 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id_account', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('is_shared', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id_category', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id_currency', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('access_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id_subcategory', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('id_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplication.category')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id_user', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='User_Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_level', models.IntegerField(default=0)),
                ('id_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplication.account')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplication.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='User_Account',
            field=models.ManyToManyField(through='aplication.User_Account', to='aplication.Account'),
        ),
        migrations.AddField(
            model_name='user',
            name='id_currency',
            field=models.ForeignKey(default='PLN', on_delete=django.db.models.deletion.SET_DEFAULT, to='aplication.currency'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id_transaction', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('is_periodic', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('converted_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('id_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplication.account')),
                ('id_subcategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='aplication.subcategory')),
                ('id_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='aplication.user')),
            ],
        ),
    ]