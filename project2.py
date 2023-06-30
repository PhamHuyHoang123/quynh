import dash
from dash import html as html
from dash import dcc as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


#getting the dataset

pro = pd.read_csv('https://raw.githubusercontent.com/PhamHuyHoang123/quynh/main/Employee-Attrition.csv')

#dash app

app = dash.Dash()
server = app.server
#layout
app.layout = html.Div(children = [
    html.Div([
        html.H1(children = 'Analysis of employee attrition',
                style={'text-align': 'center', 'font-size': '36px', 'color': '#333333', 'margin': '10px'})
    ], style={'background-color': '#f8f9fa', 'padding': '20px'}),
    html.Div([
        html.Div([
            dcc.Checklist(
                id = 'geo-checklist',
                options = [{'label': i, 'value': i}
                           for i in pro['Department'].unique()],
                value = ["Sales"],
                labelStyle={'display': 'block', 'margin': '10px'}
            ),
            dcc.Graph(id = 'price-graph'),
            dcc.RangeSlider(
                id='range-slider',
                min=pro['YearsInCurrentRole'].min(),
                max=pro['YearsInCurrentRole'].max(),
                step=1,
                value=[pro['YearsInCurrentRole'].min(), pro['YearsInCurrentRole'].max()],
                marks={str(i): str(i) for i in range(pro['YearsInCurrentRole'].min(), pro['YearsInCurrentRole'].max()+1, 1)}
            )
        ], className='six columns', style={'border': '1px solid #ced4da', 'border-radius': '5px', 'margin': '10px'}),
        html.Div([
            dcc.Graph(id = 'bar-chart')
        ], className='six columns', style={'border': '1px solid #ced4da', 'border-radius': '5px', 'margin': '10px'})
    ], className='row')])

@app.callback(
    Output(component_id = 'price-graph', component_property ='figure'),
    Input(component_id = 'geo-checklist', component_property = 'value'),
    Input(component_id = 'range-slider', component_property = 'value')
)
def update_scatter(selected_departments, selected_range):
    data = pro[(pro['Department'].isin(selected_departments)) & (pro['YearsInCurrentRole'] >= selected_range[0]) & (pro['YearsInCurrentRole'] <= selected_range[1])]
    graph = px.scatter(data, x ='YearsInCurrentRole', y = 'YearsAtCompany', color='Attrition')
    return graph

@app.callback(
    Output(component_id = 'bar-chart', component_property ='figure'),
    Input(component_id = 'geo-checklist', component_property = 'value')
)
def update_bar(selected_departments):
    data = pro[pro['Department'].isin(selected_departments)]
    bar = px.histogram(data, x ='MonthlyIncome', nbins=30)
    return bar

if __name__ == '__main__':
    app.run_server(debug = True)

