# Generated by Django 4.1.3 on 2023-02-27 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplication', '0026_alter_invitation_access_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aplication.transaction')),
                ('account_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from+', to='aplication.account')),
                ('account_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to+', to='aplication.account')),
            ],
            bases=('aplication.transaction',),
        ),
    ]