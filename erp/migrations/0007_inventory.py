# Generated by Django 4.2 on 2023-04-08 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0006_delete_inventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='inventory', serialize=False, to='erp.product')),
                ('inbound_quantity', models.IntegerField(default=0)),
                ('outbound_quantity', models.IntegerField(default=0)),
            ],
        ),
    ]