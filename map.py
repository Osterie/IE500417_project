from data_store import processed_data_only_countries
from dash import html, dcc, callback, Output, Input, State
import plotly.express as px
from dash.exceptions import PreventUpdate
import numpy as np

def create_ghg_layout():

    min_year=processed_data_only_countries['year'].min()
    max_year=processed_data_only_countries['year'].max()

    layout = html.Div([
        html.H1(id ='map-title', children='Y-axis attribute visualized', style={'textAlign':'center'}),
        
        html.Div([
            html.H2("Color Scale:"),
            dcc.RadioItems(
                id="scale-type",
                options=[
                    {"label": "Linear", "value": "linear"},
                    {"label": "Logarithmic", "value": "log"}
                ],
                value="linear",
                inline=True
            )
        ]),

        dcc.Graph(id='ghg-map'),

        html.Div([
            html.Label("Select Year:"),
            dcc.Slider(
                id='year-slider',
                min=min_year,
                max=max_year,
                value=max_year,
                marks=None,
                step=1,
                tooltip={"placement": "bottom", "always_visible": True},
            ),
            
            html.Button("Play", id="play-button", n_clicks=0),

            dcc.Interval(
                id='interval-component',
                interval=200,
                n_intervals=0,
                disabled=True
            ),
            dcc.Store(id="is-playing", data=False),

        ])
    ])
    return layout

@callback(
    Output('map-title', 'children'),
    Input('dropdown-selection-y', 'value')
)
def update_map_title(y_attr):
    if (y_attr is None) or (y_attr in ["country", "year"]):
        return "Y-axis attribute visualized"
    return f"Visualization of {y_attr} across countries (based on attribute selected on Y-axis)"


@callback(
    Output('ghg-map', 'figure'),
    Input('year-slider', 'value'),
    Input('dropdown-selection-y', 'value'),
    Input('scale-type', 'value'),
)
def update_map(selected_year, y_attr, scale_type):

    if (y_attr is None) or (y_attr in ["country", "year"]):
        raise PreventUpdate
    
    filtered_df = processed_data_only_countries[processed_data_only_countries['year'] == selected_year].copy()
    filtered_df = filtered_df[filtered_df[y_attr] > 0]
    
    if scale_type == "log":
        filtered_df['log_color'] = np.log10(filtered_df[y_attr])
        color_col = 'log_color'

        cmin = filtered_df['log_color'].min()
        cmax = filtered_df['log_color'].max()
        tickvals = np.linspace(cmin, cmax, num=5)
        ticktext = [f"{int(10**v):,}" for v in tickvals]

        colorbar_dict = dict(
            title=y_attr,
            tickvals=tickvals,
            ticktext=ticktext
        )
    else:
        color_col = y_attr
        colorbar_dict = dict(title=y_attr)

    fig = px.choropleth(
        filtered_df,
        locations="country",
        locationmode='country names',
        color=color_col,
        hover_name='country',
        projection='natural earth',
        title=f"{y_attr} ({scale_type} scale) in {selected_year}",
    )

    fig.update_traces(
        customdata=filtered_df[y_attr],
        hovertemplate="%{hovertext}<br>Value: %{customdata}"
    )

    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor="white",
            showcountries=True,
            countrycolor="Black"
        ),
        uirevision='keep-zoom',
        coloraxis_colorbar=colorbar_dict
    )

    return fig


@callback(
    Output("is-playing", "data"),
    Output("play-button", "children"),
    Input("play-button", "n_clicks"),
    State("is-playing", "data")
)
def toggle_play(n_clicks, is_playing):
    if n_clicks == 0:
        return False, "Play"
    return not is_playing, "Pause" if not is_playing else "Play"

@callback(
    Output("interval-component", "disabled"),
    Input("is-playing", "data")
)
def enable_interval(is_playing):
    return not is_playing


@callback(
    Output("year-slider", "value"),
    Input("interval-component", "n_intervals"),
    State("year-slider", "value"),
    State("year-slider", "max"),
    State("is-playing", "data")
)
def advance_year(n_intervals, current_value, slider_max, is_playing):
    if not is_playing:
        return current_value
    
    if current_value >= slider_max:
        return slider_max

    return current_value + 1
