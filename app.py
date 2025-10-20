import dash
import dash_bootstrap_components as dbc
from dash import html
from styles import NAV_LINK_STYLE

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True
)
server = app.server

header = html.Div([
    html.Div(
        html.H2("Técnicas de Modelamiento Matemático", className="text-white text-center p-3"),
        style={'backgroundColor': '#E25822'}
    ),
    html.Div(
        [
            dbc.NavLink(
                page['name'],
                href=page['relative_path'],
                style=NAV_LINK_STYLE,
                className="shadow-sm"
            )
            for page in dash.page_registry.values()
        ],
        className="d-flex justify-content-center p-2",
        style={'backgroundColor': '#E25822', 'borderTop': '2px solid white'}
    )
], className="mb-4 shadow")

app.layout = html.Div([
    header,
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=False)
