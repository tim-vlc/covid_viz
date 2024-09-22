import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


@st.cache_data
def load_data():
    df = pd.read_csv("owid-covid-data.csv")
    df['date'] = pd.to_datetime(df['date'])
    
    df['month'] = df['date'].dt.to_period('M')
    
    monthly_df = df.groupby(['location', 'month'])['new_cases'].sum().reset_index()
    
    monthly_df['month'] = monthly_df['month'].dt.to_timestamp()
    
    return monthly_df


def setup_slider(min_month, max_month):
    selected_month = st.slider(
        "Select a month",
        min_value=min_month,
        max_value=max_month,
        value=min_month,
        format="YYYY-MM",
    )
    
    return selected_month


def summary_data(filtered_df, selected_month):
    # Dashboard for showing summary data
    st.subheader(f"New Cases Data for {selected_month.strftime('%B %Y')}")
    st.dataframe(filtered_df[['location', 'new_cases_per_month']].sort_values('new_cases_per_month', ascending=False))
    st.subheader("Summary Statistics")
    st.write(f"Total New Cases: {filtered_df['new_cases_per_month'].sum():,.0f}")
    st.write(f"Average New Cases per Country: {filtered_df['new_cases_per_month'].mean():,.2f}")
    st.write(f"Median New Cases: {filtered_df['new_cases_per_month'].median():,.0f}")
    st.write(f"Maximum New Cases: {filtered_df['new_cases_per_month'].max():,.0f}")


def main_map(filtered_df, selected_month):
    # World map itself
    fig = px.scatter_geo(
        filtered_df,
        locations="location",
        locationmode="country names",
        color_discrete_sequence=["skyblue"],  
        hover_name="location",
        hover_data={
            "new_cases_per_month": ":,.0f",  
            "cases_size": False,
        },
        size="cases_size",
        projection="mercator",
        title=f"COVID-19 New Cases for {selected_month.strftime('%B %Y')}",
        size_max=150,
    )

    fig.update_geos(
        showcoastlines=True, coastlinecolor="Black",
        showland=True, landcolor="LightGray",
        showocean=True, oceancolor="white",
        showlakes=True, lakecolor="white",
        showcountries=True, countrycolor="Gray",
        fitbounds="locations",
        projection_type="natural earth"
    )

    fig.update_traces(marker=dict(
        opacity=0.8,  
        line=dict(width=0),  
        color="skyblue"  
    ))

    fig.update_layout(
        height=900,  
        margin={"r": 0, "t": 50, "l": 0, "b": 0},  
        geo=dict(
            showframe=False,
            showcoastlines=True,
        )
    )

    st.plotly_chart(fig, use_container_width=True)


def main():
    st.set_page_config(layout="wide")
    st.title("COVID-19 Monthly New Cases World Map")

    # 1. Import Data
    covid_df = load_data()

    # 2. Set up preliminary variables
    min_month = covid_df['month'].min().date().replace(day=1)
    max_month = covid_df['month'].max().date().replace(day=1)

    # 3. Show slider, the main component of our page
    selected_month = setup_slider(min_month, max_month)

    # 4. Create filetered DataFrame based on the month selected with the slider
    filtered_df = covid_df[covid_df['month'].dt.to_period('M') == pd.Period(selected_month, freq='M')]
    filtered_df['new_cases_per_month'] = filtered_df['new_cases'].fillna(0)
    filtered_df['cases_size'] = (filtered_df['new_cases_per_month'] / 200_000) * 20

    # 5. Show main map + summary data at the end of the page
    main_map(filtered_df, selected_month)
    summary_data(filtered_df, selected_month)


if __name__ == "__main__":
    main()