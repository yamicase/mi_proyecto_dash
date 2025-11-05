import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True
)
server = app.server

toggle_btn = html.Button("☰", id="toggle-btn", className="toggle-btn")

sidebar = html.Div(
    [
        html.H4("Modelamiento", className="text-white text-center mb-4"),
        html.Div(
            [
                dbc.NavLink(page['name'], href=page['relative_path'], className="sidebar-link")
                for page in dash.page_registry.values()
            ],
            className="d-flex flex-column"
        )
    ],
    id="sidebar",
    className="sidebar"
)

content = html.Div(
    [toggle_btn, dash.page_container],
    id="content",
    className="content-area"
)

app.layout = html.Div([sidebar, content])


@app.callback(
    Output("sidebar", "className"),
    Output("content", "className"),
    Input("toggle-btn", "n_clicks"),
    prevent_initial_call=True
)
def toggle_sidebar(n):
    if n and n % 2 == 1:
        return "sidebar collapsed", "content-area expanded"
    return "sidebar", "content-area"


if __name__ == "__main__":
    app.run(debug=True)
