import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta
from streamlit_extras.metric_cards import style_metric_cards

#page layout
st.set_page_config(page_title="Analytics", page_icon="🌎", layout="wide")

#sidebar logo
st.sidebar.image("data/ici.png")

#title
st.title("⏱ ONLINE ANALYTICS  DASHBOARD")

# load CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


#load dataset
df = pd.read_excel("foodsales.xlsx", sheet_name="FoodSales", engine='openpyxl')


#date filter
start_date=st.sidebar.date_input("Start Date",date.today()-timedelta(days=365*4))
end_date=st.sidebar.date_input(label="End Date")
#compare date
df2 = df[(df['OrderDate'] >= str(start_date)) & (df['OrderDate'] <= str(end_date))]

#sidebar switcher
st.sidebar.header("Please filter")
city=st.sidebar.multiselect(
    "Select City",
     options=df2["City"].unique(),
     default=df2["City"].unique(),
)
category=st.sidebar.multiselect(
    "Select Category",
     options=df2["Product"].unique(),
     default=df2["Product"].unique(),
)
region=st.sidebar.multiselect(
    "Select Region",
     options=df2["Region"].unique(),
     default=df2["Region"].unique(),
)

df_selection=df2.query(
    "City==@city & Product==@category & Region ==@region"
)

# metrics
st.subheader('Key Performance')

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="⏱ Total Items ", value=df_selection.Product.count(), delta="Number of Items in stock")
col2.metric(label="⏱ Sum of Product Total Price USD:", value=f"{df_selection.TotalPrice.sum():,.0f}",
            delta=df_selection.TotalPrice.median())
col3.metric(label="⏱ Maximum Price  USD:", value=f"{df_selection.TotalPrice.max():,.0f}", delta="High Price")
col4.metric(label="⏱ Minimum Price  USD:", value=f"{df_selection.TotalPrice.min():,.0f}", delta="Low Price")
style_metric_cards(background_color="#00588ECannot find reference 'metric_cards' in '__init__.py' ", border_left_color="#FF4B4B", border_color="#1f66bd",
                   box_shadow="#F71938")

coll1, coll2 = st.columns(2)
coll1.info("Business Metrics between[ " + str(start_date) + "] and [" + str(end_date) + "]")
