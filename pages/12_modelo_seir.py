import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint
from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(__name__, name='Modelo SEIR')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Modelo Epidemiológico SEIR", className="card-title text-center mb-4"),

        html.P(
            "El modelo SEIR incorpora una fase de incubación donde los individuos expuestos aún no transmiten la enfermedad.",
            className="text-center"
        ),
        html.Hr(),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Sistema de Ecuaciones Diferenciales", className="card-title text-center"),
                html.Img(
                    src=r"https://latex.codecogs.com/svg.latex?\frac{dS}{dt}=-\beta SI,\;\frac{dE}{dt}=\beta SI-\sigma E,\;\frac{dI}{dt}=\sigma E-\gamma I,\;\frac{dR}{dt}=\gamma I",
                    style={'display': 'block', 'margin': '10px auto', 'height': '65px'}
                )
            ]), style=INFO_CARD_STYLE), md=6),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Interpretación de Variables", className="card-title text-center"),
                dcc.Markdown("""
                * **S(t):** Susceptibles.
                * **E(t):** Expuestos (infectados pero sin contagiar).
                * **I(t):** Infectados capaces de contagiar.
                * **R(t):** Recuperados o inmunes.
                * **β:** Tasa de contagio.
                * **σ:** Tasa de progresión de expuesto a infectado (1/periodo de incubación).
                * **γ:** Tasa de recuperación.
                """, style={'paddingLeft': '20px'})
            ]), style=INFO_CARD_STYLE), md=6),
        ], className="mb-4"),

        html.Hr(),

        dbc.Row([
            dbc.Col([
                html.H4("Parámetros", className="text-center fw-bold mb-3"),

                dbc.Label("Susceptibles Iniciales (S₀):", className="small"),
                dcc.Input(id='seir-s0', type='number', value=990, min=0,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Expuestos Iniciales (E₀):", className="small"),
                dcc.Input(id='seir-e0', type='number', value=5, min=0,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Infectados Iniciales (I₀):", className="small"),
                dcc.Input(id='seir-i0', type='number', value=5, min=0,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Recuperados Iniciales (R₀):", className="small"),
                dcc.Input(id='seir-r0', type='number', value=0, min=0,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tasa de contagio (β):", className="small"),
                dcc.Input(id='seir-beta', type='number', value=0.002, step=0.001,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tasa de incubación (σ):", className="small"),
                dcc.Input(id='seir-sigma', type='number', value=0.3, step=0.01,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tasa de recuperación (γ):", className="small"),
                dcc.Input(id='seir-gamma', type='number', value=0.5, step=0.01,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tiempo máximo (tₘₐₓ):", className="small"),
                dcc.Input(id='seir-tmax', type='number', value=80, min=1, step=1,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                html.Div(id='seir-result', className="text-center fw-bold mt-3 text-primary"),
            ], md=3),

            dbc.Col(dcc.Graph(id='seir-graph', style={'height': '100%'}), md=9),
        ], align="center", className="mt-4"),
    ]),
    className="m-4"
)

layout = html.Div(page_content)


@callback(
    [Output('seir-graph', 'figure'),
     Output('seir-result', 'children')],
    [Input('seir-s0', 'value'),
     Input('seir-e0', 'value'),
     Input('seir-i0', 'value'),
     Input('seir-r0', 'value'),
     Input('seir-beta', 'value'),
     Input('seir-sigma', 'value'),
     Input('seir-gamma', 'value'),
     Input('seir-tmax', 'value')]
)
def update_seir(s0, e0, i0, r0, beta, sigma, gamma, tmax):
    if None in (s0, e0, i0, r0, beta, sigma, gamma, tmax):
        return dash.no_update, ""

    N = s0 + e0 + i0 + r0

    def seir_eq(y, t):
        S, E, I, R = y
        dSdt = -beta * S * I
        dEdt = beta * S * I - sigma * E
        dIdt = sigma * E - gamma * I
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt

    t = np.linspace(0, tmax, 500)
    sol = odeint(seir_eq, (s0, e0, i0, r0), t)
    S, E, I, R = sol.T

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name="Susceptibles"))
    fig.add_trace(go.Scatter(x=t, y=E, mode='lines', name="Expuestos"))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name="Infectados"))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name="Recuperados"))

    fig.update_layout(
        title="Dinámica del Modelo SEIR",
        xaxis_title="Tiempo",
        yaxis_title="Población",
        template="plotly_white"
    )

    peak_infected = np.max(I)
    peak_time = t[np.argmax(I)]

    return fig, f"Pico de infectados: {peak_infected:.2f} en t ≈ {peak_time:.2f}"
