import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the market data
@st.cache
def load_data():
    market_data = pd.read_csv("./MarketData.csv")
    market_data['Date'] = pd.to_datetime(market_data['Date'])
    market_data.drop(columns=['Unnamed: 0'], inplace=True)

    market_data['Price_Change'] = market_data['Adj Close'] - market_data['Open']
    market_data['Price_Change_Direction'] = market_data['Price_Change'].apply(lambda x: 1 if x > 0 else 0)
    market_data['Price_Percentage_Change'] = ((market_data['Close'] - market_data['Open']) / market_data['Open']) * 100
    market_data['Price_Percentage_Change_Direction'] = market_data['Price_Percentage_Change'].apply(lambda x: 1 if x > 0 else 0)
    window_size = 5
    market_data['Moving_Average'] = market_data['Adj Close'].rolling(window=window_size).mean()
    return market_data

market_data = load_data()
unique_years = sorted(market_data['Date'].dt.year.unique())

# Streamlit selection for year
year = st.selectbox('Select Year:', unique_years)

def update_plot(year):
    filtered_data = market_data[market_data['Date'].dt.year == year]
    grouped_data = filtered_data.groupby('Ticker')['Price_Change_Direction'].value_counts().unstack().fillna(0)
    tickers = grouped_data.index
    zeros = grouped_data[0].values
    ones = grouped_data[1].values
    x = np.arange(len(tickers))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, zeros, width, label='Losses per day')
    ax.bar(x + width/2, ones, width, label='Profits per day')

    ax.set_xlabel('Ticker')
    ax.set_ylabel('Count')
    ax.set_title(f'Counts of losses and profits occurred per day by Ticker ({year})')
    ax.set_xticks(x)
    ax.set_xticklabels(tickers)
    ax.legend()

    st.pyplot(fig)

update_plot(year)
