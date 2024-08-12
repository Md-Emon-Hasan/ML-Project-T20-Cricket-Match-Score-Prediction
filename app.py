from flask import Flask
from flask import render_template
from flask import request
import pickle
import pandas as pd
import os

app = Flask(__name__)

# Define the path to the model file
model_path = r'models/model.pkl'

# Check if the model file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"The file at {model_path} does not exist.")

# Load the model
try:
    with open(model_path, 'rb') as model_file:
        pipe = pickle.load(model_file)
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

# Teams and venues lists
teams = [
    'Australia', 'New Zealand', 'South Africa', 'England', 'India', 'West Indies', 'Pakistan', 'Bangladesh', 'Afghanistan', 'Sri Lanka'
]

venues = [
    'Shere Bangla National Stadium', 'R Premadasa Stadium', 'Dubai International Cricket Stadium', 'New Wanderers Stadium', 'Eden Park', 'Newlands', 'Pallekele International Cricket Stadium', 'Kensington Oval, Bridgetown', 'Melbourne Cricket Ground', 'Beausejour Stadium, Gros Islet', 'Kennington Oval', 'Kingsmead', 'Westpac Stadium', 'Central Broward Regional Park Stadium Turf Ground', 'Seddon Park', 'SuperSport Park', 'Old Trafford', 'Zahur Ahmed Chowdhury Stadium', 'R.Premadasa Stadium, Khettarama', 'Sheikh Zayed Stadium', 'Sydney Cricket Ground', 'Trent Bridge', 'The Rose Bowl', 'Bay Oval', 'Wankhede Stadium', 'Eden Gardens', 'Gaddafi Stadium', 'Vidarbha Cricket Association Stadium, Jamtha', "Lord's", 'Adelaide Oval', 'M Chinnaswamy Stadium', 'Warner Park, Basseterre', 'Sophia Gardens', "Queen's Park Oval, Port of Spain", 'Brisbane Cricket Ground, Woolloongabba', 'Edgbaston', 'Mahinda Rajapaksa International Cricket Stadium, Sooriyawewa', 'Shere Bangla National Stadium, Mirpur', 'The Wanderers Stadium', 'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium', 'Feroz Shah Kotla', 'Punjab Cricket Association IS Bindra Stadium, Mohali', 'County Ground', 'National Stadium', 'Stadium Australia'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        try:
            batting_team = request.form['batting_team']
            bowling_team = request.form['bowling_team']
            venue = request.form['venue']
            current_score = int(request.form['current_score'])
            overs = float(request.form['overs'])
            wickets = int(request.form['wickets'])
            last_five = int(request.form['last_five'])

            ball_left = 120 - (overs * 6)
            wickets_left = 10 - wickets
            crr = current_score / overs if overs != 0 else 0  # Prevent division by zero

            input_df = pd.DataFrame(
                {'batting_team': [batting_team],
                'bowling_team': [bowling_team],
                'venue': [venue],
                'current_score': [current_score],
                'ball_left': [ball_left],
                'wickets_left': [wickets_left],
                'current_run_rate': [crr],
                'last_five': [last_five],
                'wicket_left': [wickets_left]}
            )

            result = pipe.predict(input_df)
            prediction = int(result[0])
        except Exception as e:
            prediction = f"Error: {str(e)}"  # Display error message in case of an exception
    return render_template('index.html', teams=sorted(teams), venues=sorted(venues), prediction=prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)