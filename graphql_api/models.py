from django.db import models, connection
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

class Logs(models.Model):
    id = models.AutoField(primary_key=True)  
    interaction_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=255)
    name = models.CharField(max_length=1000)
    is_auto_created = models.BooleanField(default=False)  

    def __str__(self):
        return f"Лог {self.interaction_type} : {self.created_at}"

    class Meta:
        verbose_name = "Логи"
        verbose_name_plural = "Логи"
        managed = True
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

    def save(self, *args, **kwargs):
        if not self.pk:  
            with connection.cursor() as cursor:
                cursor.callproc(
                    'add_product_with_type',
                    [
                        str(self.name),
                        str(self.description),
                        str(self.onchain_address),
                        str(self.owner_address),
                        str(self.metadata),
                        str(self.type.name)
                    ]
                )
        else:
            super().save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if not self.pk:  
            with connection.cursor() as cursor:
                cursor.callproc(
                    'add_transaction',
                    [
                        str(self.tx_hash),
                        str(self.smart_contract.onchain_address),
                        str(self.product.name),
                        str(self.type),
                        self.tx_date,
                        str(self.owner_address),
                        str(self.receiver_address)
                    ]
                )
        else:
            super().save(*args, **kwargs)

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
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(blank=True)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=65)
    address = models.CharField(unique=True, max_length=60)
    role = models.ForeignKey(Roles, models.DO_NOTHING, db_column='role_id')

    def __str__(self):
        return f"Пользователь {self.uuid}"

    def save(self, *args, **kwargs):
        if not self.pk:  
            if not self.address.startswith('0x') or len(self.address) != 42:
                raise ValueError("Address must start with '0x' and be 42 characters long.")
            
            with connection.cursor() as cursor:
                cursor.callproc(
                    'add_user_with_role',
                    [
                        str(self.login),
                        str(self.password),
                        str(self.address),
                        self.role.name  
                    ]
                )
        else:
            super().save(*args, **kwargs)  
    
    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"
        managed = False
        db_table = 'users'


def create_logs(interaction_type, log_type, name, username, is_auto_created=False):
    if is_auto_created:  # Если лог был автоматически создан, не создавать новые логи
        return
    Logs.objects.create(
        interaction_type=interaction_type,
        log_type=log_type,
        name=name,
        is_auto_created=is_auto_created  # Флаг для автоматических логов
    )

# Обработчики сигналов для каждой модели

