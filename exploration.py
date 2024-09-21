import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
covid_df = pd.read_csv("owid-covid-data.csv")
small_df = covid_df[["location", "date", "new_cases"]]

# Convert date to datetime
small_df['date'] = pd.to_datetime(small_df['date'])

# Group by location and date, then sum new cases
grouped_df = small_df.groupby(['location', 'date'])['new_cases'].sum().reset_index()

# Create the plot
plt.figure(figsize=(12, 6))

# Plot data for each location
for location in grouped_df['location'].unique():
    location_data = grouped_df[grouped_df['location'] == location]
    plt.plot(location_data['date'], location_data['new_cases'], label=location)

plt.title('New COVID-19 Cases by Location')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save the figure
plt.savefig('covid_cases_plot.png')

print("Plot saved as 'covid_cases_plot.png'")

# Display the first few rows of the grouped dataframe
print(grouped_df.head())