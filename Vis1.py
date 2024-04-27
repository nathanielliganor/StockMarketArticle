import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.title("Investor's Daily")
st.markdown("""
Article By: Ayush Shah and Nathaniel Liganor
""")
st.subheader("Investing in Insights: Interactive Tools to Navigate the Stock Market")

st.markdown("""
Detailed description omitted for brevity.
""")

# Function to load the market data
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

# Streamlit selection for year for the first visualization
year_for_losses_and_profits = st.selectbox('Select Year for Losses and Profits:', unique_years, key='year1')

# Function to update plot for losses and profits
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
    ax.set_title(f'Counts of Losses and Profits Occurred Per Day by Ticker ({year})')
    ax.set_xticks(x)
    ax.set_xticklabels(tickers)
    ax.legend()
    st.pyplot(fig)

update_plot(year_for_losses_and_profits)

# Streamlit selection for year for the second visualization
year_for_price_change = st.selectbox('Select Year for Price Percentage Change:', unique_years, key='year2')

# Function to plot price percentage change
def plot_price_change(year):
    filtered_data = market_data[market_data['Date'].dt.year == year]
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_data['Date'].dt.strftime('%Y-%m-%d'), filtered_data['Price_Percentage_Change'],
            width=0.5, color='blue')
    plt.title(f'Bar Chart of Price Percentage Change for Year: {year}')
    plt.xlabel('Date')
    plt.ylabel('Percentage Change (%)')
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

plot_price_change(year_for_price_change)
