import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

import plotly.express as px

GSHEET_URL = "https://docs.google.com/spreadsheets/d/1HQz0k_VztkcI_MXvMKw0bHCcVwjPZ0nRsB_9FFA5mzo/edit"

def get_data(url : str = GSHEET_URL) -> pd.DataFrame:
    """Get data from the google sheet defined in .streamlit/secrets.toml """
    conn =  st.connection("gsheets", type=GSheetsConnection)

    #read in data as a df 
    data = conn.read(spreadsheet=url, ttl=0)

    return data

def append_data(record: dict, url: str = GSHEET_URL) -> pd.DataFrame:
    """
    Append a row to the google sheet and return the updated data.

    Append a new reecord by getting the current data, appending the new record, and updating the sheet.  
    Given more time, we can use the raw API to append directly.
    """
    
    existing_data = get_data()

    #stack old data with new record
    #TODO: with more time, use the requests library and write an AppendCellsRequest (https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/request#appendcellsrequest) myself
    updated_data = pd.concat([existing_data, pd.DataFrame([record])], ignore_index=True)

    conn = st.connection("gsheets", type=GSheetsConnection)

    try: 
        conn.update(spreadsheet=url, data=updated_data)

        st.success("Record added successfully!")

        return updated_data

    except Exception as e:
        import traceback

        st.error("Failed to add record. Please try again.")

        #the console error for debugging
        print(f"Error: {e}")
        print(traceback.format_exc())

def draw_date_slicer(df: pd.DataFrame) -> str : 
    """
    Draw a date selector for the user to filter the data by date.
    Returns the selected date as a string.
    """

    #fix the timestamp column to be a datetime object
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    #get the unique dates in descending order
    unique_dates = sorted(df["Timestamp"].dt.date.unique(), reverse=True)

    #draw the date selector
    selected_date = st.selectbox(
        "Select a date to view",
        options=unique_dates,
        format_func=lambda d: d.strftime("%A, %b %d")
    )

    return selected_date   


@st.fragment(run_every=5)
def draw_bars() -> None:
    """
    Draw a date slicer and a bar chart of mood counts for the selected date.
    """

    df = get_data()

    #make the date filter 
    selected_date = draw_date_slicer(df)  

    #filter the data by the selected date
    filtered_df = df[df["Timestamp"].dt.date == pd.to_datetime(selected_date).date()]

    if filtered_df.empty:
        st.warning(f"No data available for the selected date {selected_date}.")
        return

    #count the moods
    mood_counts = filtered_df["Mood"].value_counts().reset_index()
    mood_counts.columns = ["Mood", "Count"]

    #draw the bar chart
    fig = px.bar(mood_counts, 
                 x="Mood", 
                 y="Count", 
                 title=f"Mood Counts for {selected_date}",
                 category_orders={"Mood": [            '😤 : Angry', 
                                    '😵‍💫 : Confused', 
                                    '😐 : Neutral', 
                                    '😊 : Pleased',
                                    '🎉 : Ecstatic']
                                }              
                )    
    st.plotly_chart(fig, use_container_width=True)

#page setup stuff 
st.set_page_config(page_title="Mochi Health Mood Tracker", layout="wide")

#initialize session state
if "just_submitted" not in st.session_state:
    st.session_state["just_submitted"] = False

#these exapnder sections would likely be their own pages in a more polished app
with st.expander(" # Mood Intake Form",icon = '📝', expanded=True):
    st.markdown(
        """
        ## Mood Intake Form
        This form allows you to log the current ticket's mood so we can analyze the _feel_ of a given day.
        """
    )
    #draw the form
    with st.form("mood_intake"): 
        moods = (
            '😤 : Angry', 
            '😵‍💫 : Confused', 
            '😐 : Neutral', 
            '😊 : Pleased',
            '🎉 : Ecstatic',
        )

        mood = st.selectbox("Select the current _vibe_:"
                            , options=moods
                            , index = 2 #default to neutral
                            )
        
        note = st.text_input("Optional note:")

        submitted = st.form_submit_button("Submit")

        if submitted:

            with st.spinner("Adding data..."):
                _  = append_data({
                    "Mood": mood,
                    "Note": note,
                    "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                })   
                st.session_state["just_submitted"] = True

with st.expander("# Mood Analysis", icon='📊', expanded=True):

    #draw the bar chart
    draw_bars()




    