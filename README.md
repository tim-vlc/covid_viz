# COVID-19 Global Data Dashboard
This Streamlit app visualizes global COVID-19 data, allowing users to explore new cases per quarter/month either globally or by selecting a specific country.
The visualization was heavily inspired from a [TableauⒸ visualization on the subject](https://www.tableau.com/learn/articles/free-public-data-sets). Furthermore, the data was found on [this github repository](https://github.com/CSSEGISandData/COVID-19) by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University.

## Features
- A Histogram allows to select a country from a dropdown to visualize the number of new COVID-19 cases per quarter.
- The World Map option displays global new cases per month, adjusted with the slider.
- The Bar Plot shows the top 10 countries per new cases in the selected month.
- A Summary Menu is found at the bottom of the visualization.

## Installation
1. Clone the repository in a working directory on your machine: `git clone https://github.com/tim-vlc/covid_viz`,
2. Then, build the docker image: `cd covid_viz | docker build -t covid_viz .`,
3. Now, run the container using the following command: `docker run -p 8501:8501 covid_viz`,
4. Head to the following page on your browser: `http://localhost:8501`,
5. And voilà! All done, you can play around with the viz.
