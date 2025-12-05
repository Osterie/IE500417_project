from dash import html, dcc, Input, Output, callback
from stories.war.war_story_layout import create_war_story_layout
from stories.price.price_story_layout import create_price_story_layout
from stories.fn_goals.fn_goals_layout import create_fn_story_layout

def create_stories_layout():
    return html.Div(
        className="stores-container",
        children= [
            html.H1('Please select a story:'),
            dcc.Dropdown(['How does war affect the oil and gas industry?', 'EU\'s progression towards UN sustainability goals', 'BAKRI SIN STORY'], 'How does war affect the oil and gas industry?', id='story-dropdown'),
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
    
    elif selected_story == 'EU\'s progression towards UN sustainability goals':
        return create_fn_story_layout()
    
    elif selected_story == 'BAKRI SIN STORY':
        return create_price_story_layout()