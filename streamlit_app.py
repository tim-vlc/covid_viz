import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


@st.cache_data
def load_data():
    df = pd.read_csv("owid-covid-data.csv")
    df['date'] = pd.to_datetime(df['date'])
    
    df['month'] = df['date'].dt.to_period('M')
    
    monthly_df = df.groupby(['location', 'month'])['new_cases'].sum().reset_index()
    
    monthly_df['month'] = monthly_df['month'].dt.to_timestamp()
    
    return monthly_df


def main():
    st.set_page_config(layout="wide")
    st.title("COVID-19 Monthly New Cases World Map")

    covid_df = load_data()

    min_month = covid_df['month'].min().date().replace(day=1)
    max_month = covid_df['month'].max().date().replace(day=1)

    selected_month = st.slider(
        "Select a month",
        min_value=min_month,
        max_value=max_month,
        value=min_month,
        format="YYYY-MM"
    )

    filtered_df = covid_df[covid_df['month'].dt.to_period('M') == pd.Period(selected_month, freq='M')]

    filtered_df['new_cases_filled'] = filtered_df['new_cases'].fillna(0)

    filtered_df['new_cases_log'] = np.log1p(filtered_df['new_cases_filled'])

    max_cases = filtered_df['new_cases_filled'].max() if filtered_df['new_cases_filled'].max() > 100_000 else 100_000
    bins = [0, 1000, 10000, 50000, max_cases]
    labels = [10, 20, 30, 40]  

    filtered_df['circle_size'] = pd.cut(filtered_df['new_cases_filled'], bins=bins, labels=labels, include_lowest=True)

    fig = px.scatter_geo(
        filtered_df,
        locations="location",
        locationmode="country names",
        color_discrete_sequence=["skyblue"],  
        hover_name="location",
        hover_data={
            "new_cases_filled": ":,.0f",  
            "new_cases_log": False,
        },
        size="circle_size",  
        projection="natural earth",
        title=f"COVID-19 New Cases for {selected_month.strftime('%B %Y')}",
        size_max=40  
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

    circle_legend = {
        "2": "0-1,000 new cases",
        "5": "1,001-10,000 new cases",
        "15": "10,001-50,000 new cases",
        "30": "50,001+ new cases"
    }

    fig.update_layout(
        height=900,  
        margin={"r": 0, "t": 50, "l": 0, "b": 0},  
        geo=dict(
            showframe=False,
            showcoastlines=True,
        ),
        legend=dict(
            title="Circle Size Legend",  
            itemsizing="constant",
            traceorder="normal"
        )
    )

    for size, label in circle_legend.items():
        fig.add_trace(
            go.Scattergeo(
                lon=[None],  
                lat=[None],  
                mode="markers",
                marker=dict(size=int(size), color="skyblue", sizemode='area'),
                name=label
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        st.subheader(f"New Cases Data for {selected_month.strftime('%B %Y')}")
        
    st.dataframe(filtered_df[['location', 'new_cases_filled']].sort_values('new_cases_filled', ascending=False))
    st.subheader("Summary Statistics")
    st.write(f"Total New Cases: {filtered_df['new_cases_filled'].sum():,.0f}")
    st.write(f"Average New Cases per Country: {filtered_df['new_cases_filled'].mean():,.2f}")
    st.write(f"Median New Cases: {filtered_df['new_cases_filled'].median():,.0f}")
    st.write(f"Maximum New Cases: {filtered_df['new_cases_filled'].max():,.0f}")

if __name__ == "__main__":
    main()