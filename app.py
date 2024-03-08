import pandas as pd
import streamlit as st
import altair as at
import plotly.express as py
import numpy as np


vehicles = pd.read_csv("https://github.com/fbahat/Usvehicledata/blob/main/vehicles_us.csv")

print(vehicles.head(10))

vehicles.isna()
vehicles.isna().sum()
vehicles.duplicated().sum() 

vehicles['fuel'].unique()

# Histogram of price
price_histogram = py.histogram(vehicles, x='price', nbins=20, title='Price Distribution')
st.plotly_chart(price_histogram)

# Histogram of odometer
odometer_histogram = py.histogram(vehicles, x='odometer', nbins=20, title='Odometer Distribution')
st.plotly_chart(odometer_histogram)

# Scatterplot of price vs odometer
price_vs_odometer_scatter = py.scatter(vehicles, x='price', y='odometer', title='Price vs Odometer')
st.plotly_chart(price_vs_odometer_scatter)

# Scatterplot of price vs model_year
price_vs_model_year_scatter = py.scatter(vehicles, x='price', y='model_year', title='Price vs Model Year')
st.plotly_chart(price_vs_model_year_scatter)
