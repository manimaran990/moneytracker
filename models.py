from pydantic import BaseModel
from enum import Enum
import datetime


class ExpenseCats(str, Enum):
    """expense category enum"""

    shopping = "shopping"
    hotel = "hotel"
    food = "food"
    entertainment = "entertainment"
    houserent = "houserent"
    phonebill = "phonebill"
    misc = "misc"
    transfers = "transfers"
    paycheck = "paycheck"
    remittance = "remittance"
    service = "service"
    bill_payment = "bill_payment"


class CreditOrDebit(str, Enum):
    credit = "credit"
    debit = "debit"


class CurrencyType(str, Enum):
    CAD = "CAD"
    INR = "INR"


class Expense(BaseModel):
    """single expense model"""

    user: str = None
    date: str = datetime.date.today()
    expense_type: ExpenseCats = None
    credit_or_debit: CreditOrDebit = "debit"
    amount: float = None
    currency_type: CurrencyType = None
    description: str = None


class Item(BaseModel):
    name = str
