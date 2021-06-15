#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import os
from pathlib import Path
import string
import pandas as pd
import numpy as np
import seaborn as sns
import panel as pn
from panel.interact import interact, interactive, fixed, interact_manual
from panel import widgets
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
pn.extension("plotly")
from pytrends.request import TrendReq


# In[2]:


# Load .env
load_dotenv()


# In[3]:


# Set Alpaca API key and Secret key
alpaca_key = os.getenv("ALPACA_API_KEY")
alpaca_secret = os.getenv("ALPACA_API_SECRET")

# Create the Alpaca API object
alpaca = tradeapi.REST(alpaca_key, alpaca_secret, api_version = "vs")
timeframe = "1D"
start = pd.Timestamp("2016-05-26", tz = "US/Pacific").isoformat()
end = pd.Timestamp("2021-06-6", tz = "US/Pacific").isoformat()


# In[4]:


# Declares Global Variables
pytrend = TrendReq()

sectors = [
    'Communications',
    'Consumer Discretionary',
    'Consumer Staples',
    'Energy',
    'Financial',
    'Healthcare',
    'Industrial',
    'Information Technology',
    'Materials',
    'Real Estate',
    'Utilities'
    ]

beta = ['Min', 'Max', 'Median', 'Mutual Fund']

z_field = ['Close', 'Volume']

sector_tickers = {
    'Communications':
        {'Min': 'VZ', 'Max': 'LYV', 'Median': 'TMUS', 'Mutual Fund': 'VOX'},
    'Consumer Discretionary':
        {'Min': 'NVR', 'Max': 'F', 'Median': 'HLT', 'Mutual Fund': 'VCR'},
    'Consumer Staples':
        {'Min': 'CLX', 'Max': 'SYY', 'Median': 'PM', 'Mutual Fund': 'VDC'},
    'Energy':
        {'Min': 'COG', 'Max': 'OXY', 'Median': 'SLB', 'Mutual Fund': 'VDE'},
    'Financial':
        {'Min': 'CBOE', 'Max': 'LNC', 'Median': 'BAC', 'Mutual Fund': 'VFH'},
    'Healthcare':
        {'Min': 'DGX', 'Max': 'ALGN', 'Median': 'CAH', 'Mutual Fund': 'VHT'},
    'Industrial':
        {'Min': 'DGX', 'Max': 'TDG', 'Median': 'DE', 'Mutual Fund': 'VIS'},
    'Information Technology':
        {'Min': 'ORCL', 'Max': 'ENPH', 'Median': 'NTAP', 'Mutual Fund': 'VGT'},
    'Materials':
        {'Min': 'NEM', 'Max': 'FCX', 'Median': 'AVY', 'Mutual Fund': 'VAW'},
    'Real Estate':
        {'Min': 'PSA', 'Max': 'SPG', 'Median': 'UDR', 'Mutual Fund': 'VNQ'},
    'Utilities':
        {'Min': 'ED', 'Max': 'AES', 'Median': 'SRE', 'Mutual Fund': 'VPU'}
}

member_picks = {
'Boomer': ['VDC', 'VNQ', 'VOX', 'VAW'],
'Stonks': ['GME', 'AMC', 'PSLV', 'BB'],
'Pro Gamer': ['AAPL', 'TSLA', 'AMC', 'WMT'],
'Real American': ['LMT', 'TAP', 'PM', 'HAL']
}


# In[5]:


# Panel Text
group_members = '''
## Group 4
* Ben McCright aka 👵 Boomer 👴
* Josh Ferguson aka 🦅 Proud Patriot 🇺🇸
* Cole Wood aka 💎 Diamond Hands 👐
'''

box_blurb = '''
## Risk of each Sector and S & P 500 index, select the Beta:'''

heat_blurb = '''
## Correlation of each Sector and the S & P 500 index, select the Beta:'''

trend_blurb = '''
## Closing price and Goolge search interest: select Sector and Beta:'''

candlestick_blurb = '''
## Candlestick chart, select Sector and Beta:'''

spy_blurb = '''
## Compares closing price to SPY fund, select Sector and Beta:'''

tt_blurb = '''
## Go back in time to 2017 and see where your investments would be now, enter 3 Stocks and Amounts:
### (Warning: Does not reflect stock splits)'''

sharpe_blurb = '''
## Sharpe ratio of 4 stocks chosen by group members, select Portfolio:'''


# In[6]:


# Generates Correlation Heatmap of Sector Mutual Funds & Index
def df_to_plotly(df):
    return {'z': df.values.tolist(),
            'x': df.columns.tolist(),
            'y': df.index.tolist()}

