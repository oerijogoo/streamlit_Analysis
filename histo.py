import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import seaborn as sns
import numpy as np
# page layouts

st.set_page_config(page_title="ICI", page_icon="data/ici.png", layout="wide")


# streamlit themes=nonee
theme_plotly = None

# sidebar logo
st.sidebar.image("data/ici.png")

# title
st.title("🔬 Histology Data Analysis")

# load CSS Style
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# Load the Excel file
data = pd.read_excel('histo.xlsx')



# Get unique values from the 'site', 'gender', 'age', 'sample_type', 'findings' and 'days_gap' columns
site_options = ['All'] + list(data['site'].unique())
gender_options = ['All'] + list(data['gender'].unique())
age_options = ['All'] + list(data['age'].unique())
sample_type_options = ['All'] + list(data['sample_type'].unique())
findings_options = ['All'] + list(data['findings'].unique())
days_gap_options = ['All'] + list(data['days_gap'].unique())

# Add a sidebar for site, gender, age, sample type, and findings selection
selected_sites = st.sidebar.multiselect("Select Site", site_options, default=['All'])
selected_gender = st.sidebar.multiselect("Select Gender", gender_options, default=['All'], key="gender_select")
selected_age = st.sidebar.multiselect("Select Age", age_options, default=['All'], key="age_select")
selected_sample_type = st.sidebar.multiselect("Select Sample Type", sample_type_options, default=['All'], key="sample_type_select")
selected_findings = st.sidebar.multiselect("Select Findings", findings_options, default=['All'], key="findings_select")
selected_days_gap = st.sidebar.multiselect("Select days_gap", days_gap_options, default=['All'], key="days_gap_select")
# Filter the data based on the selected sites, gender, age, sample type, and findings days gaps
if 'All' in selected_sites:
    filtered_data = data
else:
    filtered_data = data[data['site'].isin(selected_sites)]

if 'All' in selected_gender:
    selected_gender = gender_options[1:]

if 'All' in selected_age:
    selected_age = age_options[1:]

if 'All' in selected_sample_type:
    selected_sample_type = sample_type_options[1:]

if 'All' in selected_findings:
    selected_findings = findings_options[1:]

if 'All' in selected_days_gap:
    selected_days_gap = days_gap_options[1:]

filtered_data = filtered_data[filtered_data['gender'].isin(selected_gender)]
filtered_data = filtered_data[filtered_data['age'].isin(selected_age)]
filtered_data = filtered_data[filtered_data['sample_type'].isin(selected_sample_type)]
filtered_data = filtered_data[filtered_data['findings'].isin(selected_findings)]
filtered_data = filtered_data[filtered_data['days_gap'].isin(selected_days_gap)]

site_count = filtered_data['site'].value_counts()
gender_count = filtered_data['gender'].value_counts()
age_count = filtered_data.groupby(['site', 'gender', 'age']).size().unstack(fill_value=0)
sample_type_count = filtered_data['sample_type'].value_counts()
findings_count = filtered_data['findings'].value_counts()
days_gap_count = filtered_data.groupby(['site', 'gender', 'days_gap']).size().unstack(fill_value=0)

# Create the pie chart for site count with site colors
fig_pie_site = go.Figure(data=[go.Pie(labels=site_count.index, values=site_count.values)])
fig_pie_site.update_traces(marker=dict(colors=['rgb(255, 165, 0)', 'rgb(165, 42, 42)']))
fig_pie_site.update_layout(
    title="SITES",
)

# Create the pie chart for gender count with gender colors
fig_pie_gender = go.Figure(data=[go.Pie(labels=gender_count.index, values=gender_count.values)])
fig_pie_gender.update_traces(marker=dict(colors=['rgb(0, 128, 0)', 'rgb(0, 0, 255)']))
fig_pie_gender.update_layout(
    title="Gender",
)

# Create the grouped bar chart for age frequency with different colors
fig_bar_age = go.Figure()

# Assign the colors for sites and genders
site_colors = ['rgb(255, 165, 0)', 'rgb(165, 42, 42)']
gender_colors = ['rgb(0, 128, 0)', 'rgb(0, 0, 255)']
bar_colors = ['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)', 'rgb(255, 255, 0)']

for site in site_count.index:
    for gender in gender_count.index:
        if (site, gender) in age_count.index:
            fig_bar_age.add_trace(go.Bar(
                x=age_count.columns,
                y=age_count.loc[(site, gender)],
                name=f"{site} - {gender}",
                marker_color=site_colors[0] if site == 'Site 1' else site_colors[1],
                legendgroup=f"{site} - {gender}",
            ))

# Update the marker colors for each bar in the grouped bar chart
for i, trace in enumerate(fig_bar_age.data):
    trace.marker.color = bar_colors[i % len(bar_colors)]

fig_bar_age.update_layout(
    title="Age Frequency by Site and Gender",
    xaxis_title="Age",
    yaxis_title="Frequency"
)

# Create the pie chart for sample type count with sample type colors
fig_pie_sample_type = go.Figure(data=[go.Pie(labels=sample_type_count.index, values=sample_type_count.values)])
fig_pie_sample_type.update_traces(marker=dict(colors=['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)']))
fig_pie_sample_type.update_layout(
    title="SAMPLE TYPE",
)

# Create the pie chart for findings count
fig_pie_findings = go.Figure(data=[go.Pie(labels=findings_count.index, values=findings_count.values)])
fig_pie_findings.update_layout(
    title="FINDINGS",
)

