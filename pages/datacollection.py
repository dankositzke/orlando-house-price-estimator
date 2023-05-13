# Imports from 3rd party libraries
import dash
from dash.dcc.Markdown import Markdown
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import os

# Imports from this application
from app import app

app_dir = os.path.dirname(os.path.abspath(__file__))
img1_path = os.path.join(app_dir, "Redfin_big.PNG")

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Data Collection

            All 'sold' housing data from the previous 6 months (Apr-Sep 2021) were collected from redfin.com using python's 'selenium' automation library.

            Redfin.com has a nice feature that allows you to download a csv file of the current properties on your screen.
            This is shown in the following image.

            When a user clicks on the download button, however, they are only given the first 9 pages of homes - about 350 properties. 
            This creates a problem, because depending on how zoomed in or zoomed out the map is, there may be 50, 500, or 5000 available homes.

            If we click on the download button when, say, 1000 homes are displayed on the map, we are only able to download a third of the available data.

            This is where I used the selenium automation. I split the map into a 15x15 grid of latitude and longitude coordinates, and wrote a script that automatically alters the redfin URL based on the particular geographic square that we want. 
            The automation clicks on the download button for us, and then moves onto the next grid square by altering the latitude and longitude coordinates within the URL, clicking on the download button again, and so on. 
            This occurs until the script has moved through the entire grid and downloaded all of the data. 

            """
        ),
        html.Br(),
        html.Img(
            src="assets/redfinwithgrid.png", style={"height": "50%", "width": "80%"}
        ),
        html.Br(),
        html.Br(),
        dcc.Markdown(
            """
        
            The reason this is helpful is because since we are zoomed in enough, now all of the data can be downloaded without missing any homes or trying to manually zoom in and out of specific neighborhoods.

            After the script finished, I ended up with approximately 20,000 records spread across 225 csv files.
            I merged the files together in a few clicks using Microsoft Excel Power Query and then used the merged data to create the model. Information about the model can be found in the 'Model' tab. 
            """
        ),
    ],
)


layout = dbc.Row([column1])
