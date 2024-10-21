import streamlit as st 
import pandas as pd 
import plotly.express as px
import requests

st.set_page_config(layout="wide")


polling_average = requests.get('https://projects.fivethirtyeight.com/polls/president-general/2024/national/polling-average.json').json()
df_polling_average = pd.DataFrame(polling_average)


fig = px.line(df_polling_average, x ='date', y='pct_estimate', color='candidate', error_x='hi', title='EUA 2024 - Presidencial Polls' )
fig.update_layout(hovermode="x")
fig.show()

