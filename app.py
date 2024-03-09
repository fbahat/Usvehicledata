import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as py
import numpy as np
import  requests

base_url = "https://raw.githubusercontent.com/"
url  = base_url + "fbahat/Usvehicledata/main/vehicles_us.csv"
vehicles = pd.read_csv(url)

#Data Organiziting

vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0)
vehicles['paint_color'] = vehicles['paint_color'].fillna('Unknown')
vehicles['cylinders'] = vehicles[['cylinders', 'type']].groupby('type').transform(lambda x:x.fillna(x.median()))
missing_values = vehicles.isnull().any()


# Function to create histogram
def create_histogram(data, column, title):
    histogram = py.histogram(data, x=column, nbins=20, title=title)
    st.plotly_chart(histogram)

def create_scatterplot(data, x_column, y_column, title):
    scatterplot = py.scatter(data, x=x_column, y=y_column, title=title)
    st.plotly_chart(scatterplot)

st.header('US CAR PRICE ANALYSIS')

show_data = st.checkbox('Show Dataset')

if show_data:
    st.write(vehicles)
# Histogram of price
st.subheader("Histograms")
create_histogram(vehicles, 'price', 'Price Distribution')
create_histogram(vehicles, 'odometer', 'Odometer Distribution')

# Histogram of odometer
st.subheader("Scatterplots")
create_scatterplot(vehicles, 'price', 'odometer', 'Price vs Odometer')
create_scatterplot(vehicles, 'price', 'model_year', 'Price vs Model Year')

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

# Check for missing values in 'model' and 'type' columns
missing_values = vehicles[['model', 'type']].isnull().any()
if missing_values.any():
    st.error("There are missing values in the dataset. Please clean the data and try again.")
else:
    # Group by manufacturer and get unique vehicle types
    vehicle_types_by_manufacturer = vehicles.groupby('model')['type'].unique().reset_index()

    # Create Altair chart
    st.header("Comparison of Vehicle Brands with Their Types")
    chart = alt.Chart(vehicle_types_by_manufacturer).mark_bar().encode(
        x=alt.X('model:N', title='Manufacturer'),
        y=alt.Y('count(type):Q', title='Number of Vehicle Types'),
        color=alt.Color('model:N', legend=None),
        tooltip=['model:N', 'count(type):Q']
    ).properties(
        width=600,
        height=400,
        title="Comparison of Vehicle Brands with Their Types"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
# Check for missing values in 'model' and 'fuel' columns
missing_values = vehicles[['model', 'fuel']].isnull().any()
if missing_values.any():
    st.error("There are missing values in the dataset. Please clean the data and try again.")
else:
    # Group by manufacturer and get count of each fuel type
    fuel_count_by_manufacturer = vehicles.groupby('model')['fuel'].value_counts().reset_index(name='count')

    # Create Altair chart
    st.header("Comparison of Vehicle Fuel Types by Manufacturer")
    chart = alt.Chart(fuel_count_by_manufacturer).mark_bar().encode(
        x=alt.X('model:N', title='Manufacturer'),
        y=alt.Y('count:Q', title='Count of Vehicles'),
        color=alt.Color('fuel:N', legend=alt.Legend(title="Fuel Type")),
        tooltip=['model:N', 'fuel:N', 'count:Q']
    ).properties(
        width=600,
        height=400,
        title="Comparison of Vehicle Fuel Types by Manufacturer"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
