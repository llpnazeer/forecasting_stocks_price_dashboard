
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV file
data = pd.read_csv('report (1).csv')

# Dashboard Title
st.title("Models Performance Dashboard")

# Section: Overview of Mean Squared Error (MSE)
st.header("Overall MSE Comparison")
fig = px.bar(data, x='Model_name', y='MSE', color='Symbol', barmode='group',
             labels={'MSE': 'Mean Squared Error'},
             title="Overall Mean Squared Error by Model")
st.plotly_chart(fig)

# Section: MSE Trend Over Weeks
st.header("MSE Trend Over Weeks Summary")
mse_weeks = data.melt(id_vars=['Symbol', 'Model_name'], value_vars=['MSE_week_1', 'MSE_week_2', 'MSE_week_3', 'MSE_week_4'],
                      var_name='Week', value_name='MSE_value')

fig2 = px.line(mse_weeks, x='Week', y='MSE_value', color='Model_name', line_group='Symbol',
               labels={'MSE_value': 'Mean Squared Error', 'Week': 'Week'},
               title="MSE Trend Over Weeks")
st.plotly_chart(fig2)

# Section: Best Model by Symbol
st.header("Best Model by Symbol")
best_models = data.loc[data.groupby('Symbol')['MSE'].idxmin()]

# Count how many times each model is the best
best_model_counts = best_models['Model_name'].value_counts().reset_index()
best_model_counts.columns = ['Model_name', 'Count']

fig3 = px.bar(best_model_counts, x='Model_name', y='Count',
              labels={'Count': 'Number of Times Best', 'Model_name': 'Model Name'},
              title="Count of Best Model by Symbol")
st.plotly_chart(fig3)

# Section: MSE Trend Over Weeks
st.header("MSE Trend Over Weeks For Each Ticker")

# Convert the week names to ordered categorical values to ensure proper plotting
mse_weeks['Week'] = pd.Categorical(mse_weeks['Week'], categories=['MSE_week_1', 'MSE_week_2', 'MSE_week_3', 'MSE_week_4'], ordered=True)

# Create a line chart for each symbol to show the MSE trend over the weeks
symbols = mse_weeks['Symbol'].unique()

for symbol in symbols:
    st.subheader(f"MSE Trend for {symbol}")
    symbol_data = mse_weeks[mse_weeks['Symbol'] == symbol]
    
    fig_ = px.line(symbol_data, x='Week', y='MSE_value', color='Model_name',
                  labels={'MSE_value': 'Mean Squared Error', 'Week': 'Week'},
                  title=f"MSE Trend Over Weeks for {symbol}")
    st.plotly_chart(fig_)


# Section: Detailed Metrics
st.header("Detailed Metrics by Model")
st.dataframe(data)
