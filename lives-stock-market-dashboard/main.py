from datetime import date, datetime, timedelta
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from plotly import graph_objects
from data_fetching import data_fetching
import plotly.express as px


COLORS = [
    "#1e88e5",
    "#7cb342",
    "#fbc02d",
    "#ab47bc",
    "#26a69a",
    "#5d8aa8",
]



#  Define app 
app = dash.Dash(
    __name__,
    title="Stock Market monitor",
    assets_folder="./assets",
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],

)

stock_option = [{"label": symbol, "value": symbol} for symbol in data_fetching.symbols]



# Define App layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H1("Stock Market Monitor",
                                className="app__header__title"),
                        html.P(
                            "Get the lastest Stock Price by labels",
                            className="app__header__subtitle",
                        ),
                    ],
                    className="app__header__desc",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P("Select a stock symbol"),
                        dcc.Dropdown(
                            id="stock-symbol",
                            searchable=True,
                            multi=True,
                            options=stock_option,
                        )
                    ],
                    className="select_component"
                ),
                html.Div(
                    [
                        html.P("Time Picker"),
                        dcc.DatePickerRange(
                            id='my-date-picker-range',
                            min_date_allowed=date(1995, 8, 5),
                            max_date_allowed=datetime.now(),
                            initial_visible_month=datetime.now(),
                            end_date=datetime.now(),
                            start_date=datetime.now() - timedelta(15),
                            className="date_picker"
                        )
                    ],
                    className="selector_time"
                )
            ],
            className="app__selector",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H6("Current price changes",
                                     className="graph__title")]
                        ),
                        dcc.Graph(id="stock-graph"),
                    ],
                    className="graph",
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H6("Percent changes", className="graph__title")]
                        ),
                        dcc.Graph(id="stock-graph-percent-change"),
                    ],
                    className="graph",
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H6("Volumes",
                                     className="graph__title")]
                        ),
                        dcc.Graph(id="stock-graph-volume"),
                    ],
                    className="graph    ",
                ),
            ],
            className="app__content",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Select a stock symbol To see Company infomation"),
                        dcc.Dropdown(
                            id="stock-symbol-info",
                            searchable=True,
                            options=stock_option
                        )
                    ],
                    className="select_component"
                ),
                html.Div(
                    id="company_info",
                    className="__infomation"
                )
            ],
            className="company_info"
        ),
    ],
    className="app__container",
)



# Define the first callback function to generate the stock price graph
@app.callback(
    Output("stock-graph", "figure"),  # Output component: stock-graph (figure)
    [
        Input("stock-symbol", "value"),  # Input component: stock-symbol (value)
        Input("my-date-picker-range", "start_date"),  # Input component: my-date-picker-range (start_date)
        Input("my-date-picker-range", "end_date"),  # Input component: my-date-picker-range (end_date)
    ],
)
def generate_stock_graph(selected_symbols, start_date: str, end_date: str):
    # Extract the date portion from start_date and end_date
    start_date = start_date.split("T")[0]
    end_date = end_date.split("T")[0]

    # Fetch the close prices for the selected symbols and date range
    df = data_fetching.fetch_close_price(start_date, end_date, selected_symbols)

    # Rename columns if only one symbol is selected
    columns = list(filter(lambda col: col != "Date", list(df.columns)))
    if selected_symbols is not None and len(selected_symbols) == 1:
        df = df.rename(columns={columns[0]: selected_symbols[0]})
        columns = selected_symbols

    # Generate the line graph using Plotly Express
    fig = px.line(df, x="Date", y=columns)

    # Customize the graph layout
    fig.update_layout(
        xaxis={"title": "Time"},
        yaxis={"title": "Price"},
        margin={"l": 70, "b": 70, "t": 70, "r": 70},
        hovermode="closest",
        plot_bgcolor="#282a36",
        paper_bgcolor="#282a36",
        font={"color": "#aaa"},
    )

    # Return the graph figure
    return fig




