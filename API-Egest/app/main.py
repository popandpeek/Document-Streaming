# You need this to use FastAPI, work with statuses and be able to end HTTPExceptions
from fastapi import FastAPI
 
# You need this to be able to turn classes into JSONs and return
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Needed for json.dumps
import json

# used for BaseModel
from pydantic import BaseModel

# used for DB
import pymongo

# Invoice schema
class InvoiceItem(BaseModel):
    InvoiceNo: int
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: int
    Country: str


app = FastAPI()


# MongoDB
myclient = pymongo.MongoClient("mongo",27017,username='root',password='example')
mydb = myclient["docstreaming"]
mycol = mydb["invoices"] 


# Base URL
@app.get("/")
async def root():
    return {"message": "Hello World from API-Egest"}


# Get Invoice
@app.get("/invoice/{item_id}")
def get_invoice(item_id: str):
    print("Get invoice received")
    try:
        myquery = {"InvoiceNo": item_id}
        mydoc = mycol.find( myquery, { "_id": 0, "InvoiceDate": 0, "Country": 0, "CustomerID": 0 })
        mydoc_list = list(mydoc)
        mydoc_json = json.dumps(mydoc_list, indent=2)
        return mydoc_json
    except ValueError:
        return JSONResponse(content=jsonable_encoder('ERROR'), status_code=400)


# Get Customer
@app.get("/customer/{cust_id}")
def get_customer(cust_id: str):
    print("Get customer received")
    try: 
        myquery = {"CustomerID": cust_id}
        mydoc = mycol.find( myquery , { "_id": 0, "StockCode": 0, "Description": 0, "Quantity": 0, "Country": 0, "UnitPrice": 0})
        mydoc_list = list(mydoc)
        mydoc_json = json.dumps(mydoc_list, indent=2)
        return mydoc_json
    except ValueError:
        return JSONResponse(content=jsonable_encoder('ERROR'), status_code=400)
