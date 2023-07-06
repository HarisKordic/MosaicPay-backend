from .models import Account
import string
def convertAccountToJson(account:Account)->string:
    account_dict = {
    'account_id': account.account_id,
    'name': account.name,
    'balance': float(account.balance),
    'user': account.user.user_id
    }
    return account_dict
    
