import strawberry
from typing import List
from .models import (
    Logs, ProductTypes, Products,
    Requests, Roles, SmartContracts,
    Transactions, UserLogs, UserRequests,
    UserTransactions, Users
)
from .types import  (
    RolesType, UsersType, ProductsType,
    ProductTypesType, LogsType, RequestsType,
    SmartContractsType, TransactionsType, UserLogsType, 
    UserRequestsType, UserTransactionsType
)

@strawberry.type
class Query:
    @strawberry.field
    def roles(self, id: int = None, name: str = None) -> List[RolesType]:
        if id is not None:
            return list(Roles.objects.filter(id=id))
        if name:
            return list(Roles.objects.filter(name=name))
        return list(Roles.objects.all())

    @strawberry.field
    def users(self,address: str = None, id: int = None) -> List[UsersType]:
        if id is not None:
            return list(Users.objects.filter(id=id))
        if address is not None:
            return list(Users.objects.filter(address=address))
        return list(Users.objects.all())

    @strawberry.field
    def products(self, id: int = None) -> List[ProductsType]:
        if id is not None:
            return list(Products.objects.filter(id=id))
        return list(Products.objects.all())

    @strawberry.field
    def product_types(self, id: int = None) -> List[ProductTypesType]:
        if id is not None:
            return list(ProductTypes.objects.filter(id=id))
        return list(ProductTypes.objects.all())

    @strawberry.field
    def logs(self, id: int = None) -> List[LogsType]:
        if id is not None:
            return list(Logs.objects.filter(id=id))
        return list(Logs.objects.all())

    @strawberry.field
    def requests(self, id: int = None) -> List[RequestsType]:
        if id is not None:
            return list(Requests.objects.filter(id=id))
        return list(Requests.objects.all())

    @strawberry.field
    def smart_contracts(self, id: int = None) -> List[SmartContractsType]:
        if id is not None:
            return list(SmartContracts.objects.filter(id=id))
        return list(SmartContracts.objects.all())

    @strawberry.field
    def transactions(self, id: int = None) -> List[TransactionsType]:
        if id is not None:
            return list(Transactions.objects.filter(id=id))
        return list(Transactions.objects.all())

    @strawberry.field
    def user_logs(self, id: int = None) -> List[UserLogsType]:
        if id is not None:
            return list(UserLogs.objects.filter(id=id))
        return list(UserLogs.objects.all())

    @strawberry.field
    def user_requests(self, id: int = None) -> List[UserRequestsType]:
        if id is not None:
            return list(UserRequests.objects.filter(id=id))
        return list(UserRequests.objects.all())

    @strawberry.field
    def user_transactions(self, id: int = None) -> List[UserTransactionsType]:
        if id is not None:
            return list(UserTransactions.objects.filter(id=id))
        return list(UserTransactions.objects.all())

