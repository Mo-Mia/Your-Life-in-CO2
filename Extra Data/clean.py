import pandas as pd

# Load the data
data_daily = pd.read_csv('co2_daily_mlo.csv', comment='#', delim_whitespace=True, header=None)

# Rename the columns
data_daily.columns = ['Year', 'Month', 'Day', 'Decimal Date', 'CO2']

# Convert the year, month, and day into a date
data_daily['Date'] = pd.to_datetime(data_daily[['Year', 'Month', 'Day']])

# Set the date as the index
data_daily.set_index('Date', inplace=True)

# Drop the columns we don't need
data_daily.drop(['Year', 'Month', 'Day', 'Decimal Date'], axis=1, inplace=True)

# Load the data
data_monthly = pd.read_csv('co2_mm_mlo.csv', comment='#', delim_whitespace=True, header=None)

# Rename the columns
data_monthly.columns = ['Year', 'Month', 'Decimal Date', 'Average', 'Deseasonalized', 'NDays', 'SDev', 'Uncertainty']

# Convert the year and month into a date
data_monthly['Date'] = pd.to_datetime(data_monthly[['Year', 'Month']].assign(DAY=1))

# Set the date as the index
data_monthly.set_index('Date', inplace=True)

# Drop the columns we don't need
data_monthly.drop(['Year', 'Month', 'Decimal Date', 'Deseasonalized', 'NDays', 'SDev', 'Uncertainty'], axis=1, inplace=True)