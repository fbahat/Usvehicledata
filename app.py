import pandas as pd
import streamlit as st
import altair as at
import plotly.express as py
import numpy as np
from matplotlib import pyplot as plt
import  requests

base_url = "https://raw.githubusercontent.com/"
url  = base_url + "fbahat/Usvehicledata/main/vehicles_us.csv"
vehicles = pd.read_csv(url)

st.header('US CAR PRICE ANALYSIS')

show_data = st.checkbox('Show Dataset')
if show_data:
    st.write(vehicles)
# Histogram of price
price_histogram = py.histogram(vehicles, x='price', nbins=20, title='Price Distribution')
show_price_histogram = st.checkbox('Show Price Distribution Histogram')
if show_price_histogram:
    st.plotly_chart(price_histogram)

# Histogram of odometer
odometer_histogram = py.histogram(vehicles, x='odometer', nbins=20, title='Odometer Distribution')
show_odometer_histogram = st.checkbox('Show Odometer Distribution Histogram')
if show_odometer_histogram:
    st.plotly_chart(odometer_histogram)

# Scatterplot of price vs odometer
price_vs_odometer_scatter = py.scatter(vehicles, x='price', y='odometer', title='Price vs Odometer')
show_price_vs_odometer_scatter = st.checkbox('Show Price vs Odometer Scatterplot')
if show_price_vs_odometer_scatter:
    st.plotly_chart(price_vs_odometer_scatter)

# Scatterplot of price vs model_year
price_vs_model_year_scatter = py.scatter(vehicles, x='price', y='model_year', title='Price vs Model Year')
show_price_vs_model_year_scatter = st.checkbox('Show Price vs Model Year Scatterplot')
if show_price_vs_model_year_scatter:
    st.plotly_chart(price_vs_model_year_scatter)

# Vehicle condition by model year
vehicle_types = py.scatter(vehicles, x='condition', y='model_year', title='Price vs Model Year')
vehicle_types_show = st.checkbox('Show Condition vs Model Year Scatterplot')
if vehicle_types_show:
    st.plotly_chart(vehicle_types)


# Check for missing values in 'model' column
if vehicles['model'].isnull().any():
    st.error("There are missing values in the 'model' column. Please clean the data and try again.")
else:
    # Check if 'model' column contains strings
    if not vehicles['model'].apply(lambda x: isinstance(x, str)).all():
        st.error("The 'model' column contains non-string values. Please clean the data and try again.")
    else:
        # Split 'model' column into 'manufacturer' and 'model'
        vehicles[['manufacturer', 'model']] = vehicles['model'].str.split(n=1, expand=True)

        # Group by manufacturer and get unique vehicle types
        vehicle_types_by_manufacturer = vehicles.groupby(['manufacturer', 'model'])['type'].unique().reset_index()

        # Plot the chart
        st.header("Vehicle Types by Manufacturer")
        fig = py.bar(vehicle_types_by_manufacturer, x='manufacturer',
                    y=vehicle_types_by_manufacturer['type'].apply(lambda x: len(x)),
                    color='model',
                    title="Vehicle Types by Manufacturer",
                    labels={'manufacturer':'Manufacturer', 'type':'Number of Vehicle Types', 'model': 'Model'})
        st.plotly_chart(fig)
# Check for missing values in 'model' and 'type' columns
missing_values = vehicles[['model', 'type']].isnull().any()
if missing_values.any():
    st.error("There are missing values in the dataset. Please clean the data and try again.")
else:
    # Group by manufacturer and get unique vehicle types
    vehicle_types_by_manufacturer = vehicles.groupby('model')['type'].unique().reset_index()

    # Plot the chart
    st.header("Comparison of Vehicle Brands with Their Types")
    fig = py.bar(vehicle_types_by_manufacturer, x='model',
                 y=vehicle_types_by_manufacturer['type'].apply(lambda x: len(x)),
                 title="Comparison of Vehicle Brands with Their Types",
                 labels={'model': 'Manufacturer', 'type': 'Number of Vehicle Types'})
    st.plotly_chart(fig)
