from django.db import models


class Logs(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    interaction_type = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    log_type = models.CharField(max_length=255)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return f"Лог {self.interaction_type} : {self.created_at}"

    class Meta:
        verbose_name = "Логи"
        verbose_name_plural = "Логи"
        managed = False
        db_table = 'logs'


class ProductTypes(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Типы продуктов"
        verbose_name_plural = "Типы продуктов"
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

    def __str__(self):
        return f"Товар {self.name}"

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"
        managed = False
        db_table = 'products'


class Requests(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    created_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)


    def __str__(self):
        return f"Запрос от {self.created_at}"

    class Meta:
        verbose_name = "Запросы"
        verbose_name_plural = "Запросы"
        managed = False
        db_table = 'requests'


class Roles(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return f"Роль {self.name}"

    class Meta:
        verbose_name = "Роли"
        verbose_name_plural = "Роли"
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

    def __str__(self):
        return f"Смарт контракт {self.onchain_address}"

    class Meta:
        verbose_name = "Смарт контракты"
        verbose_name_plural = "Смарт контракты"
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

    def __str__(self):
        return f"tx {self.tx_hash}" 

    class Meta:
        verbose_name = "Транзакции"
        verbose_name_plural = "Транзакции"
        managed = False
        db_table = 'transactions'


class UserLogs(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    log = models.ForeignKey(Logs, models.DO_NOTHING, db_column='log_id')
    uuid = models.UUIDField()

    def __str__(self):
        return f"Лог {self.uuid}"

    class Meta:
        verbose_name = "Логи Пользователей"
        verbose_name_plural = "Логи Пользователей"
        managed = False
        db_table = 'user_logs'



class UserRequests(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    request = models.ForeignKey(Requests, models.DO_NOTHING, db_column='request_id')
    uuid = models.UUIDField()

    def __str__(self):
        return f"Запрос {self.uuid}"

    class Meta:
        verbose_name = "Запросы пользователей"
        verbose_name_plural = "Запросы пользователей"
        managed = False
        db_table = 'user_requests'



class UserTransactions(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    tx = models.ForeignKey(Transactions, models.DO_NOTHING, db_column='tx_id')
    uuid = models.UUIDField()

    def __str__(self):
        return f"tx {self.uuid}"

    class Meta:
        verbose_name = "Транзакции пользователей"
        verbose_name_plural = "Транзакции пользователей"
        managed = False
        db_table = 'user_transactions'


class Users(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем id
    uuid = models.UUIDField()
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=65)
    address = models.CharField(unique=True, max_length=60)
    role = models.ForeignKey(Roles, models.DO_NOTHING, db_column='role_id')


    def __str__(self):
        return f"Пользователь {self.uuid}"
    
    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"
        managed = False
        db_table = 'users'
