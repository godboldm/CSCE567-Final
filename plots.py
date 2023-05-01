import plotly.graph_objects as go

# Function to create a bar chart for driver success
def driver_bar(data):
    fig = go.Figure(data=[
        go.Bar(name='Wins', x=data['driverRef'], y=data['wins']),
        go.Bar(name='Podiums', x=data['driverRef'], y=data['podiums']),
        go.Bar(name='Points', x=data['driverRef'], y=data['points'])
    ])
    fig.update_layout(barmode='group')
    return fig

# Function to create a diverging bar chart for driver conversions
def driver_diverging_bar(data):
    fig = go.Figure(data=[
        go.Bar(name='Pit Stops', x=data['driverRef'], y=data['pit_stops']),
        go.Bar(name='Pit Stops', x=data['driverRef'], y=data['pit_stops'])
    ])
    fig.update_layout(barmode='group')
    return fig

# Function to create a line chart for driver position
def driver_line(data):
    fig = go.Figure(data=go.Scatter(x=data['driverRef'], y=data['position']))
    return fig

# Function to create a pie chart for pit duration
def driver_pie(data):
    fig = go.Figure(data=[go.Pie(labels=data['driverRef'], values=data['duration'])])
    return fig

# Function to create a bar chart for constructor success
def constructor_bar(data):
    fig = go.Figure(data=[
        go.Bar(name='Wins', x=data['constructorRef'], y=data['wins']),
        go.Bar(name='Podiums', x=data['constructorRef'], y=data['podiums']),
        go.Bar(name='Points', x=data['constructorRef'], y=data['points'])
    ])
    fig.update_layout(barmode='group')
    return fig

# Function to create a map for constructor driver locations
def constructor_map(data):
    fig = go.Figure(data=go.Scattergeo(
        lon = data['lng'],
        lat = data['lat'],
        text = data['driverRef'],
        mode = 'markers',
        marker_color = data['wins'],
        ))

    fig.update_layout(
        title = 'Constructor Driver Locations',
        geo_scope='world',
    )
    return fig

# Function to create a histogram for constructor points
def constructor_hist(data):
    fig = plt.figure()
    plt.hist(data['points'], bins=20)
    return fig

# Function to create a scatter plot for constructor's driver positions over time
def constructor_scatter(data):
    fig = go.Figure(data=go.Scatter(x=data['year'], y=data['position']))
    return fig