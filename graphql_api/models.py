from django.db import (
    models, 
    connection,
    transaction,
    IntegrityError
)
from django.http import JsonResponse
from django.core.validators import (
    MinLengthValidator,
     MaxLengthValidator,
      RegexValidator
)

import uuid 

class Logs(models.Model):
    id = models.AutoField(primary_key=True)
    interaction_type = models.CharField(max_length=255,
        validators=[MinLengthValidator(3), MaxLengthValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=255, 
    validators=[
        MinLengthValidator(3), 
        MaxLengthValidator(100)
    ])
    name = models.CharField(max_length=1000, validators=[
        MinLengthValidator(3),
        MaxLengthValidator(1000)
    ])
    is_auto_created = models.BooleanField(default=False)

    def __str__(self):
        return f"Лог {self.interaction_type} : {self.created_at}"

    class Meta:
        verbose_name = "Логи"
        verbose_name_plural = "Логи"
        managed = True
        db_table = 'logs'


class ProductTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255, 
    validators=[
        MinLengthValidator(3),
        MaxLengthValidator(255)
    ])

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Типы товаров"
        verbose_name_plural = "Типы товаров"
        managed = False
        db_table = 'product_types'


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255,
        validators=[MinLengthValidator(2), MaxLengthValidator(255)]
    )
    description = models.CharField(max_length=1000, blank=True, null=True)
    onchain_address = models.CharField(unique=True, max_length=60, 
        validators=[MinLengthValidator(40), MaxLengthValidator(60)]
    )
    owner_address = models.CharField(unique=True, max_length=60,
        validators=[MinLengthValidator(40), MaxLengthValidator(60)]
    )
    metadata = models.TextField(blank=True, null=True)
    type = models.ForeignKey(ProductTypes, models.DO_NOTHING, db_column='type_id')

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
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
        except Exception as e:
            return JsonResponse({"error": f"Ошибка при сохранении продукта: {str(e)}"}, status=400)

    def __str__(self):
        return f"Товар {self.name}"

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"
        managed = False
        db_table = 'products'


class Requests(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(
        validators=[
            MinLengthValidator(7)
        ]
    )
    name = models.CharField(max_length=255,
        validators=[MinLengthValidator(3), MaxLengthValidator(100)]
    )
    email = models.CharField(max_length=255,
        validators=[RegexValidator(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')]
    )

    def __str__(self):
        return f"Запрос от {self.created_at}"

    class Meta:
        verbose_name = "Запросы"
        verbose_name_plural = "Запросы"
        managed = False
        db_table = 'requests'


class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255,
    validators=[
            MinLengthValidator(3),
            MaxLengthValidator(255)
        ]
    )

    def __str__(self):
        return f"Роль {self.name}"

    class Meta:
        verbose_name = "Роли"
        verbose_name_plural = "Роли"
        managed = False
        db_table = 'roles'


class SmartContracts(models.Model):
    id = models.AutoField(primary_key=True)
    onchain_address = models.CharField(max_length=60,
        validators=[MinLengthValidator(40), MaxLengthValidator(60)]
    )
    abi = models.JSONField(blank=True, null=True)
    owner_address = models.CharField(max_length=60,
        validators=[MinLengthValidator(40), MaxLengthValidator(60)]
    )
    status = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    uuid = models.UUIDField(blank=True, null=True)

    def __str__(self):
        return f"Смарт контракт {self.onchain_address}"

    class Meta:
        verbose_name = "Смарт контракты"
        verbose_name_plural = "Смарт контракты"
        managed = True
        db_table = 'smart_contracts'


class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    tx_hash = models.CharField(max_length=65, validators=[
        MinLengthValidator(64), MaxLengthValidator(64)
    ])
    smart_contract = models.ForeignKey(SmartContracts, models.DO_NOTHING, db_column='smart_contract_id')
    type = models.CharField(max_length=255)
    product = models.ForeignKey(Products, models.DO_NOTHING, db_column='product_id')
    tx_date = models.DateTimeField()
    owner_address = models.CharField(max_length=60,
        validators=[MinLengthValidator(40), MaxLengthValidator(60)]
    )
    receiver_address = models.CharField(max_length=60, blank=True, null=True, 
        validators=[MinLengthValidator(40), MaxLengthValidator(60)]
    )

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
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
        except Exception as e:
            return JsonResponse({"error": f"Ошибка при сохранении транзакции: {str(e)}"}, status=400)

    def __str__(self):
        return f"tx {self.tx_hash}"

    class Meta:
        verbose_name = "Транзакции"
        verbose_name_plural = "Транзакции"
        managed = False
        db_table = 'transactions'


class UserLogs(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    log = models.ForeignKey(Logs, models.DO_NOTHING, db_column='log_id')
    uuid = models.UUIDField(blank=True)

    def __str__(self):
        return f"Лог {self.uuid}"

    class Meta:
        verbose_name = "Логи Пользователей"
        verbose_name_plural = "Логи Пользователей"
        managed = False
        db_table = 'user_logs'


class UserRequests(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    request = models.ForeignKey(Requests, models.DO_NOTHING, db_column='request_id')
    uuid = models.UUIDField(blank=True, default=uuid.uuid4())

    def __str__(self):
        return f"Запрос {self.uuid}"

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(
                        "CALL add_user_request_transaction(%s, %s)", 
                        [self.user_id, self.request_id]
                    )
                super().save(*args, **kwargs)
        except IntegrityError as e:
            raise ValueError(f"Failed to save UserRequests object: {e}")
        except Exception as e:
            raise ValueError(f"An error occurred: {e}")

    class Meta:
        verbose_name = "Запросы пользователей"
        verbose_name_plural = "Запросы пользователей"
        managed = False
        db_table = 'user_requests'


class UserTransactions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    tx = models.ForeignKey(Transactions, models.DO_NOTHING, db_column='tx_id')
    uuid = models.UUIDField(blank=True)

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
    login = models.CharField(max_length=50,
        validators=[MinLengthValidator(5), MaxLengthValidator(50)]
    )
    password = models.CharField(max_length=50, 
    validators=[
        MinLengthValidator(7), MaxLengthValidator(50)
    ])
    address = models.CharField(unique=True, max_length=60, 
        validators=[MinLengthValidator(40), MaxLengthValidator(60)]
    )
    role = models.ForeignKey(Roles, models.DO_NOTHING, db_column='role_id')
    email = models.CharField(max_length=255,
        validators=[RegexValidator(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')]
    )

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                if not self.pk:

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
        except Exception as e:
            return JsonResponse({"error": f"Ошибка при сохранении пользователя: {str(e)}"}, status=400)

    def __str__(self):
        return f"Пользователь {self.uuid}"

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"
        managed = True
        db_table = 'users'
