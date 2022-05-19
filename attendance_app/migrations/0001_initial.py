# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-16 18:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance_app.Semester')),
            ],
        ),
        migrations.AddField(
            model_name='semester',
            name='stream',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance_app.Stream'),
        ),
    ]