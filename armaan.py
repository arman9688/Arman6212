import  streamlit as st 

st.title("First streamlit App")
st.header("My first streamlit App")
st.text("This is a simple streamlit app")
st.code("print('Hello world')",language='python')

import pandas as pd

df=pd.read_csv("retail_sales_data.csv")
df['Date']=pd.to_datetime(df['Date'])
st.dataframe(df)

st.bar_chart(data=df,x='Date',y='Total Amount')