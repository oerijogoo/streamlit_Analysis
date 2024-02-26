import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as colors
from streamlit_extras.metric_cards import style_metric_cards

# Function to calculate summaries
def calculate_summaries(column):
    mean = column.mean()
    mode = column.mode().values
    max_value = column.max()
    min_value = column.min()
    std_dev = column.std()
    median = column.median()
    count = len(column)
    range_value = max_value - min_value
    return mean, mode, max_value, min_value, std_dev, median, count,range_value

# page layout
st.set_page_config(page_title="Colposcopy Analytics", page_icon="🌎", layout="wide")

# streamlit theme=none
theme_plotly = None

# sidebar logo
st.sidebar.image("data/ici.png")

# title
st.title("iThemba_Colposcopy_Analysis")

# load CSS Style
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Read the data from Excel file
df = pd.read_excel("colpo.xlsx")

# Sidebar filters for programs and locations
programs = df["program"].unique()
programs = ["Select All"] + list(programs)
selected_programs = st.sidebar.multiselect("Select Programs", programs, default="Select All", key="programs")

locations = df["location"].unique()
locations = ["Select All"] + list(locations)
selected_locations = st.sidebar.multiselect("Select Locations", locations, default="Select All", key="locations")

# Filter the data based on selected programs and locations
if "Select All" in selected_programs and "Select All" in selected_locations:
    filtered_df = df
elif "Select All" in selected_programs:
    filtered_df = df[df["location"].isin(selected_locations)]
elif "Select All" in selected_locations:
    filtered_df = df[df["program"].isin(selected_programs)]
else:
    filtered_df = df[(df["program"].isin(selected_programs)) & (df["location"].isin(selected_locations))]

# Calculate summaries for age column
age_column = filtered_df["age"]
mean_age, mode_age, max_age, min_age, std_dev_age, median_age, count_age, range_age = calculate_summaries(age_column)

# Display the summaries
st.subheader("Summary for Age")
st.write(f"<span style='color: blue;'>Mean:</span> {mean_age}", unsafe_allow_html=True)
st.write(f"<span style='color: blue;'>Mode:</span> {mode_age}", unsafe_allow_html=True)
st.write(f"<span style='color: blue;'>Max:</span> {max_age}", unsafe_allow_html=True)
st.write(f"<span style='color: blue;'>Min:</span> {min_age}", unsafe_allow_html=True)
st.write(f"<span style='color: blue;'>Range:</span> {range_age}", unsafe_allow_html=True)
st.write(f"<span style='color: blue;'>Standard Deviation:</span> {std_dev_age}", unsafe_allow_html=True)
st.write(f"<span style='color: blue;'>Median:</span> {median_age}", unsafe_allow_html=True)
st.write(f"<span style='color: blue;'>Count:</span> {count_age}", unsafe_allow_html=True)

# Display the filtered data
#st.subheader("Filtered Data")
#st.write(filtered_df)

# sidebar switche
st.sidebar.header("")
st.sidebar.subheader("Select Values")

# Get unique values for the program and location columns
program_values = df["program"].unique()
location_values = df["location"].unique()
hpv16_values = df["hpv16"].unique()
hpv18_values = df["hpv18"].unique()
hpvdna_values = df["hpvdna"].unique()
Via_Results_values = df["Via_Results"].unique()
Colposcopic_impression_values = df["Colposcopic_impression"].unique()
HIV_STATUS_values = df["HIV_STATUS"].unique()
age_values = df["age"].unique()

# Add "Select All" option to the program and location values
program_values = ["Select All"] + list(program_values)
location_values = ["Select All"] + list(location_values)
hpv16_values = ["Select All"] + list(hpv16_values)
hpv18_values = ["Select All"] + list(hpv18_values)
hpvdna_values = ["Select All"] + list(hpvdna_values)
Via_Results_values = ["Select All"] + list(Via_Results_values)
Colposcopic_impression_values = ["Select All"] + list(Colposcopic_impression_values)
HIV_STATUS_values = ["Select All"] + list(HIV_STATUS_values)
age_values = ["Select All"] + list(age_values)

