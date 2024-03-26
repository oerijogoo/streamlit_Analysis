from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import io

st.set_page_config(page_title="ICI", page_icon="data/ici.png", layout="wide")


# streamlit themes=none
theme_plotly = None


# title
st.header("🔬 Histology Data Analysis")


# load CSS Style
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# Load the Excel file
data = pd.read_excel('histof.xlsx')


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
selected_sample_type = st.sidebar.multiselect("Select Sample Type", sample_type_options, default=['All'], key="sample_type_select")
selected_findings = st.sidebar.multiselect("Select Findings", findings_options, default=['All'], key="findings_select")

# Filter the data based on the selected sites, gender, age, sample type, and findings days gaps
if 'All' in selected_sites:
    filtered_data = data
else:
    filtered_data = data[data['site'].isin(selected_sites)]

if 'All' in selected_gender:
    selected_gender = gender_options[1:]


if 'All' in selected_sample_type:
    selected_sample_type = sample_type_options[1:]

if 'All' in selected_findings:
    selected_findings = findings_options[1:]


filtered_data = filtered_data[filtered_data['gender'].isin(selected_gender)]
filtered_data = filtered_data[filtered_data['sample_type'].isin(selected_sample_type)]
filtered_data = filtered_data[filtered_data['findings'].isin(selected_findings)]
print(filtered_data['age'].dtypes)
site_count = filtered_data['site'].value_counts()
gender_count = filtered_data['gender'].value_counts()
age_count = filtered_data.groupby(['site', 'gender', 'age']).size().unstack(fill_value=0)
sample_type_count = filtered_data['sample_type'].value_counts()
findings_count = filtered_data['findings'].value_counts()
days_gap_count = filtered_data.groupby(['site', 'gender', 'days_gap']).size().unstack(fill_value=0)

#for initialization
# Get the columns chosen in the charts
selected_columns = ['id', 'site', 'gender', 'age', 'sample_type', 'findings', 'days_gap']
# Filter the data based on the selected columns
filtered_table_data = filtered_data[selected_columns]
# Calculate statistics for the 'days_gap' column
days_gap_data = filtered_table_data['days_gap']
days_gap_count = len(days_gap_data)

# Define the range
range_min = 0
range_max = 280


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
# Set the desired step size for the day intervals
day_interval_step = st.sidebar.slider('Day Interval Step', min_value=3, max_value=20, value=10)
# Check if the slider value is less than 3
if day_interval_step < 3:
    st.error("The selected day interval step must be at least 3.")
else:
    # Generate day intervals based on the step size, starting from 5
    day_min = 0  # Start from 0
    day_max = 500  # Maximum day interval
    day_intervals = list(range(day_min, day_max + 1, day_interval_step))

    # Adjust the last interval to include day up to 20
    if day_intervals[-1] != day_max:
        day_intervals.append(day_max)
# Generate day intervals based on the step size, starting from 5
day_min = 0  # Start from 0
day_max = 500  # Maximum day interval
day_intervals = list(range(day_min, day_max + 1, day_interval_step))

# Adjust the last interval to include day up to 20
if day_intervals[-1] != day_max:
    day_intervals.append(day_max)

# Calculate day count by site and gender
day_count = filtered_data.groupby(['site', 'gender'])['days_gap'].apply(lambda x: np.histogram(x, bins=day_intervals)[0]).unstack(fill_value=0)

# Create the stacked bar chart for day frequency
fig_bar_day = go.Figure()

# Assign the colors for sites and genders
site_colors = ['rgb(255, 0, 0)', 'rgb(0, 128, 0)', 'rgb(0, 0, 255)', 'rgb(255, 255, 0)', 'rgb(128, 0, 128)']  # Update site colors
gender_colors = {'MALE': 'rgb(0, 0, 255)', 'FEMALE': 'rgb(255, 165, 0)', 'OTHER': 'rgb(255, 0, 255)'}  # Update gender colors
bar_colors = ['rgb(255, 165, 0)', 'rgb(165, 42, 42)', 'rgb(0, 128, 128)', 'rgb(128, 0, 128)', 'rgb(0, 255, 255)', 'rgb(255, 0, 255)']  # Update bar colors


# Initialize lists to store x and y values
x_values = []
y_totals = []

