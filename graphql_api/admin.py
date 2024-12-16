from django.contrib import admin
from .models import (
    Logs, ProductTypes, Products, Requests, Roles, SmartContracts,
    Transactions, UserLogs, UserRequests, UserTransactions, Users
)
from django.http import HttpResponse
from pathlib import Path
import subprocess
from django.utils.timezone import now
from django.conf import settings


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'interaction_type', 'created_at', 'log_type', 'name')
    search_fields = ('interaction_type', 'log_type', 'name')
    list_filter = ('log_type', 'created_at')
    list_per_page = 100

    readonly_fields = ('id', 'interaction_type', 'created_at', 'log_type', 'name')
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    


@admin.register(ProductTypes)
class ProductTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 30



@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'onchain_address', 'owner_address', 'type')
    search_fields = ('name', 'onchain_address', 'owner_address')
    list_filter = ('type',)
    list_per_page = 50



@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'name', 'email')
    search_fields = ('name', 'email', 'description')
    list_filter = ('created_at',)
    list_per_page = 50



@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 15


@admin.register(SmartContracts)
class SmartContractsAdmin(admin.ModelAdmin):
    list_display = ('id', 'onchain_address', 'owner_address', 'status', 'created_at', 'uuid')
    search_fields = ('onchain_address', 'owner_address', 'uuid')
    list_filter = ('status', 'created_at')
    list_per_page = 20


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tx_hash', 'smart_contract', 'type', 'product', 'tx_date', 'owner_address', 'receiver_address')
    search_fields = ('tx_hash', 'owner_address', 'receiver_address', 'type')
    list_filter = ('type', 'tx_date')
    list_per_page = 100


@admin.register(UserLogs)
class UserLogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'log', 'uuid')
    search_fields = ('uuid',)
    list_filter = ('log',)
    list_per_page = 100

    readonly_fields = ('id', 'user', 'log', 'uuid')
    
    # Запрет добавления, изменения и удаления объектов
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



@admin.register(UserRequests)
class UserRequestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'request')
    search_fields = ('uuid',)
    list_filter = ('request',)
    list_per_page = 50


@admin.register(UserTransactions)
class UserTransactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tx', 'uuid')
    search_fields = ('uuid',)
    list_filter = ('tx',)
    list_per_page = 50


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'address', 'role', 'email')
    search_fields = ('login', 'address', 'uuid')
    list_filter = ('role',)
    list_per_page = 20

