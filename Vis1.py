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
In today’s rapidly evolving financial landscape, understanding the stock market’s complex dynamics is crucial for both season investors and newcomers alike. This article aims to demystify the intricacies of stock markets through a series of interactive visualizations that bring clarity to the historical performance and current state of major stock market indices, sectoral impacts, and real-time market fluctuations. From exploring long-term trends and volatility in iconic indices such as the S&P 500, Dow Jones, and NASDAQ, to dissecting the performance across diverse sectors like technology, healthcare, and finance, and finally to providing up-to-the-minute updates via a real-time ticker and news feed, these visualizations offer a comprehensive look into the forces shaping our financial world. Each component is designed to not only inform but also engage users, facilitating a deeper understanding of how historical trends and current events converge to influence market behavior.

Navigating the intricate world of stock markets requires a firm grasp of historical context and real-time data analysis. Our interactive visualizations provide a multifaceted exploration, enabling readers to delve into the ebbs and flows that have shaped market trajectories over the past decade and a half. Through intuitive visual representations, we unravel the performances of industry titans across the S&P 500, Dow Jones, and NASDAQ, shedding light on their resilience, adaptability, and growth amidst ever-changing economic landscapes.

Diving deeper, our sector-specific analyses offer a nuanced perspective, dissecting the triumphs and tribulations witnessed by technology frontrunners, the steady prowess of healthcare giants, and the pivotal role of finance institutions. These visualizations go beyond mere numbers, painting a vivid picture of how innovation, regulatory shifts, and global events have impacted these vital sectors, ultimately influencing the broader market dynamics.

Moreover, our real-time data integration ensures that readers remain at the forefront of market developments. The live ticker and news feed provide instantaneous updates, capturing the pulse of the financial world as it unfolds. Whether tracking sudden market fluctuations, monitoring breaking news, or staying abreast of emerging trends, these features empower users to make informed decisions and stay ahead of the curve..
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

# Streamlit selection for year
year = st.selectbox('Select Year:', unique_years)

# Define the ticker names mapping
ticker_names = {
    '^NYA': "NYSE",
    '^IXIC': "NASDAQ",
    '^DJI': "Dow Jones",
    '^GSPC': "S&P 500"
}

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

# Function to plot price percentage change
def plot_price_change(year):
    filtered_data = market_data[market_data['Date'].dt.year == year]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_data['Date'].dt.strftime('%Y-%m-%d'), filtered_data['Price_Percentage_Change'],
            width=0.5, color='blue')  # Adjust width as needed

    plt.title(f'Bar Chart of Price Percentage Change for Year: {year}')
    plt.xlabel('Date')
    plt.ylabel('Percentage Change (%)')
    
    # Improve the date formatting and set x-axis to show only month-start ticks
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Adjust interval as needed
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(plt)

# Call the functions to update the plots
update_plot(year)

st.markdown("""
### Data Manipulation
Market data, often stored in files like "MarketData.csv," undergoes a series of essential transformations to unlock its insights for investors. Think of it as refining raw material to extract its purest form. Initially, the data's time references are standardized using a process known as datetime conversion (pd.to_datetime()).
This ensures that all dates are in a consistent format, making comparisons across different time periods accurate and meaningful. Next, unnecessary clutter is removed from the dataset. This involves eliminating extraneous columns that don't contribute to the analysis or understanding of market trends (drop(columns=['Unnamed: 0'])). 
These could be placeholder columns or data labels that serve no analytical purpose. The manipulation of market data involves calculating key metrics such as Price Change and Percentage Change, which offer crucial insights into how asset prices fluctuate over time. Price Change indicates whether an asset's price increased or decreased 
during a specific period by measuring the difference between its closing and opening prices. Percentage Change, on the other hand, expresses the relative change in an asset's price as a percentage of the opening price, providing valuable context regarding the magnitude of price movements. Additionally, employing advanced techniques like 
moving averages further enhances our understanding of market trends. By smoothing out short-term fluctuations, moving averages reveal the underlying trend in asset prices over defined periods. In essence, this data manipulation process refines raw market data into actionable intelligence, forming the bedrock of informed investment decisions and empowering investors to navigate the complexities of finance with confidence.
""")

plot_price_change(year)
