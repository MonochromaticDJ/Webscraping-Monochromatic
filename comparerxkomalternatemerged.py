import pandas as pd
import dash
import pathlib
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve

# Load the 'name', 'price', 'link' columns from 'xkomwithlinks.xlsx'
df_all = pd.read_excel('xkomwithlinks.xlsx', usecols=['name', 'price', 'link'])

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Layout of the app
app.layout = html.Div([
    dcc.Input(id='search-bar', type='text', placeholder='Search by product name...'),
    dcc.Graph(id='price-bar-chart')
])

# Define callback to update the bar chart based on search
@app.callback(
    Output('price-bar-chart', 'figure'),
    [Input('search-bar', 'value')]
)
def update_chart(search_value):
    # Filter the DataFrame based on search value
    if search_value:
        filtered_df = df_all[df_all['name'].str.contains(search_value, case=False)]
    else:
        filtered_df = df_all

    # Sort the DataFrame by prices in ascending order
    filtered_df = filtered_df.sort_values(by='price', ascending=True)

    # Data visualization using Plotly graph objects
    fig = go.Figure()

    # Bar chart with bars aligned with the y-axis
    bar_trace = go.Bar(
        x=filtered_df['name'],
        y=filtered_df['price'],
        base=0,  # Set the base to 0 to align bars with the y-axis
        marker=dict(
            color=filtered_df['price'],  # Use price values for color
            colorscale='Cividis',
            
        ),
        hoverinfo='text',
        hovertext=filtered_df.apply(
            lambda row: f'{row["name"]}<br>Price: {row["price"]}',
            axis=1
        )
    )

    fig.add_trace(bar_trace)

    # Add annotations with hyperlinks to the top of each bar
    annotations = []
    for index, row in filtered_df.iterrows():
        annotation = dict(
            x=row['name'],
            y=row['price'],
            xref='x',
            yref='y',
            text=f'<a href="{row["link"]}" target="_blank">.</a>',
            showarrow=False,
            font=dict(
                color='black',
                size=50
            ),
            hovertext=f'<a href="{row["link"]}" target="_blank">link</a>'
        )
        annotations.append(annotation)

    # Update layout to include annotations
    fig.update_layout(
        xaxis=dict(title='Product Name', tickangle=30),  # Tilt the product names by 30 degrees
        yaxis=dict(title='Price'),
        template='plotly',
        height=1400,
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20),
        title=dict(
            text='Zoomable database of all x-kom.pl iPhones (with hyperlinks available on the very top of each bar)',
            x=0.5,  # Centered title
            font=dict(size=32)  # Double the font size
        ),
        annotations=annotations
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
