from django.db import models
from django.contrib.auth.models import AbstractUser
class Test(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField()

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    def __str__(self):
        return self.name
    
#USER
class User(AbstractUser):
    user_id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    birthday=models.DateField(null=True)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=255)

    username=None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    class Meta:
        verbose_name="User"
        verbose_name_plural="Users"
        db_table="user"
    def __str__(self) -> str:
        return self.first_name +" "+self.last_name
    
    

#USER ROLE
class UserRole(models.Model):
    user_role_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,unique=True)
    class Meta:
        verbose_name="UserRole"
        verbose_name_plural="UserRoles"
        db_table="user_role"
    def __str__(self) -> str:
        return self.name

#USER ROLE USER
class UserRoleUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['user', 'user_role']
        db_table="user_role_user"

# ACCOUNT
class Account(models.Model):
    account_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    balance=models.DecimalField(decimal_places=2,max_digits=10)
    user=models.ForeignKey('User', on_delete=models.CASCADE,max_length=4)
    class Meta:
        verbose_name="Account"
        verbose_name_plural="Accounts"
        db_table="account"
    def __str__(self) -> str:
        return self.name

#ACCOUNT CHANGES LOG
class AccountChangesLog(models.Model):
    account_changes_log_id=models.AutoField(primary_key=True)
    change_type=models.CharField(max_length=255)
    change_date=models.DateField(auto_now=True)
    changed_by_user=models.ForeignKey('User', on_delete=models.CASCADE,max_length=4)
    account=models.ForeignKey('Account', on_delete=models.SET_NULL,max_length=4,null=True)
    class Meta:
        verbose_name="AccountChangesLog"
        verbose_name_plural="AccountChangesLogs"
        db_table="account_changes_log"
    def __str__(self) -> str:
        return self.change_type
    
#TRANSACTION
class Transaction(models.Model):
    transaction_id=models.AutoField(primary_key=True)
    type=models.CharField(max_length=1)
    amount=models.DecimalField(decimal_places=2,max_digits=10)
    account=models.ForeignKey('Account', on_delete=models.CASCADE,max_length=4)
    transaction_state=models.ForeignKey('TransactionState', on_delete=models.CASCADE,max_length=4)
    class Meta:
        verbose_name="Transaction"
        verbose_name_plural="Transactions"
        db_table="transaction"
    def __str__(self) -> str:
        return self.transaction_id

#TRANSACTION STATE
class TransactionState(models.Model):
    transaction_state_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=9,unique=True)
    class Meta:
        verbose_name="TransactionState"
        verbose_name_plural="TransactionStates"
        db_table="transaction_state"
    def __str__(self) -> str:
        return self.name

# TRANSACTION CHANGES LOG
class TransactionChangesLog(models.Model):
    transaction_changes_log_id=models.AutoField(primary_key=True)
    change_type=models.CharField(max_length=255)
    change_date=models.DateField(auto_now=True)
    changed_by_user=models.ForeignKey('User', on_delete=models.CASCADE,max_length=4)
    transaction=models.ForeignKey('Transaction', on_delete=models.SET_NULL,max_length=4,null=True)
    class Meta:
        verbose_name="TransactionChangesLog"
        verbose_name_plural="TransactionChangesLogs"
        db_table="transaction_changes_log"
    def __str__(self) -> str:
        return self.change_type

#DOCUMENT
class Document(models.Model):
    document_id=models.AutoField(primary_key=True)
    url=models.CharField(max_length=2048,unique=True)
    type=models.CharField(max_length=4, default="jpg")
    user=models.ForeignKey('User', on_delete=models.CASCADE,max_length=4)
    account=models.ForeignKey('Account', on_delete=models.CASCADE,max_length=4,null=True)

    class Meta:
        verbose_name="Document"
        verbose_name_plural="Documents"
        db_table="document"
    def __str__(self) -> str:
        return self.url