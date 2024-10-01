from django.db import models


class Logs(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    interaction_type = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    log_type = models.CharField(max_length=255)
    name = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'logs'


class ProductTypes(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'product_types'


class Products(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=1000, blank=True, null=True)
    onchain_address = models.CharField(unique=True, max_length=60)
    owner_address = models.CharField(unique=True, max_length=60)
    metadata = models.TextField(blank=True, null=True)
    type = models.ForeignKey(ProductTypes, models.DO_NOTHING, db_column='type_id')

    class Meta:
        managed = False
        db_table = 'products'


class Requests(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    created_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'requests'


class Roles(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'roles'


class SmartContracts(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    onchain_address = models.CharField(max_length=60)
    abi = models.JSONField(blank=True, null=True)
    owner_address = models.CharField(max_length=60)
    status = models.CharField(max_length=100, blank=True, null=True)
    createad_at = models.DateTimeField()
    uuid = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'smart_contracts'


class Transactions(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    tx_hash = models.CharField(max_length=65)
    smart_contract = models.ForeignKey(SmartContracts, models.DO_NOTHING, db_column='smart_contract_id')
    type = models.CharField(max_length=255)
    product = models.ForeignKey(Products, models.DO_NOTHING, db_column='product_id')
    tx_date = models.DateTimeField()
    owner_address = models.CharField(max_length=60)
    receiver_address = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transactions'


class UserLogs(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    log = models.ForeignKey(Logs, models.DO_NOTHING, db_column='log_id')
    uuid = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'user_logs'


class UserRequests(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    request = models.ForeignKey(Requests, models.DO_NOTHING, db_column='request_id')
    uuid = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'user_requests'


class UserTransactions(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    tx = models.ForeignKey(Transactions, models.DO_NOTHING, db_column='tx_id')
    uuid = models.UUIDField()

    class Meta:
        managed = False
        db_table = 'user_transactions'


class Users(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    uuid = models.UUIDField()
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=65)
    address = models.CharField(unique=True, max_length=60)
    role = models.ForeignKey(Roles, models.DO_NOTHING, db_column='role_id')

    class Meta:
        managed = False
        db_table = 'users'
