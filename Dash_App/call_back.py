from dash import Dash, html, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

app = Dash(__name__)

# Read the airline data into pandas dataframe
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                           encoding="ISO-8859-1", dtype={'Div1Airport': str, 'Div1TailNum': str, 'Div2Airport': str, 'Div2TailNum': str})

# Layout
app.layout = html.Div(children=[
    html.H1('Airline Performance Dashboard', style={
            'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Div(["Input Year: ", dcc.Input(id='input-year', value=2010, type='number',
             style={'height': '40px', 'font-size': 25}), ], style={'color': 'red'}),
    html.Br(),
    html.Br(),
    html.Div(dcc.Graph(id='line-plot')),
    html.Div(dcc.Graph(id='bar-plot'))
])

# add callback decorator


@app.callback(
    Output(component_id='line-plot', component_property='figure'),
    Input(component_id='input-year', component_property='value')
)
# Add computation to callback function and return graph
def get_graph(entered_year):
    # select data
    df = airline_data[airline_data['Year'] == int(entered_year)]

    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    fig = px.line(data_frame=line_data, x=line_data['Month'], y=line_data['ArrDelay'], markers=dict(
        color='green'), title="Month vs Average Flight Delay Time")

    return fig


@app.callback(
    Output(component_id='bar-plot', component_property='figure'),
    Input(component_id='input-year', component_property='value')
)
# Add computation to callback function and return graph
def get_graph2(entered_year):
    # select data
    df = airline_data[airline_data['Year'] == int(entered_year)]

    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    fig_bar = px.bar(data_frame=line_data,
                     x=line_data['Month'], y=line_data['ArrDelay'], title='Bar Chart')

    return fig_bar


if __name__ == '__main__':
    app.run(debug=True)
