import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt
import calendar
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.layouts import column
from bokeh.palettes import Category10
from bokeh.io import output_notebook
from bokeh.util.serialization import convert_date_to_datetime
from altair import datum

st.title("Investor's Daily")
st.subheader("Investing in Insights: Interactive Tools to Navigate the Stock Market")

# Enable Altair data transformer
alt.data_transformers.enable("default")

# Function to load and preprocess the market data
@st.cache
def load_data():
    df = pd.read_csv("./MarketData.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df.drop(columns=['Unnamed: 0'], inplace=True)
    df['Price_Change'] = df['Adj Close'] - df['Open']
    df['Price_Change_Direction'] = df['Price_Change'].apply(lambda x: 1 if x > 0 else 0)
    df['Price_Percentage_Change'] = ((df['Close'] - df['Open']) / df['Open']) * 100
    df['Price_Percentage_Change_Direction'] = df['Price_Percentage_Change'].apply(lambda x: 1 if x > 0 else 0)
    window_size = 5
    df['Moving_Average'] = df['Adj Close'].rolling(window=window_size).mean()
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Month'].apply(lambda x: calendar.month_name[x])
    ticker_name_mapping = {
        '^NYA': 'New York Stock Exchange',
        '^IXIC': 'NASDAQ',
        '^DJI': 'Dow Jones',
        '^GSPC': 'S&P 500'
    }
    df['Ticker_Name'] = df['Ticker'].map(ticker_name_mapping)
    return df

df = load_data()

# Selection for year for the first Matplotlib plot
year_for_losses_and_profits = st.selectbox('Select Year for Losses and Profits:', options=df['Year'].unique(), key='year1')

# Function to update plot for losses and profits
def update_plot(year):
    filtered_data = df[df['Year'] == year]
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

# Selection for year for the second Matplotlib plot
year_for_price_change = st.selectbox('Select Year for Price Percentage Change:', options=df['Year'].unique(), key='year2')

# Function to plot price percentage change
def plot_price_change(year):
    filtered_data = df[df['Year'] == year]
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

# Selection for year for the Altair chart
year_for_altair = st.selectbox('Select Year for Altair Chart:', options=df['Year'].unique(), key='year3')

# Filtering data for the Altair chart based on selected year
filtered_altair_df = df[df['Year'] == year_for_altair]

# Create the Altair chart
months_order = [calendar.month_name[i] for i in range(1, 13)]
chart = alt.Chart(filtered_altair_df).mark_bar().encode(
    x=alt.X("Month_Name:O", title="Month", sort=months_order, axis=alt.Axis(labelAngle=-45)),
    y=alt.Y("sum(Volume):Q", title="Total Volume"),
    color=alt.Color("Ticker_Name:N", title="Ticker"),
    tooltip=[alt.Tooltip('sum(Volume):Q', title="Volume Sum", format=',.0f')]
).properties(
    title="Monthly Volume Sum for Each Ticker in Selected Year"
)

st.altair_chart(chart, use_container_width=True)

###############################

# Load and preprocess the data
@st.cache
def load_data():
    df = pd.read_csv("./MarketData.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    return df

df = load_data()

# Define ticker names mapping
ticker_names = {
    '^NYA': "NYSE",
    '^IXIC': "NASDAQ",
    '^DJI': "Dow Jones",
    '^GSPC': "S&P 500"
}
df['Ticker_Name'] = df['Ticker'].map(ticker_names)

# Create an interactive slider for the date range
min_date, max_date = df['Date'].min(), df['Date'].max()
min_date_ms = int(min_date.timestamp() * 1000)  # convert to milliseconds
max_date_ms = int(max_date.timestamp() * 1000)
slider = alt.binding_range(min=min_date_ms, max=max_date_ms, step=86400000)  # step is one day in milliseconds
date_selector = alt.selection_single(name="Select", fields=['date'], bind=slider, init={'date': min_date_ms})


# Create the Altair chart
chart = alt.Chart(df).mark_line().encode(
    x=alt.X('Date:T', title="Date"),
    y=alt.Y('Adj Close:Q', title="Adjusted Close"),
    color='Ticker_Name:N',
    tooltip=['Ticker_Name:N', 'Date:T', 'Adj Close:Q']
).add_selection(
    date_selector
).transform_filter(
    (datum.date >= date_selector.date) & (datum.date < date_selector.date + 86400000)  # Filter for the selected day
).properties(
    width=800,
    height=400
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
