from import_export import resources
from .models import (
    Logs,
    ProductTypes,
    Products,
    Requests,
    Roles,
    SmartContracts,
    Transactions,
    UserLogs,
    UserRequests,
    UserTransactions,
    Users,
)

class LogsResource(resources.ModelResource):
    class Meta:
        model = Logs

class ProductTypesResource(resources.ModelResource):
    class Meta:
        model = ProductTypes

class ProductsResource(resources.ModelResource):
    class Meta:
        model = Products

class RequestsResource(resources.ModelResource):
    class Meta:
        model = Requests

class RolesResource(resources.ModelResource):
    class Meta:
        model = Roles

class SmartContractsResource(resources.ModelResource):
    class Meta:
        model = SmartContracts

class TransactionsResource(resources.ModelResource):
    class Meta:
        model = Transactions

class UserLogsResource(resources.ModelResource):
    class Meta:
        model = UserLogs

class UserRequestsResource(resources.ModelResource):
    class Meta:
        model = UserRequests

class UserTransactionsResource(resources.ModelResource):
    class Meta:
        model = UserTransactions

class UsersResource(resources.ModelResource):
    class Meta:
        model = Users
