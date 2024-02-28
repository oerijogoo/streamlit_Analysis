import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Load the Excel file
data = pd.read_excel('histo.xlsx')

# Set the title and top bar
st.title("Histo Analysis")
st.markdown("---")


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
selected_days_gap = st.sidebar.multiselect("Select days_gap", age_options, default=['All'], key="days_gap_select")
# Filter the data based on the selected sites, gender, age, sample type, and findings days gap
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

# Create the pie chart for gender count with gender colors
fig_pie_gender = go.Figure(data=[go.Pie(labels=gender_count.index, values=gender_count.values)])
fig_pie_gender.update_traces(marker=dict(colors=['rgb(0, 128, 0)', 'rgb(0, 0, 255)']))

# Create the grouped bar chart for age frequency with different colors
fig_bar_age = go.Figure()

# Assign the colors for sites and genders
site_colors = ['rgb(255, 165, 0)', 'rgb(165, 42, 42)']
gender_colors = ['rgb(0, 128, 0)', 'rgb(0, 0, 255)']
bar_colors = ['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)', 'rgb(255, 255, 0)']

for site in site_count.index:
    for gender in gender_count.index:
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

fig_bar_age.update_layout(title="Age Frequency by Site and Gender", barmode='group')

# Create the pie chart for sample type count with sample type colors
fig_pie_sample_type = go.Figure(data=[go.Pie(labels=sample_type_count.index, values=sample_type_count.values)])
fig_pie_sample_type.update_traces(marker=dict(colors=['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)']))

# Create the pie chart for findings count
fig_pie_findings = go.Figure(data=[go.Pie(labels=findings_count.index, values=findings_count.values)])

# Create the grouped bar chart for days_gap frequency with different colors
fig_bar_days_gap = go.Figure()

# Assign the colors for sites and genders
days_gap_colors = ['rgb(0, 128, 0)', 'rgb(0, 0, 255)']

for site in site_count.index:
    for gender in gender_count.index:
        fig_bar_days_gap.add_trace(go.Bar(
            x=days_gap_count.columns,
            y=days_gap_count.loc[(site, gender)],
            name=f"{site} - {gender}",
            marker_color=site_colors[0] if site == 'Site 1' else site_colors[1],
            legendgroup=f"{site} - {gender}",
        ))

# Update the marker colors for each bar in the grouped bar chart
for i, trace in enumerate(fig_bar_days_gap.data):
    trace.marker.color = bar_colors[i % len(bar_colors)]

fig_bar_days_gap.update_layout(title="days_gap Frequency by Site and Gender", barmode='group')


# Display the pie chart for site count
st.plotly_chart(fig_pie_site, use_container_width=True)

# Display the pie chart for gender count
st.plotly_chart(fig_pie_gender, use_container_width=True)

# Display the grouped bar chart for age frequency
st.plotly_chart(fig_bar_age, use_container_width=True)

# Display the pie chart for sample type count
st.plotly_chart(fig_pie_sample_type, use_container_width=True)

# Display the pie chart for findings count
st.plotly_chart(fig_pie_findings, use_container_width=True)
# Display the pie chart for findings counts
st.plotly_chart(fig_bar_days_gap, use_container_width=True)





# Get the current yearss
current_year = datetime.now().year
footer_text = f"<p style='text-align: center;'>© {current_year} ICI</p>"
st.markdown(footer_text, unsafe_allow_html=True)
