from dash import html, dcc, Input, Output, callback
from stories.war.war_story_layout import create_war_story_layout

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
        return create_war_story_layout()
    
    elif selected_story == 'DANIEL SIN STORY':
        return "hello"
    
    elif selected_story == 'BAKRI SIN STORY':
        return "hello"
