import streamlit as st
from pandas import read_json
import requests 


# Below the fist chart add a input field for the invoice number
cust_id = st.sidebar.text_input("CustomerID:")

# if enter has been used on the input field 
if cust_id:

    # only includes or excludes
    mydoc = requests.get('http://api-egest:8080/customer/' + cust_id)

    # create dataframe from resulting documents to use drop_duplicates
    df = read_json(mydoc.json())
    
    # drop duplicates, but keep the first one
    df.drop_duplicates(subset ="InvoiceNo", keep = 'first', inplace = True)

    # Add the table with a headline
    st.header("Output Customer Invoices")
    table2 = st.dataframe(data=df) 
    

# Below the fist chart add a input field for the invoice number
inv_no = st.sidebar.text_input("InvoiceNo:")

# if enter has been used on the input field 
if inv_no:
    
    mydoc = requests.get('http://api-egest:8080/invoice/' + inv_no)

    # create the dataframe
    df = read_json(mydoc.json())

    # reindex it so that the columns are order lexicographically 
    reindexed = df.reindex(sorted(df.columns), axis=1)

    # Add the table with a headline
    st.header("Output by Invoice ID")
    table2 = st.dataframe(data=reindexed) 


