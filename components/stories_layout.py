from dash import html, dcc
from dash import Input, Output, callback
from components.home_main_layout import create_main_layout
from data_store import processed_data


def create_stories_layout():
    return html.Div(
        className="stores-container",
        children= [
            dcc.Dropdown(['How does war affect the oil and gas industry?', 'DANIEL SIN STORY', 'BAKRI SIN STORY'], 'NYC', id='story-dropdown'),
            html.Div(id='story-area')
        ]
    )

@callback(
    Output('story-area', 'children'),
    Input('story-dropdown', 'value')
)
def update_output(selected_story):
    if selected_story == 'How does war affect the oil and gas industry?':
        return create_war_story()
    
    elif selected_story == 'DANIEL SIN STORY':
        return "hello"
    
    elif selected_story == 'BAKRI SIN STORY':
        return "hello"


def create_war_story():
    return create_main_layout(processed_data)