# Multiselect to choose programs and locations
selected_programs = st.sidebar.multiselect("Select Programs", program_values, default=["Select All"])
selected_locations = st.sidebar.multiselect("Select Locations", location_values, default=["Select All"])
selected_hpv16 = st.sidebar.multiselect("Select HPV16", hpv16_values, default=["Select All"])
selected_hpv18 = st.sidebar.multiselect("Select HPV18", hpv16_values, default=["Select All"])
selected_hpvdna = st.sidebar.multiselect("Select HPVDA", hpv16_values, default=["Select All"])
selected_Via_Results = st.sidebar.multiselect("Select Via_Results", Via_Results_values, default=["Select All"])
selected_Colposcopic_impression = st.sidebar.multiselect("Select Colposcopic_impression", Colposcopic_impression_values, default=["Select All"])
selected_HIV_STATUS = st.sidebar.multiselect("Select HIV_STATUS", HIV_STATUS_values, default=["Select All"])
selected_age = st.sidebar.multiselect("Select Age", age_values, default=["Select All"])

# metrics


# Filter the data based on selected programs and locations
filtered_df = df.copy()

if "Select All" not in selected_programs:
    filtered_df = filtered_df[filtered_df["program"].isin(selected_programs)]

if "Select All" not in selected_locations:
    filtered_df = filtered_df[filtered_df["location"].isin(selected_locations)]

if "Select All" not in selected_hpv16:
    filtered_df = filtered_df[filtered_df["hpv16"].isin(selected_hpv16)]

if "Select All" not in selected_hpv18:
    filtered_df = filtered_df[filtered_df["hpv18"].isin(selected_hpv18)]

if "Select All" not in selected_hpvdna:
    filtered_df = filtered_df[filtered_df["hpvdna"].isin(selected_hpvdna)]

if "Select All" not in selected_Via_Results:
    filtered_df = filtered_df[filtered_df["Via_Results"].isin(selected_Via_Results)]

if "Select All" not in selected_Colposcopic_impression:
    filtered_df = filtered_df[filtered_df["Colposcopic_impression"].isin(selected_Colposcopic_impression)]

if "Select All" not in selected_HIV_STATUS:
    filtered_df = filtered_df[filtered_df["HIV_STATUS"].isin(selected_HIV_STATUS)]

if "Select All" not in selected_age:
    filtered_df = filtered_df[filtered_df["age"].isin(selected_age)]
if filtered_df.empty:
    st.write("No data available for the selected programs and locations.")
