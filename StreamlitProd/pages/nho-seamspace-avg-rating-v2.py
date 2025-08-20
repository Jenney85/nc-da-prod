import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.io as pio

# import plotly.graph_objects as go
pio.templates.default = "plotly"

st.set_page_config(page_title="RPTSeamspace1: Seamspace Emotions Avg Rating", layout="wide")
st.title("📊 Seamspace Emotions Avg Rating (RPTSeamspace1)")

# Check login
if "user_email" not in st.session_state:
    st.warning("Please log in first from the main page.")
    st.stop()

email = st.session_state["user_email"]
role = st.session_state["user_role"]
st.write(f"**You are logged in under {email} as {role}**")

# Load data
df = pd.read_excel("Seamspace_Emotions-Data.xlsx", sheet_name="Emotions-nolink", header=1)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Filter by user
if role != "admin":
    df = df[df["User email"] == email]

# check if empty
if df.empty:
    st.warning("No data found for the selected user.")
    st.warning("Please log in with a different account from the main page.")
    st.stop()

# Sidebar filters
st.sidebar.header("📅 Filter Options")
start_date = st.sidebar.date_input("Start Date", value=df["Timestamp"].min())
end_date = st.sidebar.date_input("End Date", value=df["Timestamp"].max())

indicators = df["Indicator"].dropna().unique()
selected_indicators = st.sidebar.multiselect("🎯 Select up to 5 Indicators", indicators, max_selections=5)

if role == "admin":
    emails = df["User email"].dropna().unique() # if more than xx, perhaps just ask for input
    selected_emails = st.sidebar.multiselect("🎯 Select up to 3 emails", emails, max_selections=3)
#   selected_emails = st.text_input("Enter user email to filter:").strip().lower()
else:
    selected_emails = ""

# Create columns for positive and negative ratings
df['Positive_Rating'] = np.where(df['Rating'] > 0, df['Rating'], np.nan)

# Create "Negative Rating" column
df['Negative_Rating'] = np.where(df['Rating'] < 0, df['Rating'], np.nan)

# Apply filters
mask = (df["Timestamp"] >= pd.to_datetime(start_date)) & (df["Timestamp"] <= pd.to_datetime(end_date))
if selected_indicators:
    mask &= df["Indicator"].isin(selected_indicators)
if selected_emails:
    mask &= df["User email"].isin(selected_emails)

filtered = df[mask]

if filtered.empty:
    st.warning("No data found for the selected filters.")
    # st.warning("Please select at least one indicator.")
    st.stop()

# Total unique session count
total_unique_sessions = filtered["sess6digit"].nunique()
st.metric(label="Total Unique Sessions: ", value=total_unique_sessions)

# Average Rating 
# mean_ratings = filtered["Rating"].mean()
# rounded_mean_ratings = round(mean_ratings, 2)  # Round to 2 decimal places
# st.metric("Average Rating: ", rounded_mean_ratings)

# Mean of positive Rating 
positive_mean = filtered['Positive_Rating'].mean() 
rounded_positive_mean = round(positive_mean, 2)  # Round to 2 decimal places
st.metric("Average Positive Rating: ", rounded_positive_mean)

# Mean of negative Rating 
negative_mean = filtered['Negative_Rating'].mean() 
rounded_negative_mean = round(negative_mean, 2)  # Round to 2 decimal places
st.metric("Average Negative Rating: ", rounded_negative_mean)

# Combined Mean (total mean)
combined_mean = filtered['Rating'].mean()
rounded_combined_mean = round(combined_mean, 2)  # Round to 2 decimal places
st.metric("Average Combined Rating: ", rounded_combined_mean)

# --- Display Results in Streamlit ---

st.header("Results:")

# Display positive mean
# st.metric(label="mean of Positive Rating", value=positive_mean) 

# Display negative mean
# st.metric(label="mean of Negative Rating", value=negative_mean)

# Display combined mean
# st.metric(label="Combined mean", value=combined_mean)