# Add the day values as stacked bars on the chart
for site in day_count.index:
    site_data = day_count.loc[site]
    # Update x_values within the loop
    x_values = [f"{interval}-{interval + day_interval_step - 1}" for interval in day_intervals[:-1]]
    x_values.append(f"{day_intervals[-2] + 1}-{day_max}")  # Adjust the last interval to include the maximum day
    for i, gender in enumerate(site_data.index):
        if isinstance(site_data[gender], int):
            y_values = [site_data[gender]] * len(day_intervals[:-1])
        else:
            y_values = site_data[gender].tolist()
        fig_bar_day.add_trace(go.Bar(
            x=x_values,
            y=y_values,
            name=f"{site} - {gender}",
            marker_color=gender_colors[gender],  # Use gender as a key to access color
            legendgroup=f"{site} - {gender}",
            offsetgroup=f"{site} - {gender}"
        ))
        # Calculate total for each group
        if not y_totals:
            y_totals = y_values.copy()
        else:
            for j, y_val in enumerate(y_values):
                y_totals[j] += y_val

# Update the marker colors for each bar in the stacked bar chart
for i, trace in enumerate(fig_bar_day.data):
    trace.marker.color = bar_colors[i % len(bar_colors)]

# Add total annotations to the chart
for i, total in enumerate(y_totals):
    fig_bar_day.add_annotation(
        x=i,
        y=total,
        text=str(total),
        showarrow=False,
        yshift=10,  # Adjust vertical position
        font=dict(size=10)  # Adjust font size
    )

fig_bar_day.update_layout(
    title="Stacked Grouped Day Frequency by Site and Gender",
    xaxis_title="Day Group interval",
    yaxis_title="Frequency",
    barmode='stack',  # Change the barmode to 'stack' for stacked bars
    xaxis=dict(
        tickmode='linear',
        tickvals=list(range(len(x_values))),
        ticktext=x_values
    )
)

# Define initial width and height for the charts
initial_chart_width = 100
initial_chart_height = 50


# Define the layout for the first row with custom column sizes
col1, col2 = st.columns([2, 2])  # Adjust the width ratios as needed

# Display the pie chart for site count in the first row
show_pie_site = st.sidebar.checkbox("Show Pie Chart for Site Count", value=False)
if show_pie_site:
    col1.plotly_chart(fig_pie_site, use_container_width=True)

# Display the pie chart for gender counts in the first row
show_pie_gender = st.sidebar.checkbox("Show Pie Chart for Gender Counts", value=False)
if show_pie_gender:
    col2.plotly_chart(fig_pie_gender, use_container_width=True)

# Define the layout for the second row with custom column sizes
col3, col4 = st.columns([2, 2])  # Adjust the width ratios as needed

# Display the pie chart for sample type count in the second row
show_pie_sample_type = st.sidebar.checkbox("Show Pie Chart for Sample Type Count", value=False)
if show_pie_sample_type:
    col3.plotly_chart(fig_pie_sample_type, use_container_width=True)

# Display the pie chart for findings count in the second row
show_pie_findings = st.sidebar.checkbox("Show Pie Chart for Findings Count", value=False)
if show_pie_findings:
    col4.plotly_chart(fig_pie_findings, use_container_width=True)

# Display the grouped bar chart for day frequency
show_bar_day = st.sidebar.checkbox("Show Grouped Bar Chart for Day Intervals", value=False)
if show_bar_day:
    st.plotly_chart(fig_bar_day)


# Calculate the histogram of days_gap values
hist, _ = np.histogram(filtered_data['days_gap'], bins=day_intervals)

# Find the index of the interval with the highest frequency
modal_interval_index = np.argmax(hist)

# Retrieve the start and end values of the modal class
modal_class_start = day_intervals[modal_interval_index]
modal_class_end = day_intervals[modal_interval_index + 1]

# Calculate the range between the highest and lowest class intervals
range_between_classes = day_intervals[-1] - day_intervals[0]

# Calculate the range in class-based analysis
class_ranges = []
for i in range(len(day_intervals) - 1):
    class_range = day_intervals[i + 1] - day_intervals[i]
    class_ranges.append(class_range)

# Calculate the middle class
median_interval_index = len(day_intervals) // 2
middle_class_start = day_intervals[median_interval_index - 1]
middle_class_end = day_intervals[median_interval_index]
middle_class = (middle_class_start + middle_class_end) / 2

