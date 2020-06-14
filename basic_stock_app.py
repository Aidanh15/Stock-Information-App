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

tickerDf_week= tickerData.history(period='1d', start = (datetime.now() - timedelta(days=8)), end=str(current_date))
spydf_week = spydata.history(period='1d', start = (datetime.now() - timedelta(days=8)), end=str(current_date))
print(tickerDf_week)
TEST = (datetime.now() - timedelta(days=7))
print(TEST)

tickerDf_year = tickerData.history(period='1d', start='2020-1-01', end=str(current_date))
spydf_year = spydata.history(period='1d', start='2020-1-01', end=str(current_date))

st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)
# Yearly change (for beat the market section)
first_value = tickerDf_year.Close.iloc[0]
last_value = tickerDf_year.Close.iloc[-1]
change = (last_value - first_value)/first_value

#Daily change(for below section)
first_value_week = tickerDf_week.Close.iloc[0]
last_value_week = tickerDf_week.Close.iloc[-1]
change_week = (last_value_week - first_value_week)/first_value_week


if change_week > 0:
   st.write("This stock is up **{:.2f}".format(change_week*100)+ '%** this week')
elif change_week < 0:
   st.write("This stock is down **{:.2f}".format(change_week*100)+ '%** this week')

st.button('year') 



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
