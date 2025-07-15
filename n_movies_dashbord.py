import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# Load Excel data
df = pd.read_excel("n_movies_coloured.xlsx")

# Data Cleaning & Preparation
df['year_clean'] = df['year'].str.extract(r'(\d{4})').astype(float)
df['duration_min'] = df['duration'].str.extract(r'(\d+)').astype(float)
df['genre_main'] = df['genre'].str.split(',').str[0]
df['sentiment_label'] = df['sentiment'].map({1: 'Positive', 0: 'Neutral', -1: 'Negative'})

df_clean = df.dropna(subset=['rating', 'votes', 'duration_min', 'year_clean', 'sentiment_score'])

# 1. IMDb Ratings Boxplot
fig1 = go.Figure()
fig1.add_trace(go.Box(y=df_clean['rating'], name='IMDb Ratings', boxmean=True))
fig1.update_layout(title='Box Plot of IMDb Ratings')

# 2. Votes Distribution
fig2 = go.Figure()
fig2.add_trace(go.Histogram(x=df_clean['votes'], nbinsx=30))
fig2.update_layout(title='Distribution of Votes', xaxis_title='Votes', yaxis_title='Count')

# 3. Ratings Over the Years
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=df_clean['year_clean'],
    y=df_clean['rating'],
    mode='markers',
    marker=dict(color=df_clean['sentiment_score'], colorscale='Viridis', showscale=True),
    text=df_clean['title']
))
fig3.update_layout(title='Ratings Over the Years (Colored by Sentiment Score)',
                   xaxis_title='Year', yaxis_title='Rating')

# 4. Average Rating by Genre
genre_rating = df_clean.groupby('genre_main')['rating'].mean().sort_values(ascending=False)
fig4 = go.Figure()
fig4.add_trace(go.Bar(x=genre_rating.index, y=genre_rating.values))
fig4.update_layout(title='Average Rating by Main Genre', xaxis_title='Genre', yaxis_title='Average Rating')

# 5. Sentiment Pie
sentiment_counts = df_clean['sentiment_label'].value_counts()
fig5 = go.Figure()
fig5.add_trace(go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values))
fig5.update_layout(title='Sentiment Distribution of Movies')

# 6. Rating vs Duration
fig6 = go.Figure()
fig6.add_trace(go.Scatter(
    x=df_clean['duration_min'],
    y=df_clean['rating'],
    mode='markers',
    text=df_clean['title'],
    marker=dict(color='orange')
))
fig6.update_layout(title='Rating vs. Duration', xaxis_title='Duration (min)', yaxis_title='Rating')

# 7. Sentiment Score by Genre
fig7 = go.Figure()
fig7.add_trace(go.Box(y=df_clean['sentiment_score'], x=df_clean['genre_main'], boxmean=True))
fig7.update_layout(title='Sentiment Score by Genre', xaxis_title='Genre', yaxis_title='Sentiment Score')

# 8. Rating by Certificate
rating_by_cert = df_clean.groupby('certificate')['rating'].mean().sort_values()
fig8 = go.Figure()
fig8.add_trace(go.Bar(x=rating_by_cert.index, y=rating_by_cert.values))
fig8.update_layout(title='Average Rating by Certificate', xaxis_title='Certificate', yaxis_title='Average Rating')

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src="/assets/3.png", height="60px"), width="auto"),
        dbc.Col(html.H2("Movies Sentiment Analysis Dashboard", className="text-center text-primary mb-4"), width=True),
    ], align="center", className="mb-4"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig1), md=6),
        dbc.Col(dcc.Graph(figure=fig2), md=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig3), md=6),
        dbc.Col(dcc.Graph(figure=fig4), md=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig5), md=6),
        dbc.Col(dcc.Graph(figure=fig6), md=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig7), md=6),
        dbc.Col(dcc.Graph(figure=fig8), md=6),
    ]),
], fluid=True)

# Run server
if __name__ == "__main__":
    app.run(port=5002)
