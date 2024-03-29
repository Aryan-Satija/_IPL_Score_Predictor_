import math 
import numpy as np
import pickle
import streamlit as st

st.set_page_config(page_title = 'IPL_Score_Predictor')

model = pickle.load(open('C:/Users/Dell/OneDrive/Desktop/ipl_score_predictor/ipl_ml_model.pkl', 'rb'))

st.title('IPL SCORE PREDICTOR')

with st.expander('Description'):
    st.info('A ML Model to predict IPL Scores between teams in an ongoing match.')


current_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Delhi Daredevils', 'Sunrisers Hyderabad']
team_index = dict(zip(current_teams, range(len(current_teams))))


prediction_array = []

batting_team = st.selectbox('Select Batting Team:', current_teams)

prediction_array = prediction_array + [0 if i != team_index[batting_team] else 1 for i in range(7)]


bowling_team = st.selectbox('Select Bowling Team:', current_teams)
prediction_array = prediction_array + [0 if i != team_index[bowling_team] else 1 for i in range(7)]


def adjust_overs(overs):
    if ((overs % 1) >= 0.6):
        overs += 0.4
    return overs


col1, col2 = st.columns(2)

with col1:
    overs = 0.0
    overs = st.number_input('Enter The Current Over', min_value=0.0, max_value=20.0, value=overs, step=0.1)
    overs = round(overs, 2)
    overs = adjust_overs(overs)
    overs = round(overs, 2)
    
with col2:
    runs = st.number_input('Enter Total Runs scored as of now', min_value=0, value=0, step=1)


wickets =st.slider('Enter Wickets fallen till now',0,9)
wickets = int(wickets)

col3, col4 = st.columns(2)
with col3:
    runs_in_prev_5 = st.number_input('Runs scored in the last 5 overs',min_value=0,max_value=runs,step=1)

with col4:
    wickets_in_prev_5 = st.number_input('Wickets scored in the last 5 overs',min_value=0,max_value=wickets,step=1)
    

prediction_array = prediction_array + [runs, wickets, overs, runs_in_prev_5, wickets_in_prev_5]

stadiums = ['Barabati Stadium','Brabourne Stadium', 'Buffalo Park','De Beers Diamond Oval', 'Dr DY Patil Sports Academy', 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium', 'Dubai International Cricket Stadium', 'Eden Gardens', 'Feroz Shah Kotla', 'JSCA International Stadium Complex', 'Kingsmead', 'M Chinnaswamy Stadium', 'MA Chidambaram Stadium, Chepauk', 'Maharashtra Cricket Association Stadium', 'New Wanderers Stadium', 'Newlands', 'OUTsurance Oval', 'Rajiv Gandhi International Stadium, Uppal', 'Sardar Patel Stadium, Motera', 'Sawai Mansingh Stadium', 'Shaheed Veer Narayan Singh International Stadium', 'Sharjah Cricket Stadium', 'Sheikh Zayed Stadium', "St George's Park", 'Subrata Roy Sahara Stadium', 'SuperSport Park', 'Wankhede Stadium']
stadium_index = dict(zip(stadiums, range(len(stadiums))))

stadium = st.selectbox('Select Stadium', stadiums)
prediction_array = prediction_array + [0 if i != stadium_index[stadium] else 1 for i in range(len(stadiums))]

if st.button('Predict Score'):
    prediction_array = np.array([prediction_array])
    projected_score = model.predict(prediction_array)
    projected_score[0] = int(round(projected_score[0], 0))
    st.success(f"Predicted Score : {projected_score[0] - 5} - {projected_score[0] + 5}")