# importing

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from flask import Flask
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# initiating the app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[
                dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# read the files
df = pd.read_csv('count.csv')
df1 = pd.read_csv('speed.csv')

# Build the components
Header_component = html.H1(
    "Traffic Analysis Dashboard", style={'color': 'darkcyan', 'text-align': 'center'})

# Visual Components

# Component1

countfig = go.FigureWidget()

countfig.add_scatter(
    name="Bus", x=df["Bus"], y=df["Time"].sort_values(), fill="tonexty", line_shape='spline')

countfig.add_scatter(
    name="Car", x=df["Car"], y=df["Time"].sort_values(), fill="tonexty", line_shape='spline')

countfig.update_layout(title="Vehicle Time Line")


# Component2

countfig_cum = go.FigureWidget()

countfig_cum.add_scatter(
    name="Bus", x=df["Bus"].cumsum(), y=df["Time"].sort_values(), fill="tonexty", line_shape='spline')

countfig_cum.add_scatter(
    name="Car", x=df["Car"].cumsum(), y=df["Time"].sort_values(), fill="tonexty", line_shape='spline')

countfig_cum.update_layout(title="Cummulative Traffic")

# Component3

indicator = go.FigureWidget(go.Indicator(
    mode="gauge+number",
    value=df1["Car"].mean(),
    title={'text': 'Speed km/hr'},
))
indicator.update_layout(title="Average Car speed")

# Component4

indicator1 = go.FigureWidget(go.Indicator(
    mode="gauge+number",
    value=df1["Bus"].mean(),
    title={'text': 'Speed km/hr'},
    gauge={"bar": {"color": "cyan"}}
))
indicator1.update_layout(title="Average Bus speed")

# Component5

piefig = go.FigureWidget(px.pie(labels=['Car', 'Bus'], values=[
                         df['Car'].sum(), df["Bus"].sum()],
    hole=0.4))
piefig.update_layout(title="Traffic Distribution")

# Design the components
app.layout = html.Div(
    [
        dbc.Row([Header_component]),
        dbc.Row(
            [dbc.Col(
                [dcc.Graph(figure=countfig)]), dbc.Col(dcc.Graph(figure=countfig_cum))]
        ),
        dbc.Row(
            [dbc.Col(dcc.Graph(figure=indicator)), dbc.Col(
                dcc.Graph(figure=indicator1)), dbc.Col(dcc.Graph(figure=piefig))]
        ),
    ]
)

# Run the app
app.run_server(debug=True)
