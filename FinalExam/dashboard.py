from dash import Dash, html, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import datetime as dt

# create app
app = Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Load data
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"

df = pd.read_csv(URL)

# Layout
app.layout = html.Div(children=[
    # heading
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),

    # Dropdowns
    html.Div([
        # 1st option
        html.H4('Select Report Type: '),
        html.Div(dcc.Dropdown(id='dropdown-statistics', options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics',
                'value': 'Recession Period Statistics'},
        ], placeholder='Select Statistics', style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center', 'inline': True}))
    ]),
    html.Div([
        # 2nd option
        html.H4('Select Report Year: '),
        html.Div(dcc.Dropdown(df.Year.unique(), id='select-year',  placeholder='Select Year', style={
                 'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}))
    ]),

    # Output
    html.Div([
        html.Div(id='output-container', className='chart-grid',
                 style={'display': 'flex'})
    ])
])

# Callback to enable or disable the input container based on the selected statistics


@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(value):
    if value == 'Yearly Statistics':
        return False
    else:
        return True


# callback to plot the output graphs for the respective report types
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='dropdown-statistics', component_property='value'),
        Input(component_id='select-year', component_property='value')
    ]
)
def update_output_container(value_st, value_yr):
    # Filter the data for recession periods
    if value_st == 'Recession Period Statistics':
        data = df[df['Recession'] == 1]

        # Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_rec = data.groupby(
            'Year')['Automobile_Sales'].mean().reset_index()
        R_Chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title=(
                'Automobile sales fluctuate over Recession Period (year wise)'))
        )

        # Plot 2 Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        avg_veh_sold = data.groupby('Vehicle_Type')[
            'Automobile_Sales'].mean().reset_index()
        R_Chart2 = dcc.Graph(figure=px.bar(avg_veh_sold, x='Vehicle_Type', y='Automobile_Sales', title=(
            'Average number of vehicles sold by vehicle type')))

        # Plot 3 : Pie chart for total expenditure share by vehicle type during recessions
        total_exp = data.groupby('Vehicle_Type')[
            'Advertising_Expenditure'].sum().reset_index()
        R_Chart3 = dcc.Graph(figure=px.pie(
            values=total_exp['Advertising_Expenditure'], names=total_exp['Vehicle_Type'], title='Total expenditure share by vehicle type during recessions'))

        # Plot 4 Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        eff = data.groupby('Vehicle_Type')[
            ['unemployment_rate', 'Automobile_Sales']].mean().reset_index()
        R_Chart4 = dcc.Graph(figure=px.bar(eff, x='unemployment_rate', y='Automobile_Sales',
                             color='Vehicle_Type', title=('Effect of unemployment rate on vehicle type and sales')))

        return [
            html.Div(className='chart-grid',
                     children=[html.Div(children=R_Chart1), html.Div(children=R_Chart2)]),
            html.Div(className='chart-grid',
                     children=[html.Div(children=R_Chart3), html.Div(children=R_Chart4)])
        ]
    elif (value_st == 'Yearly Statistics') and (value_yr != ""):
        yearly_data = df[df['Year'] == value_yr]
        print(value_yr)

        # Plot 1 :Yearly Automobile sales using line chart for the whole period.
        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_Chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title=(
                'Yearly Automobile sales'))
        )

        # Plot 2 :Total Monthly Automobile sales using line chart
        monthly_sales = df.groupby(
            'Month')['Automobile_Sales'].sum().reset_index()
        Y_Chart2 = dcc.Graph(
            figure=px.line(monthly_sales, x='Month', y='Automobile_Sales', title=(
                'Total Monthly Automobile sales'))
        )

        # Plot 3: Plot bar chart for average number of vehicles sold during the given year
        b_chart = yearly_data.groupby('Vehicle_Type')[
            'Automobile_Sales'].mean().reset_index()
        Y_Chart3 = dcc.Graph(figure=px.bar(b_chart, x='Vehicle_Type', y='Automobile_Sales', title=(
            f'Average Vehicles Sold by Vehicle Type in the year {value_yr}')))

        # Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
        pie_chart = df.groupby('Vehicle_Type')[
            'Advertising_Expenditure'].sum().reset_index()
        Y_Chart4 = dcc.Graph(figure=px.pie(pie_chart, names='Vehicle_Type', values='Advertising_Expenditure', title=(
            'Total Advertisement Expenditure for each vehicle')))

        return [
            html.Div(className='chart-grid',
                     children=[html.Div(children=Y_Chart1), html.Div(children=Y_Chart2)]),
            html.Div(className='chart-grid',
                     children=[html.Div(children=Y_Chart3), html.Div(children=Y_Chart4)])
        ]


if __name__ == '__main__':
    app.run(debug=True)
