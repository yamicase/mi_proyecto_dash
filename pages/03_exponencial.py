import dash 
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(__name__, name='Modelo Exponencial')

page_content = dbc.Card(
    dbc.CardBody([
        html.H2("Modelo de Crecimiento Exponencial", className="card-title text-center mb-4"),
        html.P(
            "Este modelo describe un proceso donde la tasa de cambio de una cantidad es directamente proporcional a su valor actual. Cuanto más grande es, más rápido crece.",
            className="text-center"
        ),
        html.Hr(),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Ecuación Diferencial", className="card-title text-center"),
                html.Div(
                    html.Img(src=r"https://latex.codecogs.com/svg.latex?\frac{dP}{dt}=rP", 
                             style={'height': '50px', 'display': 'block', 'margin': '10px auto'}),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Solución de la E.D.O.", className="card-title text-center"),
                html.Div(
                    html.Img(src=r"https://latex.codecogs.com/svg.latex?P(t)=P_0e^{rt}", 
                             style={'height': '50px', 'display': 'block', 'margin': '10px auto'}),
                ),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("¿Cuándo se usa?", className="card-title text-center"),
                dcc.Markdown("""
                    * **Finanzas:** Interés compuesto.
                    * **Biología:** Crecimiento de bacterias.
                    * **Epidemiología:** Propagación inicial.
                """, style={'paddingLeft': '20px'}),
            ]), style=INFO_CARD_STYLE), md=6, className="mb-4"),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H5("Puntos Críticos", className="card-title text-center"),
                dcc.Markdown("""
                    * **P = 0:** Único punto de equilibrio, de carácter **inestable**.
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
                        * **r:** Tasa de crecimiento intrínseca.
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
                dcc.Input(id='exp-initial-pop-input', type='number', value=10, min=1, 
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                dbc.Label("Tasa de Crecimiento (r):", className="small"),
                dcc.Input(id='exp-rate-input', type='number', value=0.2, min=0.01, step=0.01, 
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                dbc.Label("Tiempo Final (tₘₐₓ):", className="small"),
                dcc.Input(id='exp-time-max-input', type='number', value=10, min=1, step=0.5, 
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                dbc.Label("Tiempo a Evaluar (t):", className="small"),
                dcc.Input(id='exp-time-input', type='number', value=5, min=0, step=0.1, 
                          style=INPUT_STYLE_COMPACT, className="mb-3"),
                
                html.Div(id='exp-pop-result', className="text-center fw-bold mt-3 text-primary"),
            ], md=3),
            dbc.Col(
                dcc.Graph(id='exponential-graph', style={'height': '100%'}),
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
    [Output('exponential-graph', 'figure'),
     Output('exp-pop-result', 'children')],
    [Input('exp-initial-pop-input', 'value'),
     Input('exp-rate-input', 'value'),
     Input('exp-time-max-input', 'value'),
     Input('exp-time-input', 'value')]
)
def update_exponential_graph(p0, r, t_max, t_eval):
    if p0 is None or r is None or t_max is None or t_eval is None:
        return dash.no_update, ""

    t_eval = min(t_eval, t_max)

    t = np.linspace(0, t_max, 200)
    P = p0 * np.exp(r * t)

    P_eval = p0 * np.exp(r * t_eval)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines',
        line=dict(color='blue', width=2),
        name='Ecuación Exponencial'
    ))

    fig.add_trace(go.Scatter(
        x=[t_eval], y=[P_eval],
        mode='markers+text',
        marker=dict(color='red', size=10),
        text=[f"P({t_eval}) = {P_eval:.2f}"],
        textposition="top center",
        name='Evaluación'
    ))

    fig.update_layout(
        title_text="Crecimiento Exponencial: dP/dt = rP",
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

    return fig, f" Población en t = {t_eval}: P(t) = {P_eval:.2f}"