# Calculate the range between the highest and lowest class intervals
highest_class_start = day_intervals[-2]
highest_class_end = day_intervals[-1]
lowest_class_start = day_intervals[0]
lowest_class_end = day_intervals[1]
range_between_classes = highest_class_end - lowest_class_start


# Calculate the class intervals based on the selected step
class_interval_step = day_interval_step
lower_bound_10 = int(0.1 * range_max)
upper_bound_10 = int(0.1 * range_max) + day_interval_step - 1
lower_bound_25 = int(0.25 * range_max)
upper_bound_25 = int(0.25 * range_max) + day_interval_step - 1
lower_bound_50 = int(0.5 * range_max)
upper_bound_50 = int(0.5 * range_max) + day_interval_step - 1
lower_bound_75 = int(0.75 * range_max)
upper_bound_75 = int(0.75 * range_max) + class_interval_step
lower_bound_90 = int(0.9 * range_max)
upper_bound_90 = int(0.9 * range_max) + class_interval_step - 1


# Get the columns chosen in the charts
selected_columns = ['id', 'site', 'gender', 'age', 'sample_type', 'findings', 'days_gap']

# Filter the data based on the selected columns
filtered_table_data = filtered_data[selected_columns]
# Construct the table title based on selected values
table_title_parts = []

if selected_sites:
    table_title_parts.append(f"SITES[{', '.join(selected_sites)}]_")
if selected_gender:
    table_title_parts.append(f"GENDER[{', '.join(selected_gender)}]_")
if selected_sample_type:
    table_title_parts.append(f"SAMPLE TYPE[{', '.join(selected_sample_type)}]_")

# Filter out 'nan' from selected findings
selected_findings_filtered = [finding for finding in selected_findings if str(finding) != 'nan']

# Append findings to table title parts
table_title_parts.append(f"FINDINGS[{', '.join(selected_findings_filtered)}]")
table_title = "Data for\n" + "\n".join(table_title_parts)

# Prepare data for download
export_df = filtered_data[selected_columns]

# Prepare the Excel contents
excel_content = io.BytesIO()
with pd.ExcelWriter(excel_content, engine='xlsxwriter') as writer:
    workbook = writer.book
    worksheet = workbook.add_worksheet('Sheet1')

    # Merge cells for the titles
    title_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 10,
        'text_wrap': True
    })
    worksheet.merge_range('A1:G5', table_title, title_format)

    # Write the column headers
    header_format = workbook.add_format({
        'bold': True
    })
    for col_idx, header in enumerate(export_df.columns):
        worksheet.write(5, col_idx, header, header_format)

    # Write the data
    for row_idx, row in enumerate(export_df.itertuples(), start=6):
        for col_idx, value in enumerate(row[1:], start=0):
            worksheet.write(row_idx, col_idx, str(value))  # Convert value to string


# Download the data with title included
if st.button("Download Data"):
    # Download data as Excel
    st.download_button(
        label="Download Excel",
        data=excel_content.getvalue(),
        file_name='filtered_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )



# Display the class intervals as percentiles using Streamlit
st.header("Class Intervals (Percentiles)")
st.write("10%: {} - {}".format(lower_bound_10, upper_bound_10))
st.write("25%: {} - {}".format(lower_bound_25, upper_bound_25))
st.write("50%: {} - {}".format(lower_bound_50, upper_bound_50))
st.write("75%: {} - {}".format(lower_bound_75, upper_bound_75))
st.write("90%: {} - {}".format(lower_bound_90, upper_bound_90))

# Display the table title
st.write(table_title)
# export excel file
st.dataframe(export_df, width=800, height=600)
# Compute and display the grand total
grand_total = filtered_data.shape[0]
st.write("TOTAL:", grand_total)




# Display the calculated statistics
st.subheader("Additional Statistics")
st.write("Range Between Highest and Lowest Class Intervals:", range_between_classes)
st.write("Modal Class:", modal_class_start, "-", modal_class_end - 1)
st.write("Middle Class: {} - {}".format(lower_bound_50, upper_bound_50))



# style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
current_year = datetime.now().year
footer_text = f"<p style='text-align: center;'>© {current_year} ICI</p>"
st.markdown(footer_text, unsafe_allow_html=True)
st.markdown(hide_st_style, unsafe_allow_html=True)
