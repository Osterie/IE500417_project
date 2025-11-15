from dash import Input, Output, callback

def register_slider_callbacks():

    @callback(
        Output('slider-container', 'style'),
        Input('dropdown-selection-x', 'value')
    )
    def toggle_slider(x_attr):
        if x_attr == 'year':
            return {"display": "block"}
        else:
            return {"display": "none"}