# Create the grouped bar chart for days_gap frequency with different colors
fig_bar_days_gap = go.Figure()

# Get the number of unique combinations of sites and genders
num_groups = len(days_gap_count.index)

# Generate a color palette with the desired number of colors
days_gap_colors = sns.color_palette("husl", num_groups).as_hex()

for i, (site, gender) in enumerate(days_gap_count.index):
    fig_bar_days_gap.add_trace(go.Bar(
        x=days_gap_count.columns,
        y=days_gap_count.loc[(site, gender)],
        name=f"{site} - {gender}",
        marker_color=days_gap_colors[i],
        legendgroup=f"{site} - {gender}",
    ))

fig_bar_days_gap.update_layout(
    title="Day_Gap Frequency by Site and Gender",
    xaxis_title="Day_Gap",
    yaxis_title="Frequency"
)
coll1, coll2 = st.columns(2)
coll3, coll6 = st.columns(2)


# Display the pie chart for site count
coll1.plotly_chart(fig_pie_site, use_container_width=True)

# Display the pie chart for gender counts
coll2.plotly_chart(fig_pie_gender, use_container_width=True)


# Display the pie chart for sample type count
coll3.plotly_chart(fig_pie_sample_type, use_container_width=True)

# Display the pie chart for findings count
coll6.plotly_chart(fig_pie_findings, use_container_width=True)

# Display the grouped bar chart for age frequenciencies
st.plotly_chart(fig_bar_age, use_container_width=True)
# Display the pie chart for findings counts
st.plotly_chart(fig_bar_days_gap, use_container_width=True)

# Get the columns chosen in the charts
selected_columns = ['site', 'gender', 'age', 'sample_type', 'findings', 'days_gap']

# Filter the data based on the selected columns
filtered_table_data = filtered_data[selected_columns]

# Create three columns for the tables
col1, col2, col3 = st.columns([3, 1, 1])

# Display the filtered_table_data DataFrame as a table
with col1:
    st.write("Filtered Data:")
    st.dataframe(filtered_table_data, width=800, height=400)

# Compute and display the grand total
grand_total = filtered_table_data.shape[0]
st.write("Grand Total:", grand_total)

# Calculate statistics for the 'age' column
age_data = filtered_table_data['age']
age_count = len(age_data)
age_mean = round(sum(age_data) / age_count, 2)
age_std = round(np.sqrt(sum((x - age_mean) ** 2 for x in age_data) / age_count), 2)
age_min = int(age_data.min())
age_q1 = int(np.percentile(age_data, 25))
age_median = int(np.percentile(age_data, 50))
age_q3 = int(np.percentile(age_data, 75))
age_max = int(age_data.max())
age_range = age_max - age_min
age_mode = int(age_data.mode().values[0])

# Calculate statistics for the 'days_gap' column
days_gap_data = filtered_table_data['days_gap']
days_gap_count = len(days_gap_data)
days_gap_mean = round(sum(days_gap_data) / days_gap_count, 2)
days_gap_std = round(np.sqrt(sum((x - days_gap_mean) ** 2 for x in days_gap_data) / days_gap_count), 2)
days_gap_min = int(days_gap_data.min())
days_gap_q1 = int(np.percentile(days_gap_data, 25))
days_gap_median = int(np.percentile(days_gap_data, 50))
days_gap_q3 = int(np.percentile(days_gap_data, 75))
days_gap_max = int(days_gap_data.max())
days_gap_range = days_gap_max - days_gap_min
days_gap_mode = int(days_gap_data.mode().values[0])

# Create a DataFrame for age statistics
age_stats_formatted = pd.DataFrame({
    'count': [age_count],
    'mean': [age_mean],
    'std': [age_std],
    'min': [age_min],
    '25%': [age_q1],
    '50%': [age_median],
    '75%': [age_q3],
    'max': [age_max],
    'range': [age_range],
    'mode': [age_mode]
})

# Create a DataFrame for days_gap statistics
days_gap_stats_formatted = pd.DataFrame({
    'count': [days_gap_count],
    'mean': [days_gap_mean],
    'std': [days_gap_std],
    'min': [days_gap_min],
    '25%': [days_gap_q1],
    '50%': [days_gap_median],
    '75%': [days_gap_q3],
    'max': [days_gap_max],
    'range': [days_gap_range],
    'mode': [days_gap_mode]
})

# Function to remove decimal points and trailing zeros from integers
def remove_decimal_zeros(value):
    if isinstance(value, int):
        return str(value)
    return str(value).rstrip('0').rstrip('.')

# Format values in the statistics DataFrames
age_stats_formatted = age_stats_formatted.applymap(remove_decimal_zeros)
days_gap_stats_formatted = days_gap_stats_formatted.applymap(remove_decimal_zeros)

# Display the statistics tables
with col2:
    st.write("Statistics for Age:")
    st.table(age_stats_formatted.transpose())

with col3:
    st.write("Statistics for Days Gap:")
    st.table(days_gap_stats_formatted.transpose())
# Get the current
hide_st_style = """"
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
current_year = datetime.now().year
footer_text = f"<p style='text-align: center;'>© {current_year} ICI</p>"
st.markdown(footer_text, unsafe_allow_html=True)
st.markdown(hide_st_style, unsafe_allow_html=True)
