# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-12 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlerHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_start', models.DateTimeField(verbose_name='Début')),
                ('dt_end', models.DateTimeField(verbose_name='Fin')),
                ('md_count', models.IntegerField(verbose_name='Nombre de métadonnées')),
                ('md_modified', models.IntegerField(verbose_name='Métadonnées modifiées (t-1)')),
            ],
            options={
                'verbose_name': 'Historique du crawler',
                'verbose_name_plural': 'Historiques du crawler',
            },
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Titre')),
                ('abstract', models.TextField(verbose_name='Résumé')),
                ('md_dt_crea', models.DateTimeField(auto_now_add=True, verbose_name='Création de la métadonnée')),
                ('md_dt_update', models.DateTimeField(auto_now_add=True, verbose_name='Dernière modification de la métadonnée')),
                ('md_dt_shared_first', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('md_dt_shared_last', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('rs_dt_crea', models.DateTimeField(auto_now_add=True, verbose_name='Création de la donnée')),
                ('rs_dt_update', models.DateTimeField(auto_now_add=True, verbose_name='Dernière modification de la donnée')),
            ],
            options={
                'verbose_name': 'Métadonnée',
                'verbose_name_plural': 'Métadonnées',
                'get_latest_by': 'md_dt_update',
            },
        ),
        migrations.CreateModel(
            name='MetadataType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(db_index=True, default='VECTOR', max_length=50, unique=True, verbose_name='Type de métadonnée')),
                ('description', models.TextField(blank=True)),
                ('api_filter', models.TextField(blank=True)),
                ('api_val', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Type de métadonnée',
                'verbose_name_plural': 'Types de métadonnée',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(db_index=True, default='ACTIVE', max_length=50, unique=True, verbose_name='Statut')),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Statut de la métadonnée',
                'verbose_name_plural': 'Status des métadonnées',
            },
        ),
        migrations.AddField(
            model_name='metadata',
            name='md_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='isogeo_notify.MetadataType', verbose_name='Type de ressource décrite'),
        ),
        migrations.AddField(
            model_name='metadata',
            name='state',
            field=models.ManyToManyField(to='isogeo_notify.CrawlerHistory', verbose_name='Présence'),
        ),
    ]
