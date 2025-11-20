import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import requests
import plotly.express as px
import pandas as pd

dash.register_page(__name__, name="Clima Global")

# ============================================================
#  1. FUNCIÓN PARA OBTENER LAT/LON DE UNA CIUDAD (GEOCODING)
# ============================================================
def geocode(ciudad):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={ciudad}"

    headers = {
        "User-Agent": "Dash Weather App (contact: ejemplo@example.com)"
    }

    r = requests.get(url, headers=headers)

    # Intentar convertir a JSON
    try:
        data = r.json()
    except Exception:
        return None

    # Si la ciudad no existe o está mal escrita
    if not data:
        return None

    return {
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"]),
        "name": data[0]["display_name"],
    }


# ============================================================
#  2. FUNCIÓN PARA OBTENER CLIMA
# ============================================================
def obtener_clima(lat, lon):
    url_meteo = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly=temperature_2m"
    )

    r = requests.get(url_meteo)
    data = r.json()

    if "hourly" not in data:
        return None

    horas = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    df = pd.DataFrame({
        "Hora": pd.to_datetime(horas),
        "Temperatura (°C)": temps,
    })

    return df


# ============================================================
#  3. LAYOUT (LO QUE SE VE EN LA PÁGINA)
# ============================================================
layout = dbc.Container(
    [
        html.H2("🌍 Clima Global por Ciudad", className="mt-4 mb-3"),

        # Búsqueda
        dbc.Row([
            dbc.Col([
                dbc.Input(
                    id="ciudad-input",
                    placeholder="Escribe una ciudad (ej: Lima, Madrid, Tokyo)",
                    type="text",
                )
            ], md=8),

            dbc.Col([
                dbc.Button("Buscar Clima", id="btn-buscar", color="primary", className="w-100")
            ], md=4)
        ], className="mb-3"),

        html.Div(id="info-ciudad"),

        dbc.Card(
            dbc.CardBody([
                dcc.Loading(
                    dcc.Graph(id="grafico-temp", figure={}),
                    type="circle"
                )
            ]),
            className="mt-3"
        )
    ],
    fluid=True
)


# ============================================================
#  4. CALLBACK
# ============================================================
@dash.callback(
    Output("info-ciudad", "children"),
    Output("grafico-temp", "figure"),
    Input("btn-buscar", "n_clicks"),
    State("ciudad-input", "value"),
)
def actualizar_clima(n_clicks, ciudad_input):
    if not n_clicks or not ciudad_input:
        return "", {}

    # 1️⃣ Obtener lat y lon
    geo = geocode(ciudad_input)
    if geo is None:
        return dbc.Alert("❌ No se encontró la ciudad. Intenta otra.", color="danger"), {}

    lat = geo["lat"]
    lon = geo["lon"]
    name = geo["name"]

    # 2️⃣ Obtener clima
    df = obtener_clima(lat, lon)
    if df is None:
        return dbc.Alert("⚠ No se pudo obtener información del clima.", color="warning"), {}

    # 3️⃣ Crear gráfica
    fig = px.line(
        df,
        x="Hora",
        y="Temperatura (°C)",
        title=f"Temperatura por Hora — {ciudad_input.capitalize()}",
    )
    fig.update_layout(template="simple_white")

    # 4️⃣ Info de la ciudad
    info = dbc.Alert(
        [
            html.H5("📌 Ciudad encontrada:"),
            html.P(name),
            html.P(f"Latitud: {lat:.4f} | Longitud: {lon:.4f}"),
        ],
        color="info"
    )

    return info, fig