# Define the second callback function to generate the stock volume graph
@app.callback(
    Output("stock-graph-volume", "figure"),  # Output component: stock-graph-volume (figure)
    [
        Input("stock-symbol", "value"),  # Input component: stock-symbol (value)
        Input("my-date-picker-range", "start_date"),  # Input component: my-date-picker-range (start_date)
        Input("my-date-picker-range", "end_date"),  # Input component: my-date-picker-range (end_date)
    ],
)
def generate_stock_graph_volume(selected_symbols, start_date, end_date):
    # Extract the date portion from start_date and end_date
    start_date = start_date.split("T")[0]
    end_date = end_date.split("T")[0]

    # Fetch the volume data for the selected symbols and date range
    df = data_fetching.fetch_volume(start_date, end_date, selected_symbols)

    # Rename columns if only one symbol is selected
    columns = list(filter(lambda col: col != "Date", list(df.columns)))
    if selected_symbols is not None and len(selected_symbols) == 1:
        df = df.rename(columns={columns[0]: selected_symbols[0]})
        columns = selected_symbols

    # Generate the line graph using Plotly Express
    fig = px.histogram(df, x="Date", y=columns, histfunc="avg", barmode='group')

    # Customize the graph layout
    fig.update_layout(
        xaxis={"title": "Time"},
        yaxis={"title": "Volume"},
        margin={"l": 70, "b": 70, "t": 70, "r": 70},
        hovermode="closest",
        plot_bgcolor="#282a36",
        paper_bgcolor="#282a36",
        font={"color": "#aaa"},
    )

    # Return the graph figure
    return fig



# Define the third callback function to generate the percentage change graph
@app.callback(
    Output("stock-graph-percent-change", "figure"),  # Output component: stock-graph-percent-change (figure)
    [
        Input("stock-symbol", "value"),  # Input component: stock-symbol (value)
        Input("my-date-picker-range", "start_date"),  # Input component: my-date-picker-range (start_date)
        Input("my-date-picker-range", "end_date"),  # Input component: my-date-picker-range (end_date)
    ],
)
def generate_stock_graph_percentage(selected_symbols, start_date, end_date):
    # Extract the date portion from start_date and end_date
    start_date = start_date.split("T")[0]
    end_date = end_date.split("T")[0]

    # Fetch the close prices for the selected symbols and date range
    df = data_fetching.fetch_close_price(start_date, end_date, selected_symbols)

    columns = list(filter(lambda col: col != "Date", list(df.columns)))

    # Rename columns if only one symbol is selected
    if selected_symbols is not None and len(selected_symbols) == 1:
        df = df.rename(columns={columns[0]: selected_symbols[0]})
        columns = selected_symbols

    # Calculate the percentage changes of the stock prices
    df[columns] = df[columns].pct_change().fillna(0)

    # Generate the line graph using Plotly Express
    fig = px.line(df, x="Date", y=columns)

    # Customize the graph layout
    fig.update_layout(
        xaxis={"title": "Time"},
        yaxis={"title": "Percent change"},
        margin={"l": 70, "b": 70, "t": 70, "r": 70},
        hovermode="closest",
        plot_bgcolor="#282a36",
        paper_bgcolor="#282a36",
        font={"color": "#aaa"},
    )

    # Return the graph figure
    return fig






# Define the fourth callback function to display company information
@app.callback(
    Output("company_info", "children"),  # Output component: company_info (children)
    Input("stock-symbol-info", "value")  # Input component: stock-symbol-info (value)
)
def show_company_info(stock):
    if stock is not None:
        # Fetch the information for the selected stock
        data = data_fetching.fetch_info(stock)
        columns = [key for key in data.keys()]

        # Create an HTML layout to display the company information 
        return html.Div(
            [   
                
                html.H3(data["shortName"]),
                html.P(data['longName']),
                html.H4("About"),
                html.P("sector: " + data['sector']),
                html.P(f'{data["longBusinessSummary"]}'),
                
                html.H4("Contacts"),
                html.P(f'Address: {data["address1"]} - {data["city"]} - {data["state"]} - {data["zip"]} - {data["country"]}'),
                html.P(f'Website: {data["website"]}'),
                html.P(f'Fulltime Employees: {data["fullTimeEmployees"]}'),
                html.P(f"Currency: {data['currency']}"),
                html.P(f"Phone: {data['phone']}"),
                
                html.H4("Stock Information"),
                html.P(f"totalRevenue: {data['totalRevenue']}"),
                html.P(f"overallRisk: {data['overallRisk']}"),
                html.P(f"totalDebt: {data['totalDebt']}"),
                html.P(f"volume: {data['volume']}"),
                html.P(f"Open: {data['regularMarketOpen']}"),
                html.P(f"High: {data['regularMarketDayHigh']}"),
                html.P(f"Currency: {data['currency']}"),
                html.P(f"quickRatio: {data['quickRatio']}"),
                html.P(f"recommendationMean: {data['recommendationMean']}"),
                html.P(f"dayHigh: {data['dayHigh']}"),
                html.P(f"dayLow: {data['dayLow']}"),
                html.P(f"totalCashPerShare: {data['totalCashPerShare']}"),
                html.P(f"profitMargins: {data['profitMargins']}")
                

            ]
        )
    return 
    


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
