from fastapi import FastAPI
import pandas as pd
from enum import Enum
from models import Expense, CreditOrDebit, Item, CurrencyType
from pymongo import MongoClient
import pymongo
import json
import urllib
import os

DB_SERVER = os.getenv('MONGO_SERV')
DB_USERNAME = urllib.parse.quote(os.getenv('DB_USERNAME'))
DB_PASSWORD = urllib.parse.quote(os.getenv('DB_PASSWORD'))

client = MongoClient(
    f'mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/?retryWrites=true&w=majority'
)
db = client.projectsDB  # database name
exp_col = db.expenses  # collection name

app = FastAPI()


@app.post("/recordExpense")
async def record_expense(expense: Expense):
    """service to create/record a new expense"""
    try:
        exp_col.insert_one(dict(expense))
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": True}


@app.get("/getrecords")
async def get_records(key: str = None, val: str = None):
    """get records by key val filter"""
    records = []
    try:
        items = exp_col.find() if key == None and val == None else exp_col.find(
            {key: val})
        for item in items:
            item = dict(item)
            item.pop('_id')
            records.append(item)
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": True, "records": records}


@app.get("/getsummary/<yymm>")
async def get_summary(yymm: str):
    """get expenses summary for a month"""
    try:
        #read the collection and create df
        df = pd.DataFrame(exp_col.find())
        tdf = df[df['date'].astype(str).str.contains(yymm)]
        summary =  json.loads(tdf[['amount', 'expense_type']].groupby('expense_type').agg('sum').to_json())["amount"]
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": True, "summary": summary}
    
