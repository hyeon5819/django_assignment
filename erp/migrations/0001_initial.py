# Generated by Django 4.2 on 2023-04-07 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=256)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('F', 'Free')], max_length=1)),
                ('stock_quantity', models.IntegerField(default=0)),
            ],
        ),
    ]