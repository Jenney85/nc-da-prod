import streamlit as st
import pandas as pd
import altair as alt
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="HORPT1: Unique Session Check-ins", layout="wide")
st.title("📊 HO Number of Unique Check-in Sessions (HORPT1)")

# Check login
if not st.session_state.get("authenticated", False):
    st.warning("Please log in first from the main page.")
    st.stop()

email = st.session_state["user_email"]
role = st.session_state["user_role"]
st.write(f"**You are logged in under {email} as {role}**")

def get_google_sheets_client():
    """
    Initialize Google Sheets client using service account credentials
    """
    try:
        # Get credentials from Streamlit secrets
        credentials_dict = st.secrets["google_service_account"]
        
        # Define the scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Create credentials
        credentials = Credentials.from_service_account_info(
            credentials_dict, 
            scopes=scope
        )
        
        # Initialize the client
        client = gspread.authorize(credentials)
        return client
    
    except Exception as e:
        st.error(f"Authentication failed: {str(e)}")
        st.error("Please check your Google service account configuration.")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_nho_data():
    """
    Load NHO data from Google Sheets
    """
    try:
        client = get_google_sheets_client()
        if client is None:
            return pd.DataFrame()
        
        # Get the Google Sheet ID from secrets
        sheet_id = st.secrets["nho_data_sheet_id"]
        
        # Open the sheet
        sheet = client.open_by_key(sheet_id)
        
        # Get the specific worksheet (equivalent to "00-HO-Data-Prime-no-link")
        worksheet = sheet.worksheet("00-HO-Data-Prime-no-link")
        
        # Get all records
        records = worksheet.get_all_records()
        
        # Convert to DataFrame
        df = pd.DataFrame(records)
        
        # Convert timestamp column to datetime
        if 'Timestamp' in df.columns:
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
        
        # Clean up empty rows
        df = df.dropna(how='all')
        
        return df
    
    except Exception as e:
        st.error(f"Failed to load NHO data from Google Sheets: {str(e)}")
        return pd.DataFrame()

# Load and prep data
with st.spinner("Loading NHO data..."):
    df = load_nho_data()

if df.empty:
    st.error("No NHO data found. Please check your Google Sheets configuration.")
    st.stop()

# Change point 

# Filter by user
if role != "admin":
    df = df[df["User email"] == email]

# check if empty
if df.empty:
    st.warning("No data found for the selected user.")
    st.warning("Please log in with a different account from the main page.")
    st.stop()
    
# Sidebar filters
st.sidebar.header("📅 Filter by Date Range")
start_date = st.sidebar.date_input("Start Date", value=df["Timestamp"].min())
end_date = st.sidebar.date_input("End Date", value=df["Timestamp"].max())

# Apply date filter
mask = (df["Timestamp"] >= pd.to_datetime(start_date)) & (df["Timestamp"] <= pd.to_datetime(end_date))
filtered = df[mask]

st.subheader("Filtered Data")
st.dataframe(filtered)

# Total unique session count
total_unique_sessions = filtered["Session id"].nunique()
st.metric(label="Total Unique Sessions", value=total_unique_sessions)

# ✅ DAILY CHART (Altair version, smaller chart with integer ticks)
st.markdown("### 📆 Unique Sessions by Day (Compact View)")
daily_df = (
    filtered.groupby(filtered["Timestamp"].dt.date)["Session id"]
    .nunique()
    .reset_index()
    .rename(columns={"Timestamp": "Date", "Session id": "Unique Sessions"})
)

daily_chart = alt.Chart(daily_df).mark_bar().encode(
    x=alt.X("Date:T", title="Date"),
    y=alt.Y("Unique Sessions:Q", 
            axis=alt.Axis(
              title="Sessions", 
              tickMinStep=1,  # Ensure ticks are at least 1 unit apart
              format="i" # Format as integers (no decimal places) 
            ))
).properties(
    width=400,
    height=250
)

st.altair_chart(daily_chart, use_container_width=False)

# Weekly chart
st.markdown("### 📆 Unique Sessions by Week")
weekly = filtered.resample("W", on="Timestamp")["Session id"].nunique()
st.bar_chart(
    weekly, 
    width=400,  # Set the width in pixels 
    height=200, # Set the height in pixels
    use_container_width=False # Ensure width and height are respected
)
# repeat sizing for the following chart
# Monthly chart
st.markdown("### 📆 Unique Sessions by Month")
monthly = filtered.resample("ME", on="Timestamp")["Session id"].nunique()
st.bar_chart(
    monthly,
    width=400,  # Set the width in pixels 
    height=200, # Set the height in pixels
    use_container_width=False # Ensure width and height are respected
)

# Yearly chart
st.markdown("### 📆 Unique Sessions by Year")
yearly = filtered.resample("YE", on="Timestamp")["Session id"].nunique()
st.bar_chart(
    yearly,
    width=400,  # Set the width in pixels 
    height=200, # Set the height in pixels
    use_container_width=False # Ensure width and height are respected
)
