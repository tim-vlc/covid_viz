import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv("owid-covid-data.csv")
    df['date'] = pd.to_datetime(df['date'])
    
    df['month'] = df['date'].dt.to_period('M')
    df['quarter'] = df['date'].dt.to_period('Q')
    
    monthly_df = df.groupby(['location', 'month'])['new_cases'].sum().reset_index()
    quarterly_df = df.groupby(['location', 'quarter'])['new_cases'].sum().reset_index()
    
    monthly_df['month'] = monthly_df['month'].dt.to_timestamp()
    quarterly_df['quarter'] = quarterly_df['quarter'].dt.to_timestamp()
    
    return monthly_df, quarterly_df


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


def bar_plot(filtered_df):
    countries_to_exclude = [
        'World', 'Asia', 'Europe', 'North America', 
        'South America', 'Africa', 'Oceania', 'European Union (27)',
        'Upper-middle-income countries', 'Lower-middle-income countries', "High-income countries"
    ]
    sorted_df = filtered_df[~filtered_df['location'].isin(countries_to_exclude)].sort_values('new_cases_per_month', ascending=False)
    
    top_10_df = sorted_df.head(10)
    
    fig = go.Figure(go.Bar(
        y=top_10_df['location'][::-1],
        x=top_10_df['new_cases_per_month'][::-1],
        orientation='h',
        marker_color='skyblue',
        text=top_10_df['new_cases_per_month'][::-1].apply(lambda x: f"{x:,.0f}"),
        textposition='outside',
        insidetextanchor='middle',
    ))
    
    fig.update_layout(
        title="Top 10 Countries by New Positive Cases",
        autosize=True,
        xaxis_title="",
        yaxis_title="",
        height=400,
        margin=dict(l=0, r=0, t=100, b=0),
        bargap=0.2,
    )
    
    fig.update_xaxes(tickformat=",", showticklabels=False)
    
    fig.update_yaxes(tickmode='array', tickvals=top_10_df['location'][::-1], ticktext=top_10_df['location'][::-1])
    
    return fig


def histogram(quarterly):
    fig_histogram = px.bar(quarterly, x='quarter', y='new_cases', labels={'new_cases': 'New Cases (Thousands)'}, 
                        title="Quarterly Evolution of Positive Cases Globaly.", color_discrete_sequence=['skyblue'])
    fig_histogram.update_layout(yaxis_title='New Cases (Thousands)', yaxis=dict(tickformat=".0f"))

    quarterly['new_cases'] = quarterly['new_cases'] / 1000 # scale to thousands

    return fig_histogram


def main():
    st.set_page_config(layout="wide")
    st.title("COVID-19 Monthly New Cases World Map")

    # 1. Import Data
    covid_df, quarterly_df = load_data()

    # 2. Set up preliminary variables
    min_month = covid_df['month'].min().date().replace(day=1)
    max_month = covid_df['month'].max().date().replace(day=1)

    # 3. Show slider, the main component of our page
    selected_month = setup_slider(min_month, max_month)

    # 4. Create filetered DataFrame based on the month selected with the slider
    filtered_df = covid_df[covid_df['month'].dt.to_period('M') == pd.Period(selected_month, freq='M')]
    filtered_df['new_cases_per_month'] = filtered_df['new_cases'].fillna(0)
    filtered_df['cases_size'] = (filtered_df['new_cases_per_month'] / 200_000) * 20

    # 5. Show main map in the left column + Show bar plot in the right column
    col1, col2 = st.columns([2, 1])
    with col1:
        main_map(filtered_df, selected_month)
    with col2:
        bar_fig = bar_plot(filtered_df)
        st.plotly_chart(bar_fig, use_container_width=True, config={'displayModeBar': False, 'responsive': True})

        hist_fig = histogram(quarterly_df)
        st.plotly_chart(hist_fig)

    # 6. Show summary data at the end of the page
    summary_data(filtered_df, selected_month)


if __name__ == "__main__":
    main()