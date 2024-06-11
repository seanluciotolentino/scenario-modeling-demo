import streamlit as st
import pandas as pd
import plotly.express as px

# Function to forecast revenue based on media spend
def forecast_revenue(display_prospecting, display_retargeting, display_retention, native, olv, ctv):
    # Simple linear model for demonstration purposes
    return 1.5 * display_prospecting + 1.3 * display_retargeting + 1.2 * display_retention + 1.1 * native + 1.4 * olv + 1.6 * ctv

# Set the page layout to centered
st.set_page_config(layout="centered")

# Title of the app
st.title("Scenario Modeling: New Buyers")

# Initial data for the table
initial_data = {
    "Media Type": ["Display Prospecting", "Display Retargeting", "Display Retention", "Native", "OLV", "CTV"],
    "Scenario 1": [1000, 2000, 500, 1000, 1000, 1000],
    "Scenario 2": [1100, 1200, 400, 1100, 2100, 100],
    "Scenario 3": [900, 800, 200, 3000, 900, 1800]
}

# Create a DataFrame from the initial data
df = pd.DataFrame(initial_data)

# Display the editable table for media spend (only the first three rows)
st.header("Channel Mix")
edited_df = st.experimental_data_editor(df, use_container_width=True)

# Calculate the forecasted revenue based on the edited values
forecast_data = {
    "Scenario 1": [round(forecast_revenue(edited_df.loc[0, "Scenario 1"], edited_df.loc[1, "Scenario 1"], edited_df.loc[2, "Scenario 1"], edited_df.loc[3, "Scenario 1"], edited_df.loc[4, "Scenario 1"], edited_df.loc[5, "Scenario 1"]))],
    "Scenario 2": [round(forecast_revenue(edited_df.loc[0, "Scenario 2"], edited_df.loc[1, "Scenario 2"], edited_df.loc[2, "Scenario 2"], edited_df.loc[3, "Scenario 2"], edited_df.loc[4, "Scenario 2"], edited_df.loc[5, "Scenario 2"]))],
    "Scenario 3": [round(forecast_revenue(edited_df.loc[0, "Scenario 3"], edited_df.loc[1, "Scenario 3"], edited_df.loc[2, "Scenario 3"], edited_df.loc[3, "Scenario 3"], edited_df.loc[4, "Scenario 3"], edited_df.loc[5, "Scenario 3"]))]
}

# Create a DataFrame for the forecasted revenue
forecast_df = pd.DataFrame(forecast_data)

# Function to create a pie chart for a scenario
def create_pie_chart(scenario, show_legend):
    pie_data = {
        "Media Type": ["Display Prospecting", "Display Retargeting", "Display Retention", "Native", "OLV", "CTV"],
        "Spend": [edited_df.loc[0, scenario], edited_df.loc[1, scenario], edited_df.loc[2, scenario], edited_df.loc[3, scenario], edited_df.loc[4, scenario], edited_df.loc[5, scenario]]
    }
    pie_df = pd.DataFrame(pie_data)
    fig = px.pie(pie_df, values='Spend', names='Media Type', title=scenario, width=300, height=300)
    if not show_legend:
        fig.update_layout(showlegend=False)
    return fig

# Display pie charts for each scenario
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(create_pie_chart("Scenario 1", show_legend=False))
with col2:
    st.plotly_chart(create_pie_chart("Scenario 2", show_legend=False))
with col3:
    st.plotly_chart(create_pie_chart("Scenario 3", show_legend=False))

# Display the updated table (only the forecast row)
st.header("Forecasted New Buyers")
st.table(forecast_df)

# Create a bar plot for the forecasted revenue
bar_data = {
    "Scenario": ["Scenario 1", "Scenario 2", "Scenario 3"],
    "Forecasted New Buyers": [
        forecast_df.loc[0, "Scenario 1"],
        forecast_df.loc[0, "Scenario 2"],
        forecast_df.loc[0, "Scenario 3"]
    ]
}
bar_df = pd.DataFrame(bar_data)
bar_fig = px.bar(bar_df, x="Scenario", y="Forecasted New Buyers", title="", text="Forecasted New Buyers")

# Update the layout to display the y-axis values on the plot and remove the x-label
bar_fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
bar_fig.update_layout(xaxis_title='')

# Display the bar plot
st.plotly_chart(bar_fig, use_container_width=True)
