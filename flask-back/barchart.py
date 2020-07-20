import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
app =dash.Dash(
    __name__,server=server,
    routes_pathname_prefix='/dash/'
)
data = pd.read_csv("https://people.sc.fsu.edu/~jburkardt/data/csv/hooke.csv",sep=',')
t1 = data[' "Spring 1 (m)"']
t2= data[' "Spring 2 (m)"']
x = data['Index']

df = pd.DataFrame({"Index": x, "Spring 1": t1, "Spring 2": t2})

fig = px.bar(df, x="Index", y=["Spring 1","Spring 2"], barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