@interact(Beta = beta)
def heatmap(Beta):
    df = pd.DataFrame()
    sp_file = Path('../Data/SP500.csv')
    sp_df = pd.read_csv(sp_file, infer_datetime_format=True, parse_dates=True, index_col='Date')
    df['SP500'] = sp_df['Close']
    for k, v in sector_tickers.items():
        ticker = sector_tickers[k][Beta]
        file = Path('../Data/{}.csv'.format(ticker))
        ticker_df = pd.read_csv(file, infer_datetime_format=True, parse_dates=True, index_col='Date')
        df[k] = ticker_df['Close']
    df = df.pct_change()
    df.dropna(inplace = True)
    corr = df.corr()
    fig = go.Figure(data=go.Heatmap(
        df_to_plotly(corr),
        colorscale='blues'))
    fig.update_layout(title = 'Heatmap',width=1000, height=500)
    return fig


# In[7]:


# Generates Candlestick Chart of Sector Ticker
@interact(Sector = sectors, Beta = beta)
def candlestick(Sector, Beta):
    ticker = sector_tickers[Sector][Beta]
    file = Path('../Data/{}.csv'.format(ticker))
    df = pd.read_csv(file, infer_datetime_format=True, parse_dates=True, index_col='Date')
    fig = go.Figure(data=[go.Candlestick(
        x = df.index,
        open = df['Open'],
        high = df['High'],
        low = df['Low'],
        close = df['Close']
    )])
    fig.update_xaxes(title_text = 'Date')
    fig.update_yaxes(title_text = 'Price (USD)')
    fig.update_layout(title = ticker, width=1000, height=500)
    return fig


# In[8]:


# Generates Comparison Line Graph of Sector Ticker & SPY
@interact(Sector = sectors, Beta = beta)
def v_spy(Sector, Beta):
    ticker = sector_tickers[Sector][Beta]
    file = Path('../Data/{}.csv'.format(ticker))
    df = pd.read_csv(file, infer_datetime_format=True, parse_dates=True, index_col='Date')
    spy = pd.read_csv('../Data/SPY.csv', infer_datetime_format=True, parse_dates=True, index_col='Date')
    fig = make_subplots()
    trace1 = go.Scatter(
        x = df.index,
        y = df['Close'],
        mode = 'lines',
        name = ticker)
    trace2 = go.Scatter(
        x = spy.index,
        y = spy['Close'],
        mode = 'lines',
        name = 'SPY')    
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_xaxes(title_text = 'Date')
    fig.update_yaxes(
        title_text = 'Closing Price (USD)')
    fig.update_layout(title = ticker + " versus SPY", width=1000, height=500)
    return fig


# In[9]:


