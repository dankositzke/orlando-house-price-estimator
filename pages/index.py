# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import os
import pandas as pd
import joblib
import sklearn

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Sales Price Estimator 

            This model has been created using home sales data from April-September 2021 from redfin.com for the greater Orlando, Florida area. 
            
            Sales prices can be predicted for homes from Lake Mary to Kissimmee (North-South), Winter Garden to Alafaya (West-East), and everywhere in between.

            """
        ),
        html.Div(
            [
                # Obtain house address from user input
                html.P(["Address"]),
                dcc.Input(id="address", type="text"),
                html.Br(),
                html.Br(),
                
                # Obtain city from user input
                html.P(["City"]),
                dcc.Input(id="city", type="text"),
                html.Br(),
                html.Br(),
                
                # Obtain zip code from user input
                html.P(["Zip Code"]),
                dcc.Input(id="zip-code", type="text"),
                html.Br(),
                html.Br(),
            ]
        ),
    ],
    md=3,
)


column2 = dbc.Col(
    [
        html.Div(
            [
                # Obtain number of bedrooms from user input
                html.P(["Bedrooms"]),
                dcc.Input(id="bedrooms", type="text"),
                html.Br(),
                html.Br(),
                
                # Obtain number of bathrooms from user input
                html.P(["Bathrooms"]),
                dcc.Input(id="bathrooms", type="text"),
                html.Br(),
                html.Br(),
                
                # Obtain square feet from user input
                html.P(["Square Feet"]),
                dcc.Input(id="sqft", type="text"),
                html.Br(),
                html.Br(),
                
                # Obtain lot size from user input
                html.P(["Lot Size (in square feet)"]),
                dcc.Input(id="lot-size", type="text"),
                html.Br(),
                html.Br(),
                
                # Obtain year built from user input
                html.P(["Year Built"]),
                dcc.Input(id="year-built", type="text"),
                html.Br(),
                html.Br(),
                
                # Obtain monthly HOA fee (if any) from user input
                html.P(["Monthly HOA Fee"]),
                html.P(["(Enter 0 if none)"]),
                dcc.Input(id="hoa-fee", type="text"),
                html.Br(),
                html.Br(),
                html.Button(id="prediction_button", n_clicks=0, children="Prediction"),
            ]
        )
    ],
    md=3,
)


column3 = dbc.Col(
    [
        html.Div(
            [
                html.Br(),
                html.H4(
                    "The predicted sales price is...", style={"fontWeight": "bold"}
                ),
                html.Br(),
                html.Br(),
                html.H2(id="prediction-content", style={"fontWeight": "bold"}),
            ]
        ),
    ]
)


# Set up items for API call to get latitude and longitude
import requests

mapquest_api_key = os.getenv("MAPQUEST_API_KEY")

@app.callback(Output("address_output", "children"), [Input("address", "value")])
def check_address(address):
    return "Current address value: {}".format(address)


no_clicks = 0

@app.callback(
    Output("prediction-content", "children"),
    [
        Input("prediction_button", "n_clicks"),
        Input("address", "value"),
        Input("city", "value"),
        Input("zip-code", "value"),
        Input("bedrooms", "value"),
        Input("bathrooms", "value"),
        Input("sqft", "value"),
        Input("lot-size", "value"),
        Input("year-built", "value"),
        Input("hoa-fee", "value"),
    ],
)
def check_user_inputs(
    clicks,
    address,
    city,
    zip_code,
    bedrooms,
    bathrooms,
    sqft,
    lotsize,
    yearbuilt,
    hoafee,
):
    global no_clicks
    user_input_lat = 0
    user_input_lng = 0
    y_pred = 0
    index = 0

    if (
        clicks > no_clicks # don't make API call for lat/lng until user clicks 'Submit'
        and round(float(lotsize), 0) > 100
        and round(float(sqft), 0) > 500
        and round(float(bathrooms), 0) > 0
        and round(float(bedrooms), 0) > 0
        and round(float(yearbuilt), 0) > 1800
        and len(str(address)) > 5
        and len(str(city)) > 3
        and len(str(zip_code)) > 3
    ):

        no_clicks = no_clicks + 1
        user_input_address = str(address) + " " + str(city) + " FL " + str(zip_code)
        params = {
            "key": mapquest_api_key,
            "location": user_input_address,
        }
        
        response = requests.get(
            "http://www.mapquestapi.com/geocoding/v1/address", params=params
        ).json()
        
        user_input_lat = response["results"][0]["locations"][0]["latLng"]["lat"]
        user_input_lng = response["results"][0]["locations"][0]["latLng"]["lng"]

    if user_input_lat != 0 and user_input_lng != 0:
        pred_df = pd.DataFrame(
            
            data=[
                [
                    index,
                    bedrooms,
                    bathrooms,
                    sqft,
                    lotsize,
                    yearbuilt,
                    hoafee,
                    user_input_lat,
                    user_input_lng,
                ]
            ],
        )

        # Load in pre-trained RandomForestRegressor model
        pipeline = joblib.load("assets/pipe.joblib")
        y_pred = int(pipeline.predict(pred_df)[0])

    return f"${y_pred:,}"


layout = dbc.Row([column1, column2, column3])
