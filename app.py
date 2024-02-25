import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as colors

# Set page configuration
st.set_page_config(page_title="Program Analysis")

# Read the data from Excel file
df = pd.read_excel("colpo.xlsx")

# Sidebar
st.sidebar.title("Filters")
st.sidebar.subheader("Select Values")

# Get unique values for the program and location columns
program_values = df["program"].unique()
location_values = df["location"].unique()

# Add "Select All" option to the program and location values
program_values = ["Select All"] + list(program_values)
location_values = ["Select All"] + list(location_values)

# Multiselect to choose programs and locations
selected_programs = st.sidebar.multiselect("Select Programs", program_values, default=["Select All"])
selected_locations = st.sidebar.multiselect("Select Locations", location_values, default=["Select All"])

# Filter the data based on selected programs and locations
filtered_df = df.copy()

if "Select All" not in selected_programs:
    filtered_df = filtered_df[filtered_df["program"].isin(selected_programs)]

if "Select All" not in selected_locations:
    filtered_df = filtered_df[filtered_df["location"].isin(selected_locations)]

# Check if the filtered dataframe is empty
if filtered_df.empty:
    st.write("No data available for the selected programs and locations.")
else:
    # Group the data by location and program and count the occurrences
    grouped_data = filtered_df.groupby(["location", "program"]).size().reset_index(name="count")

    # Get a list of unique programs
    unique_programs = grouped_data["program"].unique()

    # Generate a list of colors for the unique programs
    colorscale = colors.qualitative.Plotly
    program_colors = [colorscale[i % len(colorscale)] for i in range(len(unique_programs))]

    # Create the grouped bar chart
    fig_bar = go.Figure()

    for i, program in enumerate(unique_programs):
        program_data = grouped_data[grouped_data["program"] == program]
        fig_bar.add_trace(go.Bar(x=program_data["location"], y=program_data["count"], name=program, marker_color=program_colors[i]))

    fig_bar.update_layout(title="Program Count by Location",
                          xaxis_title="Location",
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
    st.plotly_chart(fig_pie_program, use_container_width=True)

    # Count the HPV16
    hpv16_count = filtered_df["hpv16"].value_counts()

    # Create the pie chart for HPV16
    fig_pie_hpv16 = go.Figure(data=[go.Pie(labels=hpv16_count.index, values=hpv16_count.values)])
    fig_pie_hpv16.update_layout(title="HPV16 Count")

    # Display the HPV16 pie chart
    st.plotly_chart(fig_pie_hpv16, use_container_width=True)

    # Count the HPV18
    hpv18_count = filtered_df["hpv18"].value_counts()

    # Create the pie chart for HPV18
    fig_pie_hpv18 = go.Figure(data=[go.Pie(labels=hpv18_count.index, values=hpv18_count.values)])
    fig_pie_hpv18.update_layout(title="HPV18 Count")

    # Display the HPV18 pie chart
    st.plotly_chart(fig_pie_hpv18, use_container_width=True)

    # Count the HPV DNA
    hpvdna_count = filtered_df["hpvdna"].value_counts()

    # Create the pie chart for HPV DNA
    fig_pie_hpvdna = go.Figure(data=[go.Pie(labels=hpvdna_count.index, values=hpvdna_count.values)])
    fig_pie_hpvdna.update_layout(title="HPV DNA Count")

    # Display the HPV DNA pie chart
    st.plotly_chart(fig_pie_hpvdna, use_container_width=True)

    # Count the Via Results
    via_results_count = filtered_df["Via_Results"].value_counts()

    # Create the pie chart for Via Results
    fig_pie_via_results = go.Figure(data=[go.Pie(labels=via_results_count.index, values=via_results_count.values)])
    fig_pie_via_results.update_layout(title="Via Results Count")

    # Display the Via Results pie chart
    st.plotly_chart(fig_pie_via_results, use_container_width=True)

    # Count the occurrences of program and Colposcopic_impression combinations
    program_colposcopic_count = filtered_df.groupby(["program", "Colposcopic_impression"]).size().reset_index(name="count")

    # Create the pie chart for program and Colposcopic_impression
    fig_pie_program_colposcopic = go.Figure(data=[go.Pie(labels= program_colposcopic_count["Colposcopic_impression"],
                                                        values=program_colposcopic_count["count"])])

    fig_pie_program_colposcopic.update_layout(title="Program - Colposcopic Impression")

    # Display the program - Colposcopic_impression pie chart
    st.plotly_chart(fig_pie_program_colposcopic, use_container_width=True)