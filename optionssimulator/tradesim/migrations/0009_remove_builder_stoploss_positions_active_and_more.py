# Generated by Django 4.0.6 on 2022-08-04 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradesim', '0008_alter_positions_pnl_alter_positions_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='builder',
            name='stoploss',
        ),
        migrations.AddField(
            model_name='positions',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='positions',
            name='pnl',
            field=models.FloatField(default=0.0, max_length=10, null=True),
        ),
    ]
