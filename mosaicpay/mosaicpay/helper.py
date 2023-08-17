from .models import Account,Transaction
import numbers
def convertAccountToJson(account:Account)->str:
    account_dict = {
    'account_id': account.account_id,
    'name': account.name,
    'balance': float(account.balance),
    'user': account.user.user_id
    }
    return account_dict

def convertTransactionToJson(transaction:Transaction)->str:
    transaction_dict = {
    'transaction_id': transaction.transaction_id,
    'type': transaction.type,
    'amount': float(transaction.amount),
    'account': transaction.account.account_id,
    'transaction_state': transaction.transaction_state.transaction_state_id
    }
    return transaction_dict

def get_partition_key(num:numbers):
    if num%2==0:
        return "partition_0"
    return "partition_1"
