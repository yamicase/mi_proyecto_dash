import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(__name__, name='Modelo SI')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Modelo Epidemiológico SI", className="card-title text-center mb-4"),

        html.P("Modelo donde la población solo puede estar Susceptible o Infectada. No ocurre recuperación.",
               className="text-center"),
        html.Hr(),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Sistema de Ecuaciones", className="card-title text-center"),
                html.Div(
                    html.Img(src=r"https://latex.codecogs.com/svg.latex?\frac{dS}{dt}=-\beta SI,\;\frac{dI}{dt}=\beta SI",
                             style={'height': '50px', 'display': 'block', 'margin': '10px auto'}),
                ),
            ]), style=INFO_CARD_STYLE), md=6),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Interpretación", className="card-title text-center"),
                dcc.Markdown("""
                * **S(t):** Población susceptible.
                * **I(t):** Población infectada.
                * **β:** Tasa de transmisión.
                """)
            ]), style=INFO_CARD_STYLE), md=6),
        ], className="mb-4"),

        html.Hr(),
        dbc.Row([
            dbc.Col([
                html.H4("Parámetros", className="text-center fw-bold mb-3"),
                
                dbc.Label("Población Inicial Susceptible S₀:", className="small"),
                dcc.Input(id='si-s0', type='number', value=90, min=0, style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Infectados Iniciales I₀:", className="small"),
                dcc.Input(id='si-i0', type='number', value=10, min=1, style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tasa de contagio β:", className="small"),
                dcc.Input(id='si-beta', type='number', value=0.002, step=0.001,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tiempo máximo (tₘₐₓ):", className="small"),
                dcc.Input(id='si-tmax', type='number', value=50, min=1, step=1,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                html.Div(id='si-result', className="text-center fw-bold mt-3 text-primary")
            ], md=3),

            dbc.Col(dcc.Graph(id='si-graph', style={'height': '100%'}), md=9)
        ])
    ]),
    className="m-4"
)

layout = html.Div(page_content)

@callback(
    [Output('si-graph', 'figure'),
     Output('si-result', 'children')],
    [Input('si-s0', 'value'),
     Input('si-i0', 'value'),
     Input('si-beta', 'value'),
     Input('si-tmax', 'value')]
)
def update_si(s0, i0, beta, tmax):
    if None in (s0, i0, beta, tmax):
        return dash.no_update, ""
    
    N = s0 + i0
    t = np.linspace(0, tmax, 300)

    # Solución analítica
    I = (N * i0) / (i0 + (N - i0) * np.exp(-beta * N * t))
    S = N - I

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name="Susceptibles"))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name="Infectados"))

    fig.update_layout(title="Dinámica del Modelo SI", xaxis_title="Tiempo", yaxis_title="Población")
    return fig, f" Infectados finales: I({tmax}) = {I[-1]:.2f}"
