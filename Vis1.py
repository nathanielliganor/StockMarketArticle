import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt
import calendar
from altair import datum
import calendar

st.title("Investor's Daily")
st.subheader("Charting the Course: Navigating the Complexities of the Stock Market Through Data Insights and Investor Sentiment, 2008-2023")

st.markdown("""
In today’s rapidly evolving financial landscape, understanding the stock market’s complex dynamics is crucial for both season investors and newcomers alike. This article aims to demystify the intricacies of stock markets through a series of interactive visualizations that bring clarity to the historical performance and current state of major stock market indices, sectoral impacts, and real-time market fluctuations. From exploring long-term trends and volatility in iconic indices such as the S&P 500, Dow Jones, and NASDAQ, to dissecting the performance across diverse sectors like technology, healthcare, and finance, and finally to providing up-to-the-minute updates via a real-time ticker and news feed, these visualizations offer a comprehensive look into the forces shaping our financial world. Each component is designed to not only inform but also engage users, facilitating a deeper understanding of how historical trends and current events converge to influence market behavior.

Navigating the intricate world of stock markets requires a firm grasp of historical context and real-time data analysis. Our interactive visualizations provide a multifaceted exploration, enabling readers to delve into the ebbs and flows that have shaped market trajectories over the past decade and a half. Through intuitive visual representations, we unravel the performances of industry titans across the S&P 500, Dow Jones, and NASDAQ, shedding light on their resilience, adaptability, and growth amidst ever-changing economic landscapes.

Diving deeper, our sector-specific analyses offer a nuanced perspective, dissecting the triumphs and tribulations witnessed by technology frontrunners, the steady prowess of healthcare giants, and the pivotal role of finance institutions. These visualizations go beyond mere numbers, painting a vivid picture of how innovation, regulatory shifts, and global events have impacted these vital sectors, ultimately influencing the broader market dynamics.

Moreover, our real-time data integration ensures that readers remain at the forefront of market developments. The live ticker and news feed provide instantaneous updates, capturing the pulse of the financial world as it unfolds. Whether tracking sudden market fluctuations, monitoring breaking news, or staying abreast of emerging trends, these features empower users to make informed decisions and stay ahead of the curve.
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


st.subheader(" Understanding Market Growth Through Percentage Changes")
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
The monthly volume sums for each major U.S. stock index reveal a dynamic narrative of trading activity, offering deep insights into the market’s responsiveness to global events and technological advancements. Over the years, trading volumes in indices such as the S&P 500, Dow Jones, NASDAQ, and NYSE have shown significant fluctuations, 
correlating directly with key economic indicators and major global events. For instance, the financial crisis of 2008 saw trading volumes spike as panic selling ensued, while volumes surged again during the rapid market growth driven by technological innovations in the 2010s, especially within the NASDAQ, which is heavily weighted towards tech companies.

Further, geopolitical tensions such as the U.S.-China trade wars or Brexit negotiations often led to increased market volatility, reflected in higher trading volumes as investors reacted to potential economic impacts. Conversely, periods of market stability and investor confidence typically saw more moderate trading volumes. Each spike or dip provides
a snapshot of investor sentiment at that moment—whether driven by fear, optimism, or strategic recalibration. Analyzing these trends helps investors understand not just the "what" and "when" of trading, but also the "why," offering invaluable insights into the mechanics of market dynamics and economic resilience.
""")

screenshot_path = "./Screenshot 2024-04-27 at 4.19.38 AM.png"
html_file_path = "./stock_graph.html"

st.subheader("The Dynamics of Market Indices")
st.image(screenshot_path, caption='Your Screenshot', use_column_width=True)
st.caption("""
Disclaimer: Streamlit does not support Bokeh v3.x, unable to host interactive visualization. 
[See link for visualization](https://huggingface.co/spaces/nathanielliganor/NarrativeVisualization/blob/main/IndexPerformace.ipynb)
""")

st.markdown("""
Analyzing the performance of major market indices against each other from 2008 to 2023 unveils a rich tapestry of interwoven trends and divergences. While each index—S&P 500, Dow Jones, NASDAQ, and NYSE—tends to track the overall market sentiment, nuanced differences emerge, reflecting sectoral strengths, economic policies, and global shifts. 
For instance, the NASDAQ's heavy weighting towards technology often leads to more pronounced gains during tech booms, contrasting with the broader-based S&P 500, which offers a more diversified snapshot of the economy. The Dow Jones, comprising thirty blue-chip companies, is often seen as a barometer of industrial and economic health, while the 
NYSE reflects a broader spectrum of companies and industries. Over the years, these indices have displayed varying degrees of resilience and volatility, mirroring the ever-evolving landscape of global finance. Understanding these nuances is essential for investors seeking to diversify their portfolios and capitalize on emerging opportunities in 
an increasingly interconnected market.
""")

st.markdown("""
Our exploration of the stock market indices spanning the years 2008 to 2023 unveils a captivating saga of resilience, volatility, and interconnectedness. From the depths of the financial crisis to the heights of technological innovation, these indices have served as barometers of economic health and bellwethers of investor sentiment.
Through our analysis, we have witnessed the profound impact of global events, geopolitical tensions, and technological breakthroughs on market dynamics, offering invaluable insights into the intricate dance between economics and human behavior. Moreover, our examination of comparative performance among indices sheds light on sectoral strengths and 
weaknesses, providing investors with a roadmap to navigate the complexities of the financial landscape. As we reflect on this journey, we are reminded of the profound interplay between market forces and broader societal trends, underscoring the interconnectedness of global economies and the imperative of informed decision-making in an ever-evolving world.
""")
