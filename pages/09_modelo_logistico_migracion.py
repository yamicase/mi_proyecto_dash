import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(__name__, name='Modelo Logístico con Migración')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Modelo de Crecimiento Logístico con Migración", className="card-title text-center mb-4"),
        html.P(
            "Este modelo amplía el modelo logístico clásico incorporando un término de migración constante (M), "
            "que representa el flujo neto de individuos hacia o desde la población. Si M > 0, hay inmigración; si M < 0, hay emigración.",
            className="text-center"
        ),
        html.Hr(),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Ecuación Diferencial", className="card-title text-center"),
                html.Div(
                    html.Img(src=r"https://latex.codecogs.com/svg.latex?\frac{dP}{dt}=rP(1-\frac{P}{K})+M", 
                             style={'height': '60px', 'display': 'block', 'margin': '10px auto'})
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Solución", className="card-title text-center"),
                html.Div(
                    html.P(
                        "No existe una solución analítica cerrada para este modelo. "
                        "Se resuelve mediante integración numérica (método de Euler).",
                        className="text-center", style={'padding': '10px'}
                    )
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("¿Cuándo se usa?", className="card-title text-center"),
                dcc.Markdown("""
                    * **Ecología:** Especies con migración o flujo constante.  
                    * **Sociología:** Crecimiento poblacional urbano con migración neta.  
                    * **Epidemiología:** Movimientos de población entre regiones.
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Puntos de Equilibrio", className="card-title text-center"),
                dcc.Markdown("""
                    * Se obtiene resolviendo **rP(1 - P/K) + M = 0**.  
                    * Si M > 0, la población puede superar K.  
                    * Si M < 0, la población puede caer por debajo de K.
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),

        dbc.Row([
            dbc.Col(
                dbc.Card(dbc.CardBody([
                    html.H5("Descripción de Variables", className="card-title text-center"),
                    dcc.Markdown("""
                        * **P(t):** Población en el tiempo t.  
                        * **P₀:** Población inicial (en t=0).  
                        * **K:** Capacidad de carga del sistema.  
                        * **r:** Tasa de crecimiento intrínseca.  
                        * **M:** Migración neta (positiva o negativa).  
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
                dcc.Input(id='logmig-initial-pop-input', type='number', value=20, min=1, 
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tasa de Crecimiento (r):", className="small"),
                dcc.Input(id='logmig-rate-input', type='number', value=0.15, min=0.01, step=0.01, 
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Capacidad de Carga (K):", className="small"),
                dcc.Input(id='logmig-capacity-input', type='number', value=150, min=10, 
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Migración (M):", className="small"),
                dcc.Input(id='logmig-migration-input', type='number', value=5, step=0.1, 
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tiempo Final (tₘₐₓ):", className="small"),
                dcc.Input(id='logmig-time-max-input', type='number', value=60, min=1, step=0.5, 
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                dbc.Label("Tiempo a Evaluar (t):", className="small"),
                dcc.Input(id='logmig-time-input', type='number', value=20, min=0, step=0.5, 
                          style=INPUT_STYLE_COMPACT, className="mb-3"),

                html.Div(id='logmig-pop-result', className="text-center fw-bold mt-3 text-primary"),
            ], md=3),

            dbc.Col(
                dcc.Graph(id='logistic-migration-graph', style={'height': '100%'}),
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
    html.Div(
        page_content,
        style={'fontFamily': 'Outfit, sans-serif'}
    )
])

@callback(
    [Output('logistic-migration-graph', 'figure'),
     Output('logmig-pop-result', 'children')],
    [Input('logmig-initial-pop-input', 'value'),
     Input('logmig-rate-input', 'value'),
     Input('logmig-capacity-input', 'value'),
     Input('logmig-migration-input', 'value'),
     Input('logmig-time-max-input', 'value'),
     Input('logmig-time-input', 'value')]
)
def update_logistic_migration_graph(p0, r, k, m, t_max, t_eval):
    if None in (p0, r, k, m, t_max, t_eval):
        return dash.no_update, ""

    t_eval = min(t_eval, t_max)
    dt = 0.1
    n_steps = int(t_max / dt)
    t = np.linspace(0, t_max, n_steps)
    P = np.zeros(n_steps)
    P[0] = p0

    for i in range(1, n_steps):
        dPdt = r * P[i-1] * (1 - P[i-1] / k) + m
        P[i] = P[i-1] + dPdt * dt
        if P[i] < 0:
            P[i] = 0

    idx_eval = int(t_eval / dt)
    P_eval = P[idx_eval] if idx_eval < len(P) else P[-1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines',
        line=dict(color='blue', width=2),
        name='Ecuación Logística con Migración'
    ))

    fig.add_trace(go.Scatter(
        x=[0, t_max], y=[k, k],
        mode='lines', line=dict(color='red', width=2, dash='dash'),
        name='Capacidad de carga (K)'
    ))

    fig.add_trace(go.Scatter(
        x=[t_eval], y=[P_eval],
        mode='markers+text',
        marker=dict(color='green', size=10),
        text=[f"P({t_eval}) = {P_eval:.2f}"],
        textposition="top center",
        name='Evaluación'
    ))

    fig.update_layout(
        title_text="Crecimiento Logístico con Migración: dP/dt = rP(1 - P/K) + M",
        title_x=0.5,
        xaxis_title="Tiempo (t)",
        yaxis_title="Población (P)",
        template="plotly_white",
        height=550,
        font=dict(family="Outfit, sans-serif"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=20, t=60, b=40),
        plot_bgcolor='lightblue'
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='red', gridcolor='lightgray', range=[0, t_max])
    fig.update_yaxes(showline=True, linewidth=2, linecolor='red', gridcolor='lightgray')

    return fig, f"Población en t = {t_eval}: P(t) = {P_eval:.2f}"
