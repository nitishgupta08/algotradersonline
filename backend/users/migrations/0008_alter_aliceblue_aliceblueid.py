# Generated by Django 4.0.3 on 2022-03-31 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_aliceblue_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliceblue',
            name='aliceblueId',
            field=models.CharField(max_length=50, unique=True, verbose_name='AliceBlue id'),
        ),
    ]
