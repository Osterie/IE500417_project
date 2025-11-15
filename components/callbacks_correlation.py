from dash import Input, Output, callback, dash_table
from dash.exceptions import PreventUpdate


def register_correlation_callbacks(processed_data):

    @callback(
        Output('correlation-output', 'style'),
        Output('correlation-button', 'children'),
        Input('correlation-button', 'n_clicks'),
    )
    def show_hide_correlation_output(n_clicks):
        if n_clicks is None or n_clicks == 0:
            raise PreventUpdate

        if n_clicks % 2 == 1:
            return {"display": "block"}, "Hide Correlation"
        else:
            return {"display": "none"}, "Show Correlation"


    @callback(
        Output('correlation-output', 'children'),
        Input('correlation-button', 'n_clicks'),
        Input('dropdown-selection', 'value'),
        Input('dropdown-selection-x', 'value'),
        Input('dropdown-selection-y', 'value'),
        Input('year-range-slider', 'value'),
    )
    def show_correlation(n_clicks, country, x_attr, y_attr, year_range):

        if not n_clicks:
            raise PreventUpdate
        
        if n_clicks % 2 == 0:
            return ""

        if (country is None) or (x_attr is None) or (y_attr is None):
            return "Please select attributes."

        countries = [country] if isinstance(country, str) else country

        if x_attr == y_attr:
            
            data = []
            for country in countries:
                data.append(
                    {
                        "country": country,
                        "correlation": 1.0,
                        "verdict": f"Perfect correlation between {x_attr} and {y_attr}",
                    }
                )

            return dash_table.DataTable(
                data=data,
                columns=[
                    {"name": "Country", "id": "country"},
                    {"name": "Correlation", "id": "correlation"},
                    {"name": "Verdict", "id": "verdict"},
                ],
                style_cell={"textAlign": "center"},
                style_header={"fontWeight": "bold"},
            )

        dff = processed_data[processed_data.country.isin(countries)]

        if x_attr == "year" and year_range is not None:
            dff = dff[(dff["year"] >= year_range[0]) & (dff["year"] <= year_range[1])]

        results = []
        average_correlation = 0
        count = 0
        for c in countries:
            df_country = dff[dff.country == c].dropna(subset=[x_attr, y_attr])

            if len(df_country) > 1:
                corr = df_country[x_attr].astype(float).corr(df_country[y_attr].astype(float))
            else:
                corr = None

            if corr is None:
                verdict = f"Not enough data for {c}"
            else:
                if abs(corr) > 0.7:
                    verdict = f"High correlation between {x_attr} and {y_attr}"
                elif abs(corr) > 0.3:
                    verdict = f"Moderate correlation between {x_attr} and {y_attr}"
                else:
                    verdict = f"Low correlation between {x_attr} and {y_attr}"

            results.append(
                {
                    "country": c,
                    "correlation": None if corr is None else round(corr, 3),
                    "verdict": verdict,
                }
            )
            
            if corr is not None:
                average_correlation += corr
                
            if corr is not None:
                count += 1
                
        if count > 1:
            
            results.append(
                {
                    "country": "Average",
                    "correlation": None if count == 0 else round(average_correlation / count, 3),
                    "verdict": "Average correlation across selected countries"
                }
            )

        return dash_table.DataTable(
            data=results,
            columns=[
                {"name": "Country", "id": "country"},
                {"name": "Correlation", "id": "correlation"},
                {"name": "Verdict", "id": "verdict"},
            ],
            style_cell={"textAlign": "center"},
            style_header={"fontWeight": "bold"},
        )
