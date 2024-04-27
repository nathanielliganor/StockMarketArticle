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

st.markdown("""
In today’s rapidly evolving financial landscape, understanding the stock market’s complex dynamics is crucial for both season investors and newcomers alike. This article aims to demystify the intricacies of stock markets through a series of interactive visualizations that bring clarity to the historical performance and current state of major stock market indices, sectoral impacts, and real-time market fluctuations. From exploring long-term trends and volatility in iconic indices such as the S&P 500, Dow Jones, and NASDAQ, to dissecting the performance across diverse sectors like technology, healthcare, and finance, and finally to providing up-to-the-minute updates via a real-time ticker and news feed, these visualizations offer a comprehensive look into the forces shaping our financial world. Each component is designed to not only inform but also engage users, facilitating a deeper understanding of how historical trends and current events converge to influence market behavior.

Navigating the intricate world of stock markets requires a firm grasp of historical context and real-time data analysis. Our interactive visualizations provide a multifaceted exploration, enabling readers to delve into the ebbs and flows that have shaped market trajectories over the past decade and a half. Through intuitive visual representations, we unravel the performances of industry titans across the S&P 500, Dow Jones, and NASDAQ, shedding light on their resilience, adaptability, and growth amidst ever-changing economic landscapes.

Diving deeper, our sector-specific analyses offer a nuanced perspective, dissecting the triumphs and tribulations witnessed by technology frontrunners, the steady prowess of healthcare giants, and the pivotal role of finance institutions. These visualizations go beyond mere numbers, painting a vivid picture of how innovation, regulatory shifts, and global events have impacted these vital sectors, ultimately influencing the broader market dynamics.

Moreover, our real-time data integration ensures that readers remain at the forefront of market developments. The live ticker and news feed provide instantaneous updates, capturing the pulse of the financial world as it unfolds. Whether tracking sudden market fluctuations, monitoring breaking news, or staying abreast of emerging trends, these features empower users to make informed decisions and stay ahead of the curve..
""")

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

st.subheader("A Decade and a Half of Market Volatility and Resilience")


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

year_for_losses_and_profits = st.selectbox('Select Year for Losses and Profits:', options=df['Year'].unique(), key='year1')
update_plot(year_for_losses_and_profits)
# Selection for year for the first Matplotlib plot

st.markdown("""
Over the span of 15 tumultuous years from 2008 to 2023, the major U.S. stock indices—the S&P 500, Dow Jones Industrial Average, NASDAQ, 
and New York Stock Exchange—have ridden waves of significant economic upheaval, reflective of investor sentiment and global events. Starting
with the 2008 financial crisis, which sent shockwaves through global markets, these indices experienced precipitous declines, testing the resolve 
of investors. The subsequent recovery phases were punctuated by key events such as the European debt crisis in 2011, the U.S.-China trade wars starting 
in 2018, and the unprecedented global impact of the COVID-19 pandemic in 2020. Each event left a distinct mark on the indices, with rapid losses followed 
by often vigorous recoveries, showcasing the resilience of markets.

During these years, technology booms drove NASDAQ to new heights, while traditional industries bolstered the Dow Jones and NYSE, illustrating a diversification 
in investor confidence across sectors. The S&P 500, often considered a bellwether for the overall U.S. economy, displayed a steady climb interrupted by brief yet 
intense periods of volatility, mirroring investor sentiment that fluctuated between optimism and caution. The rise of digital trading platforms and algorithmic 
trading also transformed market dynamics, leading to faster recoveries and more pronounced swings. As we look towards the future, understanding these patterns of 
profit and loss becomes crucial for predicting market trends and guiding investor strategies, embodying the ever-evolving spirit of the financial landscape.
""")

# Selection for year for the second Matplotlib plot
year_for_price_change = st.selectbox('Select Year for Price Percentage Change:', options=df['Year'].unique(), key='year2')

# Function to plot price percentage change
def plot_price_change(year):
    filtered_data = df[df['Year'] == year]
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_data['Date'], filtered_data['Price_Percentage_Change'],
            width=0.5, color='blue')
    plt.title('Bar Chart of Price Percentage Change')
    plt.xlabel('Date')
    plt.ylabel('Percentage Change')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

plot_price_change(year_for_price_change)

st.markdown("""
    
Continuing from the dramatic shifts observed over the past fifteen years, the percentage changes in the prices of the major indices offer a more granular view of the stock market's growth and its broader economic implications. For instance, the strong rebounds seen in NASDAQ, predominantly fueled by the tech sector's exponential growth,
highlight the increasing importance of technology in the global economy. Similarly, the steady gains in the S&P 500 reflect the diversified nature of this index and underscore the gradual expansion of the U.S. economy across a broader range of industries. However, these percentage increases are not just numbers on a chart; they represent 
the confidence of investors in the market's stability and future growth potential.

Significant dips, often triggered by international crises or domestic policy shifts, momentarily shake this confidence, yet the historical resilience of these indices suggests a robust economic foundation capable of withstanding such shocks. This elasticity not only reassures investors about short-term recoveries but also paints a broader 
picture of long-term economic fortitude. As we dissect these percentage changes, we glean insights into the cyclical nature of markets and the pivotal role of investor sentiment in driving economic cycles. Understanding these dynamics is essential for anyone looking to navigate the complexities of investing and economic forecasting.
""")

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
