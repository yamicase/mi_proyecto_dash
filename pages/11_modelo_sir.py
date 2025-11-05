import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint
from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(__name__, name='Modelo SIR')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Modelo Epidemiológico SIR", className="card-title text-center mb-4"),

        html.P(
            "Este modelo describe la propagación de una enfermedad dividiendo la población en Susceptibles (S), Infectados (I) y Recuperados (R).",
            className="text-center"
        ),
        html.Hr(),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Sistema de Ecuaciones Diferenciales", className="card-title text-center"),
                html.Img(
                    src=r"https://latex.codecogs.com/svg.latex?\frac{dS}{dt}=-\beta SI,\;\frac{dI}{dt}=\beta SI-\gamma I,\;\frac{dR}{dt}=\gamma I",
                    style={'display': 'block', 'margin': '10px auto', 'height': '60px'}
                )
            ]), style=INFO_CARD_STYLE), md=6),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Interpretación", className="card-title text-center"),
                dcc.Markdown("""
                * **S(t):** Población susceptible.
                * **I(t):** Población infectada.
                * **R(t):** Población recuperada.
                * **β:** Tasa de contagio.
                * **γ:** Tasa de recuperación.
                * **N = S + I + R:** Población total constante.
                """, style={'paddingLeft': '20px'})
            ]), style=INFO_CARD_STYLE), md=6),
        ], className="mb-4"),

        html.Hr(),

        dbc.Row([
            dbc.Col([
                html.H4("Parámetros", className="text-center fw-bold mb-3"),

                dbc.Label("Susceptibles Iniciales (S₀):", className="small"),
                dcc.Input(id='sir-s0', type='number', value=990, min=0,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Infectados Iniciales (I₀):", className="small"),
                dcc.Input(id='sir-i0', type='number', value=10, min=1,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Recuperados Iniciales (R₀):", className="small"),
                dcc.Input(id='sir-r0', type='number', value=0, min=0,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tasa de contagio (β):", className="small"),
                dcc.Input(id='sir-beta', type='number', value=0.002, step=0.001,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tasa de recuperación (γ):", className="small"),
                dcc.Input(id='sir-gamma', type='number', value=0.5, step=0.01,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tiempo máximo (tₘₐₓ):", className="small"),
                dcc.Input(id='sir-tmax', type='number', value=60, min=1, step=1,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                html.Div(id='sir-result', className="text-center fw-bold mt-3 text-primary"),
            ], md=3),

            dbc.Col(dcc.Graph(id='sir-graph', style={'height': '100%'}), md=9),
        ], align="center", className="mt-4"),
    ]),
    className="m-4"
)

layout = html.Div(page_content)


@callback(
    [Output('sir-graph', 'figure'),
     Output('sir-result', 'children')],
    [Input('sir-s0', 'value'),
     Input('sir-i0', 'value'),
     Input('sir-r0', 'value'),
     Input('sir-beta', 'value'),
     Input('sir-gamma', 'value'),
     Input('sir-tmax', 'value')]
)
def update_sir(s0, i0, r0, beta, gamma, tmax):
    if None in (s0, i0, r0, beta, gamma, tmax):
        return dash.no_update, ""

    N = s0 + i0 + r0

    def sir_eq(y, t):
        S, I, R = y
        dSdt = -beta * S * I
        dIdt = beta * S * I - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    t = np.linspace(0, tmax, 400)
    sol = odeint(sir_eq, (s0, i0, r0), t)
    S, I, R = sol.T

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name="Susceptibles"))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name="Infectados"))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name="Recuperados"))

    fig.update_layout(title="Dinámica del Modelo SIR",
                      xaxis_title="Tiempo", yaxis_title="Población",
                      template="plotly_white")

    peak_infected = np.max(I)

    return fig, f"Pico máximo de infectados: {peak_infected:.2f}"
