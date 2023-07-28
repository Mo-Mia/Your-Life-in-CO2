import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Set the title of the app
st.title("🌍 Your Life in CO2 🌍")

# Add the "Made by Mohem" text with a heart emoji
st.markdown(":heart: Made by Mohem")

st.write("""
This app provides you with information about the average carbon dioxide (CO2) concentration in the atmosphere in your birth year.
(*Credit to Sultan Uzan for the idea*)

Enter your birth date to explore historical CO2 concentration trends and understand how CO2 levels have changed over time since your birth year.
""")

# Load the cleaned data from the CSV file
with st.spinner('Loading data...'):
    data = pd.read_csv('cleaned_daily_in_situ_co2_mlo.csv', parse_dates=['Date'], index_col='Date')

# Clean the data
data['CO2_ppm'] = pd.to_numeric(data['CO2_ppm'], errors='coerce')
data = data.dropna(subset=['CO2_ppm'])

# Ask the user for their birth date
date_input = st.text_input("Enter your birth date (YYYY-MM-DD, YYYYMMDD, or YYMMDD)")

# Validate date input and convert to datetime
birth_date = None
if date_input:
    try:
        if len(date_input) == 8: # if date format is YYYYMMDD
            birth_date = datetime.strptime(date_input, "%Y%m%d")
        elif len(date_input) == 6: # if date format is YYMMDD
            birth_date = datetime.strptime(date_input, "%y%m%d")
        else: # if date format is YYYY-MM-DD
            birth_date = datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        st.error('Invalid date format. Please enter your birth date as YYYY-MM-DD, YYYYMMDD, or YYMMDD.')

# Make sure a birth date is submitted before displaying the data
if birth_date is not None:
    with st.spinner('Calculating...'):
        # Calculate the time remaining until the next birthday
        today = datetime.today()
        next_birthday = birth_date + relativedelta(years=today.year - birth_date.year)
        if next_birthday < today:
            next_birthday += relativedelta(years=1)
        time_remaining = next_birthday - today

        # Display the confirmation step
        st.success(f"It's {time_remaining.days} days, {time_remaining.seconds // 3600} hours, "
                   f"{(time_remaining.seconds % 3600) // 60} minutes, and {time_remaining.seconds % 60} seconds until your next birthday!")

        # Filter the data to include only the rows from the user's birth year
        birth_year_data = data[data.index.year == birth_date.year]

        # Calculate the latest average CO2 concentration
        latest_avg = data['CO2_ppm'].iloc[-1]

        # Display the average CO2 concentration in the user's birth year with colorful background and bigger text
        if not birth_year_data.empty:
            birth_year_avg = birth_year_data["CO2_ppm"].mean()
            st.markdown(f'<p style="font-size:28px;background-color:#991a1a;padding:10px;border-radius:10px;">'
                        f'📌 The average CO2 concentration in your birth year was <b>{birth_year_avg:.2f} ppm.</b>'
                        f'</p>', unsafe_allow_html=True)

            # Calculate the increase in CO2 concentration since the user's birth year with colorful background and bigger text
            increase = latest_avg - birth_year_avg
            st.markdown(f'<p style="font-size:16px;background-color:#732121;padding:10px;border-radius:10px;">'
                        f'📈 The CO2 concentration has increased by {increase:.2f} ppm since you were born.'
                        f'</p>', unsafe_allow_html=True)

            # If user has toco, display the equivalent tonnes of CO2 offset
            # TODO: Add toco balance feature here

            # Display the latest CO2 concentration with rounded corners
            latest_date = data.index[-1].strftime('%B %Y')
            st.markdown(f'<p style="font-size:16px;">📊 The latest recorded CO2 concentration ({latest_date}) is {latest_avg:.2f} ppm.</p>', unsafe_allow_html=True)

            # Calculate when the safe level was passed
            safe_level_passed = data[data['CO2_ppm'] > 350].index[0]
            st.markdown(f'🚦 The safe level of 350 ppm was passed in {safe_level_passed.year}.')

            # Calculate by how much we're exceeding the safe level
            exceeding = latest_avg - 350
            st.markdown(f'🔥 We are currently exceeding the safe level by {exceeding:.2f} ppm.')

            # Plot the CO2 concentration over time using Plotly with interactive description
            st.header('🌡️ CO2 Concentration Over Time 🌡️')
            st.markdown("This interactive plot shows the CO2 concentration over time. Use the zoom and pan tools to explore the data in detail.")
            fig = px.line(data, y='CO2_ppm', labels={'x':'Year', 'y':'CO2 concentration (ppm)'})
            fig.add_vline(x=birth_date, line_color='red', line_dash="dash", opacity=0.7)
            fig.add_hline(y=350, line_color='green', line_dash="dash", opacity=0.7)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)

# Credits section
st.header('🙏 Credits and Acknowledgements 🙏')
st.write("""
- **Data**: The CO2 concentration data is provided by the Global Monitoring Laboratory - Earth System Research Laboratories. The data from March 1958 through April 1974 have been obtained by C. David Keeling of the Scripps Institution of Oceanography (SIO) and were obtained from the Scripps website (scrippsco2.ucsd.edu).
- **App Developer**: This app was developed by Mo and the team at Project Mohem.
- **Idea Credit**: This app was inspired by a concept from Sultan Uzan.
""")