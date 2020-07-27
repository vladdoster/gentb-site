# Generated by Django 2.2.13 on 2020-07-24 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0012_countryhealth_all_tb_incidence2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='countryhealth',
            name='pop_dens',
            field=models.CharField(blank=True, help_text='Population density (people per sq. km of land area)', max_length=36, null=True),
        ),
        migrations.AlterField(
            model_name='countryhealth',
            name='all_tb_incidence2018',
            field=models.CharField(blank=True, help_text='Estimated incidence (all forms) per 100 000 population', max_length=36, null=True),
        ),
        migrations.AlterField(
            model_name='countryhealth',
            name='hiv_incidence2018',
            field=models.CharField(blank=True, help_text='Estimated incidence of TB cases who are HIV-positive', max_length=36, null=True),
        ),
        migrations.AlterField(
            model_name='countryhealth',
            name='household',
            field=models.CharField(blank=True, help_text='Estimated average household size', max_length=36, null=True),
        ),
        migrations.AlterField(
            model_name='countryhealth',
            name='total_funding',
            field=models.CharField(blank=True, help_text='Total expected funding from all sources (US Dollars)', max_length=36, null=True),
        ),
    ]