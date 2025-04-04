# Generated by Django 4.2.3 on 2024-12-05 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='masapirivu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('id_no', models.CharField(max_length=30)),
                ('reciept_no', models.CharField(max_length=30)),
                ('palli', models.CharField(max_length=6)),
                ('madrassa', models.CharField(max_length=6)),
                ('mess', models.CharField(max_length=6)),
                ('description', models.CharField(max_length=100)),
                ('total_amount', models.CharField(max_length=6)),
                ('debit_credit', models.CharField(max_length=6)),
                ('date', models.CharField(max_length=15)),
            ],
        ),
    ]
