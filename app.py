import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Set the title of the app
st.title("🌍 Your Life in CO2 🌍")
st.write("""
This app provides you with information about the average carbon dioxide (CO2) concentration in the atmosphere in your birth year. (*Credit to Sultan Uzan for the idea*)
Enter your birth date to explore historical CO2 concentration trends and understand how CO2 levels have changed over time since your birth year.
""")

# Load the cleaned data from the CSV file
with st.spinner('Loading data...'):
    data = pd.read_csv('cleaned_daily_in_situ_co2_mlo.csv', parse_dates=['Date'], index_col='Date')

# Add a sidebar for toco
st.sidebar.header("Do you have toco?")
has_toco = st.sidebar.radio("", ('Yes', 'No'))

toco_balance = None
if has_toco == 'Yes':
    toco_balance = st.sidebar.number_input('Enter your toco balance')

# Ask the user for their birth date
date_input = st.text_input("Enter your birth date (YYYY-MM-DD or YYYYMMDD)")

# Validate date input and convert to datetime
try:
    if len(date_input) == 8: # if date format is YYYYMMDD
        birth_date = datetime.strptime(date_input, "%Y%m%d")
    else: # if date format is YYYY-MM-DD
        birth_date = datetime.strptime(date_input, "%Y-%m-%d")
except ValueError:
    birth_date = None

# Make sure a birth date is submitted before displaying the data
if birth_date is not None:
    with st.spinner('Calculating...'):
        # Filter the data to include only the rows from the user's birth year
        birth_year_data = data[data.index.year == birth_date.year]

        # Calculate the latest average CO2 concentration
        latest_avg = data['CO2_ppm'].iloc[-1]

        # Display the average CO2 concentration in the user's birth year
        if not birth_year_data.empty:
            birth_year_avg = birth_year_data["CO2_ppm"].mean()
            st.markdown(f'**📌 The average CO2 concentration in your birth year was {birth_year_avg:.2f} ppm.**', unsafe_allow_html=True)

            # Calculate the increase in CO2 concentration since the user's birth year
            increase = latest_avg - birth_year_avg
            st.markdown(f'**📈 The CO2 concentration has increased by {increase:.2f} ppm since you were born.**', unsafe_allow_html=True)

            # Plot the CO2 concentration over time using Plotly
            st.header('🌡️ CO2 Concentration Over Time 🌡️')
            fig = px.line(data, y='CO2_ppm', labels={'x':'Year', 'y':'CO2 concentration (ppm)'})
            fig.add_vline(x=birth_date, line_color='red', line_dash="dash", opacity=0.7)
            fig.add_hline(y=350, line_color='green', line_dash="dash", opacity=0.7)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

            # If user has toco, display the equivalent tonnes of CO2 offset
            if toco_balance is not None:
                st.sidebar.markdown(f'**💚 Your toco balance of {toco_balance} is equivalent to offsetting {toco_balance} tonnes of CO2!**', unsafe_allow_html=True)
        else:
            st.error('No data available for your birth year.')

        # Display the latest CO2 concentration
        latest_date = data.index[-1].strftime('%B %Y')
        st.markdown(f'**📊 The latest recorded CO2 concentration ({latest_date}) is {latest_avg:.2f} ppm.**', unsafe_allow_html=True)

        # Calculate when the safe level was passed
        safe_level_passed = data[data['CO2_ppm'] > 350].index[0]
        st.markdown(f'**🚦 The safe level of 350 ppm was passed in {safe_level_passed.year}.**', unsafe_allow_html=True)

        # Calculate by how much we're exceeding the safe level
        exceeding = latest_avg - 350
        st.markdown(f'**🔥 We are currently exceeding the safe level by {exceeding:.2f} ppm.**', unsafe_allow_html=True)

# Credits section
st.header('🙏 Credits and Acknowledgements 🙏')
st.write("""
- **Data**: The CO2 concentration data is provided by the Global Monitoring Laboratory - Earth System Research Laboratories. The data from March 1958 through April 1974 have been obtained by C. David Keeling of the Scripps Institution of Oceanography (SIO) and were obtained from the Scripps website (scrippsco2.ucsd.edu).
- **App Developer**: This app was developed by Mo and the team at Project Mohem.
- **Idea Credit**: This app was inspired by a concept from Sultan Uzan.
""")
