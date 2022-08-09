from fastapi import FastAPI
import pandas as pd
from enum import Enum
from models import Expense, CreditOrDebit, Item, CurrencyType
from pymongo import MongoClient
import pymongo
import json
import urllib
import os

DB_SERVER = os.getenv("MONGO_SERV")
DB_USERNAME = urllib.parse.quote(os.getenv("DB_USERNAME"))
DB_PASSWORD = urllib.parse.quote(os.getenv("DB_PASSWORD"))

client = MongoClient(
    f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/?retryWrites=true&w=majority"
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


@app.get("/getrecords/date")
async def get_records(date: str):
    """get records by key val filter"""
    records = []
    try:
        items = exp_col.find({"date": {"$regex": date}})
        for item in items:
            item = dict(item)
            item.pop("_id")
            records.append(item)
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": True, "records": records}


@app.get("/getsummary/date/column")
async def get_summary(date: str, column: str = "date"):
    """get expenses summary for a month either by date(default) or expense_type"""
    try:
        # read the collection and create df
        df = pd.DataFrame(exp_col.find())
        tdf = df[df["date"].astype(str).str.contains(date)]
        summary = json.loads(
            tdf[["amount", column]].groupby(column).agg("sum").to_json()
        )["amount"]
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": True, "summary": summary}
