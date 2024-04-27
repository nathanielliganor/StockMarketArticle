import streamlit as st
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.layouts import column
from bokeh.palettes import Category10
from bokeh.io import output_notebook

# Load the market data
@st.cache_data
def load_data():
    df = pd.read_csv("./MarketData.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

p = figure(height=400, width=800, tools="xpan", x_axis_type="datetime",
           x_range=(df['Date'].min(), df['Date'].max()))

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                height=130, width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = 'navy'
range_tool.overlay.fill_alpha = 0.2
select.add_tools(range_tool)
select.ygrid.grid_line_color = None

colors = Category10[10]

ticker_names = {
    '^NYA': "NYSE",
    '^IXIC': "NASDAQ",
    '^DJI': "Dow Jones",
    '^GSPC': "S&P 500"
}

for i, (ticker, group) in enumerate(df.groupby('Ticker')):
    ticker_name = ticker_names.get(ticker, ticker)  # Use mapping, default to ticker if not found
    source = ColumnDataSource(data={
        'date': group['Date'],
        'close': group['Adj Close']
    })
    color = colors[i % len(colors)]
    p.line(x='date', y='close', source=source, legend_label=ticker_name, color=color, line_width=2.5)
    select.line(x='date', y='close', source=source, color=color, line_width=2.5)

p.legend.title = "Ticker"
p.legend.location = 'top_left'

# Display the Bokeh plot in the Streamlit app
st.bokeh_chart(column(p, select), use_container_width=True)
