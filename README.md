# COVID-19 Global Data Dashboard
This Streamlit app visualizes global COVID-19 data, allowing users to explore new cases per quarter/month either globally or by selecting a specific country.
The visualization was heavily inspired from a [TableauⒸ visualization on the subject](https://www.tableau.com/learn/articles/free-public-data-sets). Furthermore, the data was found on [this github repository](https://github.com/CSSEGISandData/COVID-19) by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University.

## Features
- A Histogram allows to select a country from a dropdown to visualize the number of new COVID-19 cases per quarter.
- The World Map option displays global new cases per month, adjusted with the slider.
- The Bar Plot shows the top 10 countries per new cases in the selected month.
- A Summary Menu is found at the bottom of the visualization.

## Installation
**Warning** The commands need to be run on a terminal on your machine. If you do not have `Docker` or `Git` installed, please follow the following guides for [Docker](https://docs.docker.com/engine/install/) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

1. Clone the repository in a working directory on your machine: `git clone https://github.com/tim-vlc/covid_viz.git`,
2. Then, build the docker image: `cd covid_viz && docker build -t covid_viz .`,
3. Now, run the container using the following command: `docker run -p 8501:8501 covid_viz`,
4. Head to the following page on your browser: [`http://localhost:8501`](http://localhost:8501),
5. And voilà! All done, you can play around with the viz.
