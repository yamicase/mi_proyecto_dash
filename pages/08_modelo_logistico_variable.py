import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(__name__, name='Modelo Logístico Variable')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Modelo Logístico con Tasa Variable", className="card-title text-center mb-4"),
        html.P(
            "Este modelo extiende el modelo logístico clásico incorporando una tasa de crecimiento r(t) que varía con el tiempo. "
            "Esto permite representar entornos donde las condiciones cambian, como disponibilidad de recursos o estacionalidad.",
            className="text-center"
        ),
        html.Hr(),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Ecuación Diferencial", className="card-title text-center"),
                html.Div(
                    html.Img(src=r"https://latex.codecogs.com/svg.latex?\frac{dP}{dt}=r(t)P(1-\frac{P}{K})",
                             style={'height': '55px', 'display': 'block', 'margin': '10px auto'}),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Ejemplo de r(t)", className="card-title text-center"),
                html.Div(
                    html.Img(src=r"https://latex.codecogs.com/svg.latex?r(t)=r_0(1+\alpha\sin(\omega t))",
                             style={'height': '50px', 'display': 'block', 'margin': '10px auto'}),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("¿Cuándo se usa?", className="card-title text-center"),
                dcc.Markdown("""
                    * **Ecología:** Cuando el ambiente cambia estacionalmente.  
                    * **Economía:** Crecimiento de mercados con ciclos.  
                    * **Epidemiología:** Contagio con variaciones de transmisión.
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Puntos Clave", className="card-title text-center"),
                dcc.Markdown("""
                    * Si r(t) > 0 en promedio, la población crece.  
                    * Si r(t) < 0 prolongadamente, la población decae.  
                    * El equilibrio **P = K** sigue siendo estable.
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card(dbc.CardBody([
                    html.H5("Descripción de Variables", className="card-title text-center"),
                    dcc.Markdown("""
                        * **P(t):** Población en el tiempo t.  
                        * **P₀:** Población inicial.  
                        * **K:** Capacidad de carga.  
                        * **r₀:** Tasa base de crecimiento.  
                        * **α:** Amplitud de variación.  
                        * **ω:** Frecuencia de cambio.  
                        * **t:** Tiempo.
                    """, style={'paddingLeft': '20px'})
                ]), style=INFO_CARD_STYLE)
            ),
        ], className="mb-4"),

        html.Hr(className="my-4"),

        dbc.Row([
            dbc.Col([
                html.H4("Parámetros", className="text-center fw-bold mb-3"),

                dbc.Label("Población Inicial (P₀):", className="small"),
                dcc.Input(id='logvar-p0', type='number', value=10, min=1,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Capacidad de Carga (K):", className="small"),
                dcc.Input(id='logvar-k', type='number', value=150, min=10,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tasa Base (r₀):", className="small"),
                dcc.Input(id='logvar-r0', type='number', value=0.15, min=0.01, step=0.01,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Amplitud (α):", className="small"),
                dcc.Input(id='logvar-alpha', type='number', value=0.5, min=0, max=1, step=0.05,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Frecuencia (ω):", className="small"),
                dcc.Input(id='logvar-omega', type='number', value=0.2, min=0, step=0.05,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tiempo Final (tₘₐₓ):", className="small"),
                dcc.Input(id='logvar-tmax', type='number', value=60, min=10, step=1,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tiempo a Evaluar (t):", className="small"),
                dcc.Input(id='logvar-teval', type='number', value=20, min=0, step=0.5,
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                html.Div(id='logvar-result', className="text-center fw-bold mt-3 text-primary"),
            ], md=3),

            dbc.Col(
                dcc.Graph(id='logvar-graph', style={'height': '100%'}),
                md=9
            ),
        ], align="center", className="mt-4"),
    ]),
    className="m-4",
)

layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap'
    ),
    html.Div(page_content, style={'fontFamily': 'Outfit, sans-serif'})
])

@callback(
    [Output('logvar-graph', 'figure'),
     Output('logvar-result', 'children')],
    [Input('logvar-p0', 'value'),
     Input('logvar-k', 'value'),
     Input('logvar-r0', 'value'),
     Input('logvar-alpha', 'value'),
     Input('logvar-omega', 'value'),
     Input('logvar-tmax', 'value'),
     Input('logvar-teval', 'value')]
)
def update_variable_logistic(p0, k, r0, alpha, omega, tmax, teval):
    if None in [p0, k, r0, alpha, omega, tmax, teval]:
        return dash.no_update, ""

    if p0 >= k:
        p0 = k / 2

    teval = min(teval, tmax)

    t = np.linspace(0, tmax, 400)
    r_t = r0 * (1 + alpha * np.sin(omega * t))

    dt = t[1] - t[0]
    P = np.zeros_like(t)
    P[0] = p0
    for i in range(1, len(t)):
        dP = r_t[i-1] * P[i-1] * (1 - P[i-1] / k)
        P[i] = P[i-1] + dP * dt

    P_eval = np.interp(teval, t, P)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines', line=dict(color='blue', width=2),
        name='Población P(t)'
    ))

    fig.add_trace(go.Scatter(
        x=[0, tmax], y=[k, k], mode='lines',
        line=dict(color='red', dash='dash', width=2),
        name='Capacidad de carga (K)'
    ))

    fig.add_trace(go.Scatter(
        x=t, y=r_t * 20, mode='lines',
        line=dict(color='green', dash='dot', width=1.5),
        name='r(t) (escala 20×)'
    ))

    fig.add_trace(go.Scatter(
        x=[teval], y=[P_eval],
        mode='markers+text',
        marker=dict(color='darkgreen', size=10),
        text=[f"P({teval}) = {P_eval:.2f}"],
        textposition="top center",
        name='Evaluación'
    ))

    fig.update_layout(
        title_text="Crecimiento Logístico con r(t) Variable",
        title_x=0.5,
        xaxis_title="Tiempo (t)",
        yaxis_title="Población (P)",
        template="plotly_white",
        height=550,
        font=dict(family="Outfit, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=60, b=40),
        plot_bgcolor='lightblue'
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='red', gridcolor='lightgray', range=[0, tmax])
    fig.update_yaxes(showline=True, linewidth=2, linecolor='red', gridcolor='lightgray')

    return fig, f"Población en t = {teval}: P(t) = {P_eval:.2f}"
