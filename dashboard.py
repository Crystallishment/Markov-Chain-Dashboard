import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import requests

app = dash.Dash(__name__)

app.layout = html.Div([html.A('← back', href='http://localhost:3000',
       style={'display': 'block', 'margin': '20px', 'fontSize': '16px'}),
                       html.H1('analysis of pages transferal'),
                       dcc.Graph(id='visit-bar'),
                       html.H2('transferal prob for pages'),
                       dcc.Dropdown(id='page-selector'),
                       dcc.Graph(id='prob-pie'),
                       dcc.Interval(id='interval', interval=2000,n_intervals=0) ])


@app.callback(Output('visit-bar', 'figure'),
              Output('page-selector', 'options'),
              Input('interval', 'n_intervals'))

def update_graph(n):
    res = requests.get('http://localhost:8080/results')
    data = res.json()
    if not data:
        return go.Figure(), []

    visit_counts = data['visit_counts']
    fig = go.Figure(go.Bar(
        x=list(visit_counts.keys()),
        y=list(visit_counts.values()),
    ))
    fig.update_layout(title='Page visit counts')
    options = [{'label': k, 'value': k} for k in data['probability_dict'].keys()]
    return fig, options

@app.callback(
    Output('prob-pie', 'figure'),
    Input('page-selector', 'value'),
    prevent_initial_call=True
)


def update_pie(selected_page):
    res = requests.get('http://localhost:8080/results')
    data = res.json()
    if not data or not selected_page:
        return go.Figure()
    probs = data['probability_dict'][selected_page]
    fig = go.Figure(go.Pie(
        labels=list(probs.keys()),
        values=list(probs.values()),
    ))
    fig.update_layout(title=f'{selected_page} visit counts')
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)