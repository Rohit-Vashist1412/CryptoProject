import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import no_update
from pycoingecko import CoinGeckoAPI
import pandas as pd
import datetime
import time
from datetime import date

today = date.today() 
startDate = date(2010,1,1)
cg = CoinGeckoAPI()
coins = cg.get_coins()
coin_list = [sublist["id"] for sublist in coins]
currency_list = cg.get_supported_vs_currencies()


app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

app.title = "Crypto Currency Viewer "

app.layout = html.Div(children = [

                html.Div(
                    [html.H1("Crypto Currency Viewer Using PyCoinGecko API", 
                    style ={"text-align":"center"}),
                    
                    html.Div([
                        
                        html.Div([
                                    html.Div([
                                        html.H2("Select Coin", style={'margin-right': '2em'})
                                        ],
                                    ),

                                    dcc.Dropdown(id ="coinid", options = [{'label':i.capitalize().replace("-"," "), 'value':i} for i in coin_list], 
                                    placeholder= "Select a Coin", style ={"width": "70%", 'padding':'3px', 'font-size': '25px', 'text-align-last' : 'center', "position":"relative", "left":"4px", "top":"5px"}),
                                     
                                ], style = {"display":"flex"}),
                        html.Div([
                                    html.Div([
                                        html.H2("Select Currency", style={'margin-right': '2em'})
                                        ],
                                    ),

                                    dcc.Dropdown(id ="currency", options = [{'label':i.upper(), 'value':i} for i in currency_list], 
                                    placeholder= "Select a Currency", style ={"width": "70%", 'padding':'3px', 'font-size': '25px', 'text-align-last' : 'center', "position":"relative", "right":"20px", "top":"5px"}) 
                    ],              style = {"display":"flex"}),
                                    dcc.DatePickerRange(id = "range", min_date_allowed = startDate, max_date_allowed = today, 
                                    initial_visible_month=date(2017, 8, 5), end_date=date(2017, 8, 25) )
                    ]),
                    html.Div([], id='plot')
                    ])
])

@app.callback(
    Output(component_id ="plot", component_property = "children"),
    [Input(component_id = "coinid", component_property = "value"),
    Input(component_id ="currency", component_property = "value"),
    Input(component_id ="range", component_property = "start_date"),
    Input(component_id ="range", component_property = "end_date")
    ],
    )

def getData (coinid , currency, startingDate, endingDate):   
    startingDate = date.fromisoformat(startingDate)
    endingDate = date.fromisoformat(endingDate)
    coin_data = cg.get_coin_market_chart_range_by_id(
    id= coinid, vs_currency= currency, from_timestamp=time.mktime(startingDate.timetuple()), to_timestamp=time.mktime(endingDate.timetuple()))
    price_data = coin_data["prices"]
    price_data = pd.DataFrame(price_data, columns = ["Date", "Price"])
    price_data["Date"] = pd.to_datetime(price_data["Date"], unit ="ms")
    fig = px.line(price_data, x="Date", y="Price", title =f"Price of {coinid.capitalize()} in {currency.upper()}", labels=dict(Date = "Date", Price = f"Price in {currency.upper()}"))
    return dcc.Graph(figure = fig)


if __name__ == "__main__":
    app.run_server(debug =False)