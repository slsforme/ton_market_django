# Generated by Django 5.1.1 on 2024-10-01 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction_type', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('log_type', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'logs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('onchain_address', models.CharField(max_length=60, unique=True)),
                ('owner_address', models.CharField(max_length=60, unique=True)),
                ('metadata', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'product_types',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'requests',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'roles',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SmartContracts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('onchain_address', models.CharField(max_length=60)),
                ('abi', models.JSONField(blank=True, null=True)),
                ('owner_address', models.CharField(max_length=60)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('createad_at', models.DateTimeField()),
                ('uuid', models.UUIDField()),
            ],
            options={
                'db_table': 'smart_contracts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_hash', models.CharField(max_length=65)),
                ('type', models.CharField(max_length=255)),
                ('tx_date', models.DateTimeField()),
                ('owner_address', models.CharField(max_length=60)),
                ('receiver_address', models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                'db_table': 'transactions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
            ],
            options={
                'db_table': 'user_logs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
            ],
            options={
                'db_table': 'user_requests',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('login', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=65)),
                ('address', models.CharField(max_length=60, unique=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
            ],
            options={
                'db_table': 'user_transactions',
                'managed': False,
            },
        ),
    ]
