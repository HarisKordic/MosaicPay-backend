# Generated by Django 4.2.2 on 2023-07-10 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mosaicpay', '0006_document_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='account',
            field=models.ForeignKey(max_length=4, null=True, on_delete=django.db.models.deletion.CASCADE, to='mosaicpay.account'),
        ),
    ]
