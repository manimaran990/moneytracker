from fastapi import FastAPI
from models import Expense, CreditOrDebit, Item


app = FastAPI()

"""
    service to create/record a new expense
"""
@app.post("/recordExpense")
async def record_expense(expense: Expense):
    return { "expense": expense }