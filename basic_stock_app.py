import yfinance as yf
import streamlit as st
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO

current_date = datetime.now().date()
print(current_date)

st.write("""
# Simple Stock Information App 
Shown are the **closing price** and ***trading volume*** of Amazon!
""")

ticker = st.text_input("You can change the display by entering (in capital letters) the stock ticker of your choice: ", 'AMZN')

# get data for this ticker
tickerData = yf.Ticker(ticker)

# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2000-6-13', end=str(current_date))


st.write("""
## Closing Price
""")
st.line_chart(tickerDf.Close)

st.write("""
## Trading Volume
""")
st.line_chart(tickerDf.Volume)

st.write("""
## Business Information:
""")
st.write(tickerData.info["longBusinessSummary"])
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