else:
    # Group the data by location and program and count the occurrences
    grouped_data = filtered_df.groupby(["location", "program", "hpv16", "hpv18", "hpvdna", "Via_Results", "Colposcopic_impression", "HIV_STATUS", "age"]).size().reset_index(name="count")

    # Get a list of unique programs
    unique_programs = grouped_data["program"].unique()

    # Generate a list of colors for the unique programs
    colorscale = colors.qualitative.Plotly
    program_colors = [colorscale[i % len(colorscale)] for i in range(len(unique_programs))]

    # Create two columns for displaying charts side by side
    col1, col2 = st.columns(2)

    # Create the grouped bar chart
    fig_bar = go.Figure()

    for i, program in enumerate(unique_programs):
        program_data = grouped_data[grouped_data["program"] == program]
        fig_bar.add_trace(
            go.Bar(x=program_data["location"], y=program_data["count"], name=program, marker_color=program_colors[i]))

    fig_bar.update_layout(
        title="Program Count by Location",
        xaxis_title="Location",
        yaxis_title="Count",
        barmode="group"
    )

    # Display the grouped bar chart
    st.plotly_chart(fig_bar, use_container_width=True)

    # Create the grouped bar chart vgg
    fig_bar = go.Figure()

    for i, program in enumerate(unique_programs):
        program_data = grouped_data[grouped_data["program"] == program]
        fig_bar.add_trace(
            go.Bar(x=program_data["age"], y=program_data["count"], name=program, marker_color=program_colors[i]))

    fig_bar.update_layout(title="Program Count by Age",
                          xaxis_title="age",
                          yaxis_title="Count",
                          barmode="group")

    # Display the grouped bar chart
    st.plotly_chart(fig_bar, use_container_width=True)

    # Count the programs
    program_count = filtered_df["program"].value_counts()

    # Create the pie chart with the same colors as the bar chart for program count
    fig_pie_program = go.Figure(data=[go.Pie(labels=program_count.index, values=program_count.values, marker_colors=program_colors)])
    fig_pie_program.update_layout(title="Program Count")

    # Display the program pie chart
    col1.plotly_chart(fig_pie_program, use_container_width=True)

    # Count the HPV16
    hpv16_count = filtered_df["hpv16"].value_counts()

    # Create the pie chart for HPV16
    fig_pie_hpv16 = go.Figure(data=[go.Pie(labels=hpv16_count.index, values=hpv16_count.values)])
    fig_pie_hpv16.update_layout(title="HPV16 Count")

    # Display the HPV16 pie chart
    col2.plotly_chart(fig_pie_hpv16, use_container_width=True)

    # Count the HPV18
    hpv18_count = filtered_df["hpv18"].value_counts()

    # Create the pie chart for HPV18
    fig_pie_hpv18 = go.Figure(data=[go.Pie(labels=hpv18_count.index, values=hpv18_count.values)])
    fig_pie_hpv18.update_layout(title="HPV18 Count")

    # Display the HPV18 pie chart
    col1.plotly_chart(fig_pie_hpv18, use_container_width=True)

    # Count the HPV DNA
    hpvdna_count = filtered_df["hpvdna"].value_counts()

    # Create the pie chart for HPV DNA
    fig_pie_hpvdna = go.Figure(data=[go.Pie(labels=hpvdna_count.index, values=hpvdna_count.values)])
    fig_pie_hpvdna.update_layout(title="HPV DNA Count")

    # Display the HPV DNA pie chart
    col2.plotly_chart(fig_pie_hpvdna, use_container_width=True)

    # Count the Via Results
    via_results_count = filtered_df["Via_Results"].value_counts()

    # Create the pie chart for Via Results
    fig_pie_via_results = go.Figure(data=[go.Pie(labels=via_results_count.index, values=via_results_count.values)])
    fig_pie_via_results.update_layout(title="Via Results Count")

    # Display the Via Results pie chart
    col1.plotly_chart(fig_pie_via_results, use_container_width=True)

    # Count the occurrences of program and Colposcopic_impression combinations
    program_colposcopic_count = filtered_df["Colposcopic_impression"].value_counts()

    # Create the pie chart for program and Colposcopic_impression
    fig_pie_program_colposcopic = go.Figure(data=[go.Pie(labels= program_colposcopic_count.index, values=program_colposcopic_count.values)])
    fig_pie_program_colposcopic.update_layout(title="Colposcopic Impression count")


    # Display the program - Colposcopic_impression pie chart
    col2.plotly_chart(fig_pie_program_colposcopic, use_container_width=True)

    # Count the HIV_STATUS
    HIV_STATUS_count = filtered_df["HIV_STATUS"].value_counts()

    # Create the pie chart for HPV DNA
    fig_pie_HIV_STATUS = go.Figure(data=[go.Pie(labels=HIV_STATUS_count.index, values=HIV_STATUS_count.values)])
    fig_pie_HIV_STATUS.update_layout(title="HIV_STATUS Count")

    # Display the HIV_STATUS pie chart
    col1.plotly_chart(fig_pie_HIV_STATUS, use_container_width=True)



