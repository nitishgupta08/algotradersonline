# Generated by Django 4.0.4 on 2022-05-21 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strategiesAPI', '0002_alter_credentials_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='credentials',
            table='Credential',
        ),
        migrations.AlterModelTable(
            name='strategies',
            table='Strategie',
        ),
    ]
