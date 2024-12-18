# Generated by Django 5.1.1 on 2024-12-03 23:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphql_api', '0005_remove_logs_is_auto_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='is_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='logs',
            name='interaction_type',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(100)]),
        ),
        migrations.AlterField(
            model_name='logs',
            name='log_type',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(100)]),
        ),
        migrations.AlterField(
            model_name='logs',
            name='name',
            field=models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(1000)]),
        ),
    ]
