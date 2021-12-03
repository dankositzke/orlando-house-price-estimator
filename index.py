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
                # html.Button("Click here to see prediction", id="prediction"),
                html.Button(id="prediction_button", n_clicks=0, children="Prediction"),
                # html.Div(id="display_prediction"),
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


# Set up items for google maps API call to get latitude and longitude
import requests


base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
google_api_key = os.getenv("GOOGLE_API_KEY")


@app.callback(Output("address_output", "children"), [Input("address", "value")])
def check_address(address):
    return "Current address value: {}".format(address)


no_clicks = 0

# Determine whether to make the Google maps API call
# The purpose of this is to only make API calls once the user
# has input the necessary arguments. Otherwise, the callback function
# will continually make API calls to Google maps as the user changes the
# inputs while typing each individual letter or number into the box. This
# would be a big problem, because the Google maps API quota would get used
# up extremely fast. Therefore, this function will act as 'gate' to ensure
# that the API calls only happen once all of the data has been input by
# the user.
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
        clicks > no_clicks
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
        user_input_address = str(address) + str(city) + "FL" + str(zip_code)
        params = {"key": google_api_key, "address": user_input_address}
        response = requests.get(base_url, params).json()
        if response["status"] == "OK":
            user_input_lat = round(
                (response["results"][0]["geometry"]["location"]["lat"]), 6
            )
            user_input_lng = round(
                (response["results"][0]["geometry"]["location"]["lng"]), 6
            )

    if user_input_lat != 0 and user_input_lng != 0:
        pred_df = pd.DataFrame(
            # columns=[
            #     "Beds",
            #     "Baths",
            #     "Square Feet",
            #     "Lot Size",
            #     "Year Built",
            #     "HOA/Month",
            #     "Latitude",
            #     "Longitude",
            # ],
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

        pipeline = joblib.load("assets/pipe.joblib")
        y_pred = int(pipeline.predict(pred_df)[0])

    return f"${y_pred:,}"


layout = dbc.Row([column1, column2, column3])
