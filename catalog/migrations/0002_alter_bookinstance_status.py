# Generated by Django 5.2.4 on 2025-07-11 03:57
from __future__ import annotations

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(
                blank=True,
                choices=[
                    ('m', 'Maintenance'),
                    ('o', 'On loan'),
                    ('a', 'Available'),
                    ('r', 'Reserved'),
                ],
                default=('m', 'Maintenance'),
                help_text='Book availability',
                max_length=1,
            ),
        ),
    ]
