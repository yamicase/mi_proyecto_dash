import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import requests

from styles import INFO_CARD_STYLE

dash.register_page(__name__, name='Clima – API Pública')

PAISES = {
    "Perú (Lima)": (-12.0464, -77.0428),
    "México (CDMX)": (19.4326, -99.1332),
    "Argentina (Buenos Aires)": (-34.6037, -58.3816),
    "España (Madrid)": (40.4168, -3.7038),
    "Japón (Tokio)": (35.6895, 139.6917),
}

layout = dbc.Container([
    html.H2("Clima ", className="text-center mt-4 mb-4"),

    dbc.Row([
        dbc.Col([
            html.H4("PARÁMETROS", className="fw-bold"),

            dbc.Label("Seleccionar país:"),
            dcc.Dropdown(
                id="pais_selector",
                options=[{"label": k, "value": k} for k in PAISES.keys()],
                value="Perú (Lima)",
                className="mb-4",
                style={"fontSize": "18px"}
            ),

            html.Div(id="clima-actual", className="mt-4"),

        ], md=3),

        dbc.Col([
            dcc.Graph(id="grafico_clima", style={"height": "600px"})
        ], md=9)
    ])
], fluid=True)

@callback(
    [Output('clima-actual', 'children'),
     Output('grafico_clima', 'figure')],
    Input('pais_selector', 'value')
)
def actualizar_clima(pais):
    lat, lon = PAISES[pais]

    url_actual = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )

    actual = requests.get(url_actual).json()["current_weather"]

    info = html.Div([
        html.P(f" Temperatura: {actual['temperature']} °C"),
        html.P(f" Viento: {actual['windspeed']} km/h"),
        html.P(f" Dirección del viento: {actual['winddirection']}°"),
        html.P(f" Código del clima: {actual['weathercode']}"),
    ])

    url_horas = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m"
        f"&forecast_days=1"
        f"&timezone=auto"
    )

    data = requests.get(url_horas).json()["hourly"]

    df = pd.DataFrame({
        "Hora": data["time"],
        "Temp": data["temperature_2m"]
    })

    # Convertir a datetime
    df["Hora"] = pd.to_datetime(df["Hora"])
    df["HoraStr"] = df["Hora"].dt.strftime("%H:%M")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["HoraStr"],
        y=df["Temp"],
        mode='lines+markers',
        name='Temperatura (°C)',
        line=dict(width=3)
    ))

    fig.update_layout(
        title=f"Temperatura por Hora – {pais}",
        title_x=0.5,
        xaxis_title="Hora del día",
        yaxis_title="Temperatura (°C)",
        template="plotly_white",
        height=600,
        font=dict(family="Outfit, sans-serif"),
        plot_bgcolor="lightblue",
        margin=dict(l=40, r=20, t=60, b=40),
    )

    return info, fig
