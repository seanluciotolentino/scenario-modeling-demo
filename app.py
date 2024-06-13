import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns

# Set the layout to wide
st.set_page_config(layout="wide")

# Initialize the data
channels = ['SEM', 'Social', 'Display', 'Linear/CTV', 'Retail Media']
weeks = [f'Week {i+1}' for i in range(36)]

# Create two columns for layout
col1, col2 = st.columns([2, 2])  # Adjust the width ratio to make the right column bigger

# Left column: Editable table and checkboxes
with col1:
    st.title("Scenario Modeling: Awareness")

    col1a, col1b = st.columns([2.4, 1])  # Adjust the width ratio to make the right column bigger
    with col1a:
        st.subheader("Model Parameters")
        data = {
            'Channel': ['SEM', 'Social', 'Display', 'Linear/CTV', 'Retail Media'],
            'Budget': [145_000_000, 675_000_000, 30_000_000, 186_000_000, 8_300_000],
            'Effectiveness': [0.2, 0.7, 0.45, 0.6, 0.35],
            'Awareness Weight': [0.25, 0.45, 0.35, 0.65, 0.2]
        }
        df = pd.DataFrame(data)
        edited_df = st.experimental_data_editor(df)

    with col1b:
        # Add a pie chart based on the channel budget
        fig_pie = go.Figure(data=[go.Pie(labels=channels, values=edited_df['Budget'], hole=.3)])
        fig_pie.update_layout(
            autosize=False,
            width=300,
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(
                x=0.1,
                y=-1,
                traceorder='normal',
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(0,0,0,0)'
            )
        )
        st.plotly_chart(fig_pie)

    st.subheader("Flighting")
    activation_matrix = np.array([
        [1]*len(weeks),
        [1,1,0,0,0,1]*6,
        [1,1,0,0,0,1]*6,
        [1]*len(weeks),
        [1]*len(weeks),
     ])

    for i, channel in enumerate(channels):
        cols = st.columns([5.5] + [1] * len(weeks))  # Widen the first column
        cols[0].write(f"**{channel}**")
        for j, col in enumerate(cols[1:]):
            activation_matrix[i, j] = col.checkbox("", value=bool(activation_matrix[i, j]), key=f"{channel}_{weeks[j]}")

    # Store the resulting 1/0 matrix as a variable
    activation_df = pd.DataFrame(activation_matrix, index=channels, columns=weeks)

# Calculate awareness contribution for each week
awareness_contribution = []

for week in weeks:
    week_contribution = 0
    for channel in channels:
        budget = edited_df.loc[edited_df['Channel'] == channel, 'Budget'].values[0]
        effectiveness = edited_df.loc[edited_df['Channel'] == channel, 'Effectiveness'].values[0]
        awareness_weight = edited_df.loc[edited_df['Channel'] == channel, 'Awareness Weight'].values[0]
        activations = activation_df.loc[channel, week]
        if activations > 0:
            budget_per_activation = budget / activations
            week_contribution += budget_per_activation * effectiveness * awareness_weight
    awareness_contribution.append(week_contribution)

# Shift the array down by two and drop the last two values
awareness_contribution = [0, 0] + awareness_contribution[:-2]

# Scale the awareness contribution to be between 0 and 0.05
min_val = min(awareness_contribution)
max_val = max(awareness_contribution)
scaled_contribution = [(x - min_val) / (max_val - min_val) * 0.05 for x in awareness_contribution]

# Add 0.65 to the entire array
final_contribution = [x + 0.65 for x in scaled_contribution]

# Create a DataFrame for awareness contribution
awareness_df = pd.DataFrame({'Week': weeks, 'Awareness Contribution': final_contribution})

# Calculate budget spent each week for each channel
budget_spent = []

for week in weeks:
    week_budget = []
    for channel in channels:
        budget = edited_df.loc[edited_df['Channel'] == channel, 'Budget'].values[0]
        activations = activation_df.loc[channel, week]
        if activations > 0:
            budget_per_activation = budget / activations
            week_budget.append(budget_per_activation)
        else:
            week_budget.append(0)
    budget_spent.append(week_budget)

budget_spent_df = pd.DataFrame(budget_spent, columns=channels, index=weeks)

# Right column: Stacked bar chart and line plot
with col2:
    st.subheader(" ")
    st.subheader("Awareness Forecast")

    fig = go.Figure()

    # Add stacked bar chart for budget spent using seaborn hls color palette
    colors = sns.color_palette("hls", len(channels)).as_hex()
    for i, channel in enumerate(channels):
        fig.add_trace(go.Bar(
            x=weeks,
            y=budget_spent_df[channel],
            name=channel,
            marker_color=colors[i % len(colors)]
        ))

    # Add line chart for awareness contribution on a secondary y-axis
    fig.add_trace(go.Scatter(
        x=weeks,
        y=awareness_df['Awareness Contribution'],
        mode='lines+markers',
        name='Awareness',
        line=dict(color='red', width=4),
        yaxis='y2'
    ))

    fig.update_layout(
        barmode='stack',
        xaxis_title='Week',
        yaxis_title='Impressions Budget',
        yaxis2=dict(
            title='Awareness',
            overlaying='y',
            side='right',
            range=[0.5, 0.9]  # Set ymin and ymax for the awareness plot
        ),
        legend=dict(
            x=1.12,
            y=1,
            traceorder='normal',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        ),
        legend_title='Legend',
        margin=dict(l=20, r=20, t=20, b=20),
        autosize=False,
        width=800,
        height=550
    )

    st.plotly_chart(fig, use_container_width=True)
