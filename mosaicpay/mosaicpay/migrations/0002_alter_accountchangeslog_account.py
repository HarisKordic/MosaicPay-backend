# Generated by Django 4.2.2 on 2023-07-06 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mosaicpay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountchangeslog',
            name='account',
            field=models.ForeignKey(max_length=4, on_delete=django.db.models.deletion.DO_NOTHING, to='mosaicpay.account'),
        ),
    ]