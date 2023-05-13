# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Model Creation

            Behind the scenes, predictions are being made by a pre-trained machine learning algorithm. 

            Using the collected data (see the 'Data Collection' tab for information), 4 separate models were trained:

            1. Linear Regression
            2. Ridge Regression
            3. Polynomial Regression
            4. Random Forest Regression

            The random forest regressor yielded the highest score with an r-squared score of 0.81, and this is the model
            that was chosen. 

            The following are the input variables to the algorithm:

            1. Bedrooms
            2. Bathrooms
            3. Square Feet
            4. Lot Size
            5. Year Built
            6. Monthly HOA Fee
            7. Latitude Coordinate
            8. Longitude Coordinate

            As you can see from the input form, there is no latitude or longitude for the user to input.

            This information is obtained in the background when a user clicks on the 'Prediction' button. 
            An API call is made to Google Maps and the address, city, and zip code (the state is already known), is converted into
            latitude and longitude coordinates.

            After the latitude and longitude are received back from Google Maps, all 8 input variables are ready to go. 
            The variables are fed into the algorithm, and a prediction is returned to the user. 

            
            """
        ),
        dcc.Link(
            "Link to Medium article",
            href="https://medium.com/@daniel.kositzke/predicting-orlando-fl-home-sales-6158a51d106f",
        ),
    ],
)

layout = dbc.Row([column1])