@strawberry.type
class Mutation:
    # CRUD for Roles
    @strawberry.field
    def create_role(self, name: str) -> RolesType:
        role = Roles(name=name)
        role.save()
        return role

    @strawberry.field
    def update_role(self, id: int, name: str) -> RolesType:
        role = Roles.objects.get(id=id)
        role.name = name
        role.save()
        return role

    @strawberry.field
    def delete_role(self, id: int) -> bool:
        role = Roles.objects.get(id=id)
        role.delete()
        return True

    # CRUD for Users
    @strawberry.field
    def create_user(self, uuid: str, login: str, password: str,
                     address: str, role_id: int) -> UsersType:
        user = Users(uuid=uuid, login=login, password=password,
                     address=address, role_id=role_id)
        user.save()
        return user

    @strawberry.field
    def update_user(self, id: int, login: str, password: str,
                     address: str, role_id: int) -> UsersType:
        user = Users.objects.get(id=id)
        user.login = login
        user.password = password
        user.address = address
        user.role_id = role_id
        user.save()
        return user

    @strawberry.field
    def delete_user(self, id: int) -> bool:
        user = Users.objects.get(id=id)
        user.delete()
        return True

    # CRUD for Products
    @strawberry.field
    def create_product(self, name: str, description: str,
                       onchain_address: str, owner_address: str,
                       metadata: str, type_id: int) -> ProductsType:
        product = Products(
            name=name,
            description=description,
            onchain_address=onchain_address,
            owner_address=owner_address,
            metadata=metadata,
            type_id=type_id
        )
        product.save()
        return product

    @strawberry.field
    def update_product(self, id: int, name: str, description: str,
                       onchain_address: str, owner_address: str,
                       metadata: str, type_id: int) -> ProductsType:
        product = Products.objects.get(id=id)
        product.name = name
        product.description = description
        product.onchain_address = onchain_address
        product.owner_address = owner_address
        product.metadata = metadata
        product.type_id = type_id
        product.save()
        return product

    @strawberry.field
    def delete_product(self, id: int) -> bool:
        product = Products.objects.get(id=id)
        product.delete()
        return True

    # CRUD for ProductTypes
    @strawberry.field
    def create_product_type(self, name: str) -> ProductTypesType:
        product_type = ProductTypes(name=name)
        product_type.save()
        return product_type

    @strawberry.field
    def update_product_type(self, id: int, name: str) -> ProductTypesType:
        product_type = ProductTypes.objects.get(id=id)
        product_type.name = name
        product_type.save()
        return product_type

    @strawberry.field
    def delete_product_type(self, id: int) -> bool:
        product_type = ProductTypes.objects.get(id=id)
        product_type.delete()
        return True

    # CRUD for Requests
    @strawberry.field
    def create_request(self, description: str, 
                name: str, 
                email: str) -> RequestsType:
        request = Requests(
            description=description, 
            name=name, 
            email=email)
        request.save()
        return request

    @strawberry.field
    def update_request(self, id: int, description: str,
                       name: str, email: str) -> RequestsType:
        request = Requests.objects.get(id=id)
        request.description = description
        request.name = name
        request.email = email
        request.save()
        return request

    @strawberry.field
    def delete_request(self, id: int) -> bool:
        request = Requests.objects.get(id=id)
        request.delete()
        return True

    # CRUD for SmartContracts
    @strawberry.field
    def create_smart_contract(self,
                               onchain_address: str,
                               abi: str,
                               owner_address: str, 
                               status: str,
                               created_at: str,
                               uuid: str) -> SmartContractsType:
        contract = SmartContracts(
            onchain_address=onchain_address,
            abi=abi,
            owner_address=owner_address,
            status=status,
            created_at=created_at,
            uuid=uuid
        )
        contract.save()
        return contract

    @strawberry.field
    def update_smart_contract(self, id: int, onchain_address: str,
                               abi: str, owner_address: str,
                               status: str, created_at: str,
                               uuid: str) -> SmartContractsType:
        contract = SmartContracts.objects.get(id=id)
        contract.onchain_address = onchain_address
        contract.abi = abi
        contract.owner_address = owner_address
        contract.status = status
        contract.created_at = created_at
        contract.uuid = uuid
        contract.save()
        return contract

    @strawberry.field
    def delete_smart_contract(self, id: int) -> bool:
        contract = SmartContracts.objects.get(id=id)
        contract.delete()
        return True

    # CRUD for Transactions
    @strawberry.field
    def create_transaction(self, transaction_id: str, user_id: int,
                           product_id: int, status: str,
                           created_at: str) -> TransactionsType:
        transaction = Transactions(
            transaction_id=transaction_id,
            user_id=user_id,
            product_id=product_id,
            status=status,
            created_at=created_at
        )
        transaction.save()
        return transaction

    @strawberry.field
    def update_transaction(self, id: int, transaction_id: str,
                           user_id: int, product_id: int,
                           status: str, created_at: str) -> TransactionsType:
        transaction = Transactions.objects.get(id=id)
        transaction.transaction_id = transaction_id
        transaction.user_id = user_id
        transaction.product_id = product_id
        transaction.status = status
        transaction.created_at = created_at
        transaction.save()
        return transaction

    @strawberry.field
    def delete_transaction(self, id: int) -> bool:
        transaction = Transactions.objects.get(id=id)
        transaction.delete()
        return True

    @strawberry.field
    def create_user_log(self, user_id: int, 
                        action: str, 
                        created_at: str) -> UserLogsType:
        user_log = UserLogs(user_id=user_id, 
                            action=action, 
                            created_at=created_at)
        user_log.save()
        return user_log

    @strawberry.field
    def update_user_log(self, 
                        id: int, 
                        user_id: int,
                        action: str,
                        created_at: str) -> UserLogsType:
        user_log = UserLogs.objects.get(id=id)
        user_log.user_id = user_id
        user_log.action = action
        user_log.created_at = created_at
        user_log.save()
        return user_log

    @strawberry.field
    def delete_user_log(self, id: int) -> bool:
        user_log = UserLogs.objects.get(id=id)
        user_log.delete()
        return True

    # CRUD for UserRequests
    @strawberry.field
    def create_user_request(self, user_id: int, request_type: str,
                             description: str) -> UserRequestsType:
        user_request = UserRequests(user_id=user_id, 
                                    request_type=request_type,
                                    description=description)
        user_request.save()
        return user_request

    @strawberry.field
    def update_user_request(self, id: int,
                            user_id: int,
                            request_type: str,
                            description: str) -> UserRequestsType:
        user_request = UserRequests.objects.get(id=id)
        user_request.user_id = user_id
        user_request.request_type = request_type
        user_request.description = description
        user_request.save()
        return user_request

    @strawberry.field
    def delete_user_request(self, id: int) -> bool:
        user_request = UserRequests.objects.get(id=id)
        user_request.delete()
        return True

    # CRUD for UserTransactions
    @strawberry.field
    def create_user_transaction(self, user_id: int,
                                 transaction_id: str,
                                 status: str, 
                                 created_at: str) -> UserTransactionsType:
        user_transaction = UserTransactions(
            user_id=user_id,
            transaction_id=transaction_id,
            status=status,
            created_at=created_at
        )
        user_transaction.save()
        return user_transaction

    @strawberry.field
    def update_user_transaction(self, id: int, user_id: int,
                                 transaction_id: str, status: str,
                                 created_at: str) -> UserTransactionsType:
        user_transaction = UserTransactions.objects.get(id=id)
        user_transaction.user_id = user_id
        user_transaction.transaction_id = transaction_id
        user_transaction.status = status
        user_transaction.created_at = created_at
        user_transaction.save()
        return user_transaction

    @strawberry.field
    def delete_user_transaction(self, id: int) -> bool:
        user_transaction = UserTransactions.objects.get(id=id)
        user_transaction.delete()
        return True

schema = strawberry.federation.Schema(query=Query, mutation=Mutation)