@receiver(post_save, sender=Logs)
def create_log_on_save_logs(sender, instance, created, **kwargs):
    if instance.is_auto_created:  # Пропустить создание логов для автоматических логов
        return
    username = 'slsforme'
    if created:
        create_logs(
            interaction_type="CREATE",
            log_type="INFO",
            name=f"Создание {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True  # Лог автоматически создан, пропустим его
        )
    else:
        create_logs(
            interaction_type="UPDATE",
            log_type="INFO",
            name=f"Обновление {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )


@receiver(pre_delete, sender=Logs)
def create_log_on_delete_logs(sender, instance, **kwargs):
    if instance.is_auto_created:
        return
    username = 'slsforme'
    create_logs(
        interaction_type="DELETE",
        log_type="INFO",
        name=f"Удаление {instance.__class__.__name__}: {instance}",
        username=username,
        is_auto_created=True
    )


@receiver(post_save, sender=ProductTypes)
def create_log_on_save_product_types(sender, instance, created, **kwargs):
    username = 'slsforme'
    if created:
        create_logs(
            interaction_type="CREATE",
            log_type="INFO",
            name=f"Создание {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )
    else:
        create_logs(
            interaction_type="UPDATE",
            log_type="INFO",
            name=f"Обновление {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )


@receiver(pre_delete, sender=ProductTypes)
def create_log_on_delete_product_types(sender, instance, **kwargs):
    username = 'slsforme'
    create_logs(
        interaction_type="DELETE",
        log_type="INFO",
        name=f"Удаление {instance.__class__.__name__}: {instance}",
        username=username,
        is_auto_created=True
    )


@receiver(post_save, sender=Products)
def create_log_on_save_products(sender, instance, created, **kwargs):
    username = 'slsforme'
    if created:
        create_logs(
            interaction_type="CREATE",
            log_type="INFO",
            name=f"Создание {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )
    else:
        create_logs(
            interaction_type="UPDATE",
            log_type="INFO",
            name=f"Обновление {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )


@receiver(pre_delete, sender=Products)
def create_log_on_delete_products(sender, instance, **kwargs):
    username = 'slsforme'
    create_logs(
        interaction_type="DELETE",
        log_type="INFO",
        name=f"Удаление {instance.__class__.__name__}: {instance}",
        username=username,
        is_auto_created=True
    )


@receiver(post_save, sender=Requests)
def create_log_on_save_requests(sender, instance, created, **kwargs):
    username = 'slsforme'
    if created:
        create_logs(
            interaction_type="CREATE",
            log_type="INFO",
            name=f"Создание {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )
    else:
        create_logs(
            interaction_type="UPDATE",
            log_type="INFO",
            name=f"Обновление {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )


@receiver(pre_delete, sender=Requests)
def create_log_on_delete_requests(sender, instance, **kwargs):
    username = 'slsforme'
    create_logs(
        interaction_type="DELETE",
        log_type="INFO",
        name=f"Удаление {instance.__class__.__name__}: {instance}",
        username=username,
        is_auto_created=True
    )


@receiver(post_save, sender=Roles)
def create_log_on_save_roles(sender, instance, created, **kwargs):
    username = 'slsforme'
    if created:
        create_logs(
            interaction_type="CREATE",
            log_type="INFO",
            name=f"Создание {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )
    else:
        create_logs(
            interaction_type="UPDATE",
            log_type="INFO",
            name=f"Обновление {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )


@receiver(pre_delete, sender=Roles)
def create_log_on_delete_roles(sender, instance, **kwargs):
    username = 'slsforme'
    create_logs(
        interaction_type="DELETE",
        log_type="INFO",
        name=f"Удаление {instance.__class__.__name__}: {instance}",
        username=username,
        is_auto_created=True
    )


@receiver(post_save, sender=SmartContracts)
def create_log_on_save_smart_contracts(sender, instance, created, **kwargs):
    username = 'slsforme'
    if created:
        create_logs(
            interaction_type="CREATE",
            log_type="INFO",
            name=f"Создание {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )
    else:
        create_logs(
            interaction_type="UPDATE",
            log_type="INFO",
            name=f"Обновление {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )


@receiver(pre_delete, sender=SmartContracts)
def create_log_on_delete_smart_contracts(sender, instance, **kwargs):
    username = 'slsforme'
    create_logs(
        interaction_type="DELETE",
        log_type="INFO",
        name=f"Удаление {instance.__class__.__name__}: {instance}",
        username=username,
        is_auto_created=True
    )


@receiver(post_save, sender=Transactions)
def create_log_on_save_transactions(sender, instance, created, **kwargs):
    username = 'slsforme'
    if created:
        create_logs(
            interaction_type="CREATE",
            log_type="INFO",
            name=f"Создание {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )
    else:
        create_logs(
            interaction_type="UPDATE",
            log_type="INFO",
            name=f"Обновление {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )


@receiver(pre_delete, sender=Transactions)
def create_log_on_delete_transactions(sender, instance, **kwargs):
    username = 'slsforme'
    create_logs(
        interaction_type="DELETE",
        log_type="INFO",
        name=f"Удаление {instance.__class__.__name__}: {instance}",
        username=username,
        is_auto_created=True
    )




@receiver(post_save, sender=UserRequests)
def create_log_on_save_user_requests(sender, instance, created, **kwargs):
    username = 'slsforme'
    if created:
        create_logs(
            interaction_type="CREATE",
            log_type="INFO",
            name=f"Создание {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )
    else:
        create_logs(
            interaction_type="UPDATE",
            log_type="INFO",
            name=f"Обновление {instance.__class__.__name__}: {instance}",
            username=username,
            is_auto_created=True
        )


@receiver(pre_delete, sender=UserRequests)
def create_log_on_delete_user_requests(sender, instance, **kwargs):
    username = 'slsforme'
    create_logs(
        interaction_type="DELETE",
        log_type="INFO",
        name=f"Удаление {instance.__class__.__name__}: {instance}",
        username=username,
        is_auto_created=True
    )