# Generates Comparison Line Graph of Sector Ticker and its Google Search Interest
@interact(Sector = sectors, Beta = beta, Column = z_field)
def trend(Sector, Beta, Column):
    ticker = sector_tickers[Sector][Beta]
    file = Path('../Data/{}.csv'.format(ticker))
    pytrend.build_payload(kw_list=[ticker], timeframe='today 5-y')
    trend_df = pytrend.interest_over_time().rename_axis('Date')
    trend_df.index = pd.to_datetime(trend_df.index)
    df = pd.read_csv(file, infer_datetime_format=True, parse_dates=True, index_col='Date')
    overlay = pd.merge(trend_df, df[Column], how = 'outer', left_index = True, right_index=True)
    overlay = overlay.loc['2020-06-05':]
    overlay.fillna(method = 'ffill', inplace = True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    trace1 = go.Scatter(
        x = overlay.index,
        y = overlay[Column],
        mode = 'lines',
        name = Column)
    trace2 = go.Scatter(
        x = overlay.index,
        y = overlay[ticker],
        mode = 'lines',
        name = 'Search Interest')
    fig.add_trace(trace1, secondary_y=False)
    fig.add_trace(trace2, secondary_y=True)
    fig.update_yaxes(
        title_text = 'Closing Price (USD)',
        range=[overlay[Column].min()-(overlay[Column].std()*.2),overlay[Column].max()+(overlay[Column].std()*.2)], 
        secondary_y=False)
    fig.update_yaxes(
        title_text = 'Trend Factor',
        range=[0,100], 
        secondary_y=True)
    fig.update_layout(title = ticker + " Closing Price vs Search Interest", 
        xaxis_title = 'Date',
        width=1000, height=500)
    return fig


# In[10]:


# Builds Portfolio from 3 Tickers via Alpaca API, Displays Returns
@interact(Stock_1 = 'GOOG', Amount_1 = (0, 10000), Stock_2 = 'MSFT', Amount_2 = (0, 10000), Stock_3 = 'GME', Amount_3 = (0, 10000))
def api_call(Stock_1, Amount_1, Stock_2, Amount_2, Stock_3, Amount_3):
    x1 = Stock_1.upper()
    x2 = Stock_2.upper()
    x3 = Stock_3.upper()
    tickers = [x1, x2, x3]
    df = alpaca.get_barset(
        tickers,
        timeframe,
        start = start,
        end = end,
        limit = 1000
    ).df
    close = pd.DataFrame()
    close[x1] = df[x1]['close']
    close[x2] = df[x2]['close']
    close[x3] = df[x3]['close']
    portfolio_df = pd.DataFrame()
    shares1 = Amount_1 / df[x1]['close'][0]
    shares2 = Amount_2 / df[x2]['close'][0]
    shares3 = Amount_3 / df[x3]['close'][0]
    portfolio_df[x1] = df[x1]['close'] * shares1
    portfolio_df[x2] = df[x2]['close'] * shares2
    portfolio_df[x3] = df[x3]['close'] * shares3
    fig = px.line(portfolio_df, 
        labels = {
            'value': 'Closing Price (USD)',
            'time': 'Date'
        },
        width=1000, height=500)
    return fig


# In[11]:


# Generates a Boxplot Showing Risk for Each Sector
@interact(Beta = beta)
def boxplot(Beta):
    df = pd.DataFrame()
    sp_file = Path('../Data/SP500.csv')
    sp_df = pd.read_csv(sp_file, infer_datetime_format=True, parse_dates=True, index_col='Date')
    df['SP500'] = sp_df['Close']
    for k, v in sector_tickers.items():
        ticker = sector_tickers[k][Beta]
        file = Path('../Data/{}.csv'.format(ticker))
        ticker_df = pd.read_csv(file, infer_datetime_format=True, parse_dates=True, index_col='Date')
        df[k] = ticker_df['Close']
    df = df.pct_change()
    df.dropna(inplace = True)
    fig = px.box(df, 
        labels = {
            'value': 'Percent Change',
            'variable': 'Sector'
        },
        width=1000, height=500)
    return fig


# In[12]:


# Generates Bar Graph Displaying Sharpe Ratios for Portfolios Designed by Group Members
@interact(Portfolio = member_picks)
def sharpe(Portfolio):
    df = alpaca.get_barset(
        Portfolio, timeframe, start = start, end = end, limit = 504).df
    df.dropna(inplace = True)
    close = pd.DataFrame()
    for i in Portfolio:
        close[i] = df[i]['close']
    close = close.pct_change()
    close.dropna(inplace = True)
    sharpe = close.mean() / close.std() * np.sqrt(252)
    fig = px.bar(sharpe, 
        labels = {
            'value': 'Sharpe Ratio',
            'index': 'Ticker'
        },
        width=1000, height=500)
    fig.update_yaxes(range=[-0.25, 2])
    return fig


# In[13]:


# Builds Panel
dashboard = pn.Tabs(
    ('👋 Hello World', pn.Column(group_members)),
    ('🔥 Sector Heatmap', pn.Column(
        heat_blurb,
        heatmap[0],
        heatmap[1])),
    ('⚖️ Sector Risk', pn.Column(
        box_blurb,
        boxplot[0],
        boxplot[1])),
    ('🚀 Stock Trends', pn.Column(
        heat_blurb, 
        pn.Row(trend[0][0], trend[0][1]), 
        trend[1])),
    ('🕯️ Candlestick', pn.Column(
        candlestick_blurb, 
        pn.Row(candlestick[0][0], candlestick[0][1]), 
        candlestick[1])),
    ('🔭 SPY Performance', pn.Column(
        spy_blurb, 
        pn.Row(v_spy[0][0], v_spy[0][1]), 
        v_spy[1])),
    ('⏳ Time Traveler', pn.Column(
        tt_blurb,
        pn.Row(api_call[0][0], api_call[0][2], api_call[0][4]),
        pn.Row(api_call[0][1], api_call[0][3], api_call[0][5]),
        api_call[1])),
    ('🗡️ Sharpe Ratio', pn.Column(
        sharpe_blurb,
        sharpe[0],
        sharpe[1]))
)


# In[14]:


# Serves Panel
dashboard.servable()


# In[ ]:




