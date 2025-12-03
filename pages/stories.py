import dash
from data_store import processed_data
from components.stories_layout import create_stories_layout

dash.register_page(__name__, path="/stories", name="s5tories")

def layout():
    return create_stories_layout(processed_data)