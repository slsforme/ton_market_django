import strawberry
from .models import Logs, ProductTypes, Products, Requests, Roles, SmartContracts, Transactions, UserLogs, UserRequests, UserTransactions, Users

@strawberry.django.type(Logs)
class LogsType:
    id: int
    interaction_type: str
    created_at: str  
    log_type: str
    name: str

@strawberry.django.type(ProductTypes)
class ProductTypesType:
    id: int
    name: str

@strawberry.django.type(Products)
class ProductsType:
    id: int
    name: str
    description: str
    onchain_address: str
    owner_address: str
    metadata: str
    type: ProductTypesType

@strawberry.django.type(Requests)
class RequestsType:
    id: int
    created_at: str  
    description: str
    name: str
    email: str

@strawberry.django.type(Roles)
class RolesType:
    id: int
    name: str

@strawberry.django.type(SmartContracts)
class SmartContractsType:
    id: int
    onchain_address: str
    abi: str  
    owner_address: str
    status: str
    createad_at: str
    uuid: str

@strawberry.django.type(Transactions)
class TransactionsType:
    id: int
    tx_hash: str
    smart_contract: SmartContractsType
    type: str
    product: ProductsType
    tx_date: str
    owner_address: str
    receiver_address: str

@strawberry.django.type(UserLogs)
class UserLogsType:
    id: int
    user: 'UsersType'  
    log: LogsType
    uuid: str

@strawberry.django.type(UserRequests)
class UserRequestsType:
    id: int
    user: 'UsersType'  
    request: RequestsType
    uuid: str

@strawberry.django.type(UserTransactions)
class UserTransactionsType:
    id: int
    user: 'UsersType'  
    tx: TransactionsType
    uuid: str

@strawberry.django.type(Users)
class UsersType:
    id: int
    uuid: str
    login: str
    password: str
    address: str
    role: RolesType
