import requests

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database

import plotly.express as px
import pandas as pd

from dash import dash
from dash import dcc
from dash import html as dhtml

# connect on localhost:27017 (default)
mongo = MongoClient()

# get our db/collection; this will create on first run (mongo doesn't actually create until data is added)
nhl_db: Database = mongo["nhl"]
seasons: Collection = nhl_db["seasons"]

# create some indices on nested data in the json doc; speeds up search
indices = (
    "seasonId",
    "regularSeasonStartDate"
)
[seasons.create_index(index) for index in indices]

# populate some data
raw_data = requests.get("https://statsapi.web.nhl.com/api/v1/seasons").json()
seasons.insert_many(raw_data["seasons"])

# get the data
# all seasons that started before 1980
# we only want a couple of columns
desired_cols = ("seasonId", "numberOfGames")
cursor: Cursor = seasons.find({"regularSeasonStartDate": {"$lt": "1980-01-01"}}, {col: 1 for col in desired_cols})
data = pd.DataFrame(list(cursor))

# lets make a dashboard
app = dash.Dash(__name__)

fig = px.bar(data, x="seasonId", y="numberOfGames")

app.layout = dhtml.Div(
    children=[
        dhtml.H1(children="Number of Games per Season"),
        dhtml.P(children="The number of games in each NHL season prior to 1980",),
        dcc.Graph(figure=fig)
    ]
)

if __name__ == "__main__":
    app.run_server()

