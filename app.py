from pickle import TRUE
from dash import Dash
from dash.dependencies import Output, Input
import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go



external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]


#import data frame
df = pd.read_csv("data/final_list.csv")


# data cleaning - renaming
df.rename(columns={"Unnamed: 0": "Index", "comp_name": "Company", "description": "Description",
"business_model": "Business Model", "customer": "Target Customer", "keywords": "Keywords",
"stage": "Stage", "total_funding": "Total Funding (in M€)", "num_investors": "Number of Investors",
"date_founded": "Year Founded", "location": "Location", "employees": "Employees", "website": "Website"}, 
inplace = TRUE)


#drop Index
df = df.drop("Index", axis=1)

# dash has problems with NAs, therefore they are filled with a string
df = df.fillna("No Information")


# dash starts here
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server



app.layout = html.Div([
    
        #header part
        html.Div([
            html.Img(src=("/assets/Logo.png")),
            html.H1(children="Start Up List"),
            html.P(id='scraping-date', children="Last scrape was the 21.05.22"),
            html.Button("Update", id='update-button', n_clicks=0),
        ], 
        id = "header-container"),


    

        #data part
        html.Div([

            html.Div([
                
                #first drop down
                html.Div([
                    html.Label("Year", className='dropdown-labels'),
                    dcc.Dropdown(
                    options=[{"label": x, "value": x} for x in df["Year Founded"].unique()],
                    id = "year-dropdown"
                    ),
                ], id = "drop-down-year",
                ),

                #second drop down
                html.Div([
                    html.Label("Stage", className='dropdown-labels'),
                    dcc.Dropdown(
                    options=[{"label": x, "value": x} for x in df["Stage"].unique()],
                    id = "stage-dropdown",
                    ),
                ], id = "drop-down-stage",
                ),
        ],id = "drop-downs"
        ),


            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=10,
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_cell={
                    'textAlign': 'left', 
                    'padding': '5px',
                    },
                style_header={
                    'fontWeight': 'bold'
                    },
                style_table={
                    'maxWidth': '1300px',
                    'overflowY' : 'scroll',
                    'overflowX' : 'scroll',
                    'maxHeight': '500px',
                    },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'Description'},
                        'width': '500px',
                    },
                ],
                fixed_columns = {
                    "headers": True,
                    "data" : 1,
                },
                # fixed_rows = {
                #     "headers": True,
                #     "data" : 0,
                # },
                export_format='xlsx',
                export_headers='display',
                merge_duplicate_headers=True

                ),
                
            ], 
            id = "data-container"),

        ], id='container'
    
)



### Callbacks to make the app interactive
# component_id = what initial component are you referring to
# component_property @ Output = property you want to change, 
#                    @ Input  = when this changes, the callback is triggered

# @app.callback(
#     Output('table', 'data'), 
#     Input('year-dropdown', 'value'),
#     Input('stage-dropdown', 'value')
# )

# def update_rows(selected_year, selected_stage):
#     dff = df.copy()

#     if selected_year:
#         dff = dff[dff['Year Founded'] == selected_year]
#     if selected_stage:
#         dff = dff[dff['Stage'] == selected_stage]

#     return dff.to_dict('records')


### Callbacks for update button

## Run script
@app.callback(
    [Output('scraping-date', 'children')], [Output('table', 'data')],
    [Input('update-button', 'n_clicks')]
    )
def run_scraper_update_content(n_clicks):
    if n_clicks:
        script_path = './test.py'
        exec(open(script_path).read())
        df = pd.read_csv("data/final_list.csv")
        return 'Last scraped on xxx, Total times updated: {}'.format(n_clicks), df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)