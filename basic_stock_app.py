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

# Prices for today less 1 week
tickerDf_week= tickerData.history(period='5d', interval='1m')
spydf_week = spydata.history(period='5d', interval='1m')
#Prices from start of year til today
tickerDf_year = tickerData.history(period='1d', start='2020-1-01', end=str(current_date))
spydf_year = spydata.history(period='1d', start='2020-1-01', end=str(current_date))

#prices for today
tickerDf_day = tickerData.history(period='1d', start = (datetime.now() - timedelta(days=1)), end=datetime.now())
tickerDf_day_chart = tickerData.history( period= '1d', interval='1m')# Only way to overcome unusual plotting bug when using original var above
spydf_day = spydata.history(period='24h')



#All time change
first_value_AT = tickerDf.Close.iloc[0]
last_value_AT = tickerDf.Close.iloc[-1]
change_AT = (((last_value_AT - first_value_AT)/first_value_AT)*100)
# Yearly change (for beat the market section)
first_value = tickerDf_year.Close.iloc[0]
last_value = tickerDf_year.Close.iloc[-1]
change = (last_value - first_value)/first_value
#Weekly change 
first_value_week = tickerDf_week.Close.iloc[0]
last_value_week = tickerDf_week.Close.iloc[-1]
change_week = (last_value_week - first_value_week)/first_value_week
# Daily Change
first_value_day = tickerDf_day.Open.iloc[0]
last_value_day = tickerDf_day.Close.iloc[0]
change_day = (((last_value_day-first_value_day)/first_value_day)*100)






#Display closing price graph
st.write("""
## Closing Price
""")
st.subheader("All Time")
st.line_chart(tickerDf.Close)
if change_AT>0:
     st.write(ticker + " is up **{:.2f}".format(change_AT)+ '%** all time')
elif change_AT<0:
    st.write(ticker + " is down **{:.2f}".format(change_AT)+ '%** all time')

if st.checkbox("View Year"):
    st.line_chart(tickerDf_year.Close)
    if change > 0:
        st.write(ticker + " is up **{:.2f}".format(change*100)+ '%** this year')
    elif change < 0:
        st.write(ticker + " is down **{:.2f}".format(change*100)+ '%** this year')

if st.checkbox("View Week"):
    perf_graph_week = make_subplots(specs=[[{"secondary_y": True}]])
    perf_graph_week.add_trace(go.Scatter(x=tickerDf_week.index, y=tickerDf_week.Close,  mode='lines', name = 'Your Stock'), secondary_y=False)
    # Display Graph
    st.plotly_chart(perf_graph_week)
    if change_week > 0:
        st.write(ticker + " is up **{:.2f}".format(change_week*100)+ '%** this trading week')
    elif change_week < 0:
        st.write(ticker + " is down **{:.2f}".format(change_week*100)+ '%** this trading week')

if st.checkbox("View Day"):
    perf_graph2 = make_subplots(specs=[[{"secondary_y": True}]])
    perf_graph2.add_trace(go.Scatter(x=tickerDf_day_chart.index, y=tickerDf_day_chart.Close,  mode='lines', name = 'Your Stock'), secondary_y=False)
    # Display Graph
    st.plotly_chart(perf_graph2)
    if change_day > 0:
        st.write(ticker + " is up **{:.2f}".format(change_day)+ '%** today')
    elif change_day < 0:
        st.write(ticker + " is down **{:.2f}".format(change_day)+ '%** today')



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
st.write("**S&P's performance:** {:2f}% ".format(sp_perf*100))
st.write("**"+ ticker + "'s performance:** {:2f}% ".format(change*100))


st.write("""
## Business Information:
""")


try:
    st.write(tickerData.info["longBusinessSummary"])
except:
    st.write("*No Business Description provided*")


try:
    st.write('## Value of company: ')
    st.write('$'+str(tickerData.info["enterpriseValue"]))

    st.write('## Market Cap: ')
    st.write('$'+str(tickerData.info["marketCap"]))
except:
    st.write("Data not Provided")

try:
    logo = tickerData.info["logo_url"]
    response = requests.get(logo)
    img = Image.open(BytesIO(response.content))
    st.write('## Company logo: ') 
    st.image(img, caption='logo')
except:
    print("error: company has no logo")
