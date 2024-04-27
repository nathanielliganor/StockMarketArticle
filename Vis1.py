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
import calendar


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


st.markdown("""
### Data Manipulation
Market data, often stored in files like "MarketData.csv," undergoes a series of essential transformations to unlock its insights for investors. Think of it as refining raw material to extract its purest form. Initially, the data's time references are standardized using a process known as datetime conversion (pd.to_datetime()).
This ensures that all dates are in a consistent format, making comparisons across different time periods accurate and meaningful. Next, unnecessary clutter is removed from the dataset. This involves eliminating extraneous columns that don't contribute to the analysis or understanding of market trends (drop(columns=['Unnamed: 0'])). 
These could be placeholder columns or data labels that serve no analytical purpose. The manipulation of market data involves calculating key metrics such as Price Change and Percentage Change, which offer crucial insights into how asset prices fluctuate over time. Price Change indicates whether an asset's price increased or decreased 
during a specific period by measuring the difference between its closing and opening prices. Percentage Change, on the other hand, expresses the relative change in an asset's price as a percentage of the opening price, providing valuable context regarding the magnitude of price movements. Additionally, employing advanced techniques like 
moving averages further enhances our understanding of market trends. By smoothing out short-term fluctuations, moving averages reveal the underlying trend in asset prices over defined periods. In essence, this data manipulation process refines raw market data into actionable intelligence, forming the bedrock of informed investment decisions and empowering investors to navigate the complexities of finance with confidence.
""")

# Enable data transformer for Altair
alt.data_transformers.enable("default")

df = pd.read_csv("./MarketData.csv")

# Data preprocessing
df['Date'] = pd.to_datetime(df['Date'])
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
months_order = [calendar.month_name[i] for i in range(1, 13)]

# Streamlit UI elements
year = st.selectbox('Select a Year:', options=df['Year'].unique())

# Filtering data based on selected year
filtered_df = df[df['Year'] == year]

# Create the chart
chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("Month_Name:O", title="Month", sort=months_order, axis=alt.Axis(labelAngle=-45)),
    y=alt.Y("sum(Volume):Q", title="Total Volume"),
    color=alt.Color("Ticker_Name:N", title="Ticker"),
    tooltip=[alt.Tooltip('sum(Volume):Q', title="Volume Sum", format=',.0f')]
).properties(
    title="Monthly Volume Sum for Each Ticker in Selected Year"
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)

st.markdown("""
Delving into the intricacies of trading volume, our interactive visualization presents a compelling overview of the
monthly volume sums for each major US stock index from 2008 to 2023. This tool not only highlights the sheer scale of 
trading activity over time but also enables users to pinpoint specific moments of heightened volatility or unusual market tranquility. 
By hovering over the data points, users gain insights into the total trading volumes for indices like the S&P 500, Dow Jones, and 
NASDAQ—allowing them to observe how major events, such as economic recessions, technological breakthroughs, or geopolitical tensions, 
correlate with spikes or dips in market activity. This visualization is integral to understanding the rhythm of the market and equips 
investors with the knowledge to assess how external factors drive trading behaviors. Through this dynamic interface, readers can trace 
the ebb and flow of the market's pulse, providing a deeper appreciation of how historical and current events shape financial landscapes 
and influence investment strategies.
""")

