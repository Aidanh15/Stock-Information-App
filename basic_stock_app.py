import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from PIL import Image
import requests
from io import BytesIO


current_date = datetime.now().date()
print(current_date)

st.write("""
# Simple Stock Information App 
Shown are the **closing price** and ***trading volume*** of Amazon!
""")

ticker = st.text_input("You can change the display by entering the stock ticker of your choice: ", 'AMZN')
st.write("List of [tickers](http://eoddata.com/symbols.aspx)")
sp500 = 'SPY'
# get data for this ticker
tickerData = yf.Ticker(ticker)
#get sp500 data
spydata = yf.Ticker(sp500) 

# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2000-6-13', end=str(current_date))
spydf = spydata.history(period='1d', start='2000-6-13', end=str(current_date))

tickerDf_day = tickerData.history(period='1d', start = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d'), end=str(current_date))
spydf_day = spydata.history(period='1d', start = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d'), end=str(current_date))

tickerDf_year = tickerData.history(period='1d', start='2020-1-01', end=str(current_date))
spydf_year = spydata.history(period='1d', start='2020-1-01', end=str(current_date))

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)

first_value = tickerDf_year.Close.iloc[0]
last_value = tickerDf_year.Close.iloc[-1]
change = (last_value - first_value)/first_value
if change > 0:
   st.write("This stock was up **{:.2f}".format(change)+ '%** at close today')
elif change < 0:
   st.write("This stock was down **{:.2f}".format(change)+ '%** at close today')



st.write("""
## Trading Volume
""")
st.line_chart(tickerDf.Volume)


st.write("""
## Is your stock beating the market this year?
""")
sp_perf_1 = spydf_year.Close.iloc[0]

sp_perf_last = spydf_year.Close.iloc[-1]

# Calc  % change
sp_perf = (sp_perf_last - sp_perf_1)/sp_perf_1

perf_graph = make_subplots(specs=[[{"secondary_y": True}]])
perf_graph.add_trace(go.Scatter(x=spydf_year.index, y=spydf_year.Close, mode='lines', name = 'S&P 500'), secondary_y=False)
perf_graph.add_trace(go.Scatter(x=tickerDf_year.index, y=tickerDf_year.Close, mode='lines', name = ticker), secondary_y=True)

# Display Graph
st.plotly_chart(perf_graph)

# Display % change
st.write("**S&P's performance:** {:2f} ".format(sp_perf))
st.write("**"+ ticker + "'s performance:** {:2f} ".format(change))


st.write("""
## Business Information:
""")


try:
    st.write(tickerData.info["longBusinessSummary"])
except:
    st.write("*No Business Description provided*")

st.write('## Value of company: ')
st.write('$'+str(tickerData.info["enterpriseValue"]))

st.write('## Market Cap: ')
st.write('$'+str(tickerData.info["marketCap"]))

try:
    logo = tickerData.info["logo_url"]
    response = requests.get(logo)
    img = Image.open(BytesIO(response.content))
    st.write('## Company logo: ') 
    st.image(img, caption='logo')
except:
    print("error: company has no logo")