# Optional: Display the DataFrame itself
st.dataframe(filtered)

# Group data and create the line chart
# Create columns for positive and negative ratings

grouped_p_data = filtered.groupby([filtered['Timestamp'].dt.date, 'Indicator']).agg(
       Count=('sess6digit', 'nunique'),
       PRating= ('Positive_Rating', 'mean'),  # Calculate mean of positive ratings
       ).reset_index().rename(columns={'Timestamp': 'Date'})

grouped_n_data = filtered.groupby([filtered['Timestamp'].dt.date, 'Indicator']).agg(
       Count=('sess6digit', 'nunique'),
       NRating= ('Negative_Rating', 'mean'),  # Calculate mean of negative ratings
     ).reset_index().rename(columns={'Timestamp': 'Date'})

# Group by Date and Indicator and aggregate composite_score -- old code
# grouped_data = filtered.groupby([filtered['Timestamp'].dt.date, 'Indicator'])['composite_score'].agg(['mean', 'min', 'max']).reset_index().rename(columns={"Timestamp": "Date", "Indicator": "Indicator", "mean": "Avg", "min": "Min" , "max": "Max"})
   
st.subheader("Aggregated Positive Rating Statistics")
grouped_p_data = grouped_p_data.dropna(how='any',axis=0)
st.dataframe(grouped_p_data)

st.subheader("Aggregated Negative Rating Statistics")
grouped_n_data = grouped_n_data.dropna(how='any',axis=0)
st.dataframe(grouped_n_data)

st.subheader(" 📆 Avg Ratings Over Time for Selected Indicators")
    # Create columns
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Line Rating in the first column
with col1:
      # st.subheader(" 📆 Line Chart: ")
      line_fig1 = px.line(grouped_p_data,
                      x='Date',
                      y='PRating',
                      color='Indicator',  # Color lines by indicator
                      title='Line Chart -- Mean Positive Rating Over Time',
                      # trendline="ols"
       )
      #line_fig.update_layout(width=844, height=390, autosize=False)
      st.plotly_chart(line_fig1, use_container_width=True)
    
      # Scatter plot in the second column
with col2:
      # st.subheader("📆 Scatter Chart: ")
      scatter_fig1 = px.scatter(grouped_p_data,
                      x='Date',
                      y='PRating',
                      color ='Indicator',  # Color lines by indicator
                      # trendline="ols",
                      title='Scatter - Mean Positive Rating Over Time'
                      )
      #scatter_fig.update_layout(width=844, height=390, autosize=False)
      st.plotly_chart(scatter_fig1, use_container_width=True)      

with col3:
      # st.subheader(" 📆 Line Chart: ")
      line_fig2 = px.line(grouped_n_data,
                      x='Date',
                      y='NRating',
                      color='Indicator',  # Color lines by indicator
                      title='Line Chart -- Mean Negative Rating Over Time',
                      # trendline="ols"
       )
      #line_fig.update_layout(width=844, height=390, autosize=False)
      st.plotly_chart(line_fig2, use_container_width=True)
    
      # Scatter plot in the second column
with col4:
      # st.subheader("📆 Scatter Chart: ")
      scatter_fig2 = px.scatter(grouped_n_data,
                      x='Date',
                      y='NRating',
                      color ='Indicator',  # Color lines by indicator
                      # trendline="ols",
                      title='Scatter - Mean Negative Rating Over Time'
                      )
      #scatter_fig.update_layout(width=844, height=390, autosize=False)
      st.plotly_chart(scatter_fig2, use_container_width=True)

# save original code
# chart = alt.Chart(summary).mark_bar().encode(
#    x=alt.X("Indicator:N", sort="-y", title="Indicator"),
#    y=alt.Y("Avg:Q", title="Average composite_score"),
#    tooltip=["Indicator", "Avg", "Min", "Max", "composite_scores"]
# ).properties(
#    width=500,
#    height=300
#)

# st.altair_chart(chart, use_container_width=True)

