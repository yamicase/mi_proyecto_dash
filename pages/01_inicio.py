import dash
from dash import html
import dash_bootstrap_components as dbc
from styles import PROFILE_IMAGE_STYLE, INFO_CARD_STYLE

dash.register_page(__name__, name='Sobre Mí')

layout = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col(
                html.Img(src='assets/profile.jpg', style=PROFILE_IMAGE_STYLE),
                md=4,
                className="d-flex align-items-center"
            ),
            dbc.Col(
                [
                    html.H2("Junior Alberto Yanac Minaya", className="card-title"),
                    html.P(
                        "Estudiante de la carrera de Computación Científica en la UNMSM, desarrollador de software con experiencia en desarrollo web y soluciones backend. Me apasiona crear productos digitales que resuelvan problemas reales con código limpio y eficiente.",
                        className="lead"
                    ),
                    html.P(
                        "Tengo experiencia trabajando con tecnologías como JavaScript, Python, Django, MySql, SQL y Git. Siempre estoy en busca de nuevos desafíos que me permitan crecer como profesional y aportar valor a los equipos."
                    ),
                    html.P(
                        "Actualmente me encuentro en Perú, enfocado en mejorar mis habilidades en desarrollo backend y arquitectura de software. Me encanta aprender, colaborar y contribuir a proyectos open source."
                    )
                ],
                md=8,
                className="ps-md-5"
            ),
        ], align="center")
    ]),
    className="m-4",
)
