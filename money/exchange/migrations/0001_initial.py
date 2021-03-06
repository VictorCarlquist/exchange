# Generated by Django 4.0.5 on 2022-06-10 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyModel',
            fields=[
                ('currency_code', models.CharField(max_length=3, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CurrencyRateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.DecimalField(decimal_places=16, max_digits=20)),
                ('currency_code_base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency_base', to='exchange.currencymodel')),
                ('currency_code_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency_target', to='exchange.currencymodel')),
            ],
            options={
                'unique_together': {('currency_code_base', 'currency_code_target', 'date')},
            },
        ),
    ]
