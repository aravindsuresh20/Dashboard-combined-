import pandas as pd
import numpy as np
import base64
from io import BytesIO
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# ========== Load and Clean Data ==========
df = pd.read_excel("McDonald_s_Reviews.xlsx")
df.columns = df.columns.str.strip()

df['rating'] = df['rating'].astype(str).str.extract(r'(\d)').astype(float)
df['rating_count'] = df['rating_count'].astype(str).str.replace(',', '').astype(float)
df['sentiment'] = df['rating'].apply(lambda x: 1 if x >= 4 else (-1 if x <= 2 else 0))
df['sentiment_label'] = df['sentiment'].map({1: 'Positive', 0: 'Neutral', -1: 'Negative'})

def parse_review_time(text):
    text = str(text)
    if 'day' in text:
        return 0.1
    elif 'week' in text:
        return 0.5
    elif 'month' in text:
        num = ''.join([s for s in text if s.isdigit()])
        return int(num) if num else 1
    elif 'year' in text:
        num = ''.join([s for s in text if s.isdigit()])
        return int(num)*12 if num else 12
    return np.nan

df['months_ago'] = df['review_time'].apply(parse_review_time)
df_clean = df.dropna(subset=['rating', 'rating_count', 'latitude', 'longitude', 'months_ago'])

# ========== Visualizations ==========

# Pie Chart: Sentiment
pie_fig = px.pie(df_clean, names='sentiment_label', title='Sentiment Distribution')
pie_fig.update_layout(height=800, title_font_size=24)

# Store vs Sentiment
store_sentiment = df_clean.groupby('store_address')['sentiment'].mean().reset_index()
bar_sentiment = px.bar(store_sentiment, x='store_address', y='sentiment',
                       title='Store Address vs Avg Sentiment',
                       labels={'sentiment': 'Average Sentiment'})
bar_sentiment.update_layout(height=1000, xaxis_tickangle=-45, title_font_size=24)

# Review Time vs Rating
time_rating = df_clean.groupby('months_ago')['rating'].mean().reset_index()
line_time_rating = px.line(time_rating.sort_values('months_ago'), x='months_ago', y='rating',
                           title='Review Time vs Average Rating')
line_time_rating.update_layout(height=800, title_font_size=24)

# Top Stores by Review Count
top_stores = df_clean['store_address'].value_counts().nlargest(10).reset_index()
top_stores.columns = ['store_address', 'review_count']
bar_top_stores = px.bar(top_stores, x='store_address', y='review_count',
                        title='Top 10 Stores by Review Count')
bar_top_stores.update_layout(height=1000, xaxis_tickangle=-45, title_font_size=24)

# Map: Ratings by Location
scatter_map = px.scatter(df_clean, x='longitude', y='latitude', color='rating',
                         title='Store Locations (Colored by Rating)',
                         hover_data=['store_address'])
scatter_map.update_layout(height=600, title_font_size=24)

# Store vs Avg Rating Count
rating_store = df_clean.groupby('store_address')['rating_count'].mean().reset_index()
bar_rating_count = px.bar(rating_store.sort_values('rating_count', ascending=False).head(10),
                          x='store_address', y='rating_count',
                          title='Top 10 Stores by Avg Rating Count')
bar_rating_count.update_layout(height=1000, xaxis_tickangle=-45, title_font_size=24)

# Word Cloud
text = ' '.join(df_clean['review'].dropna().astype(str).tolist())
wordcloud = WordCloud(width=1600, height=700, background_color='white').generate(text)
buffer = BytesIO()
plt.figure(figsize=(16, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.savefig(buffer, format='png')
plt.close()
encoded_wordcloud = base64.b64encode(buffer.getvalue()).decode()

# ========== Dash App ==========

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "McDonald's Review Dashboard"

app.layout = dbc.Container(fluid=True, children=[

    # Row for logo + title
    dbc.Row([
        dbc.Col(
            html.Img(src='/assets/3.png', style={'height': '140px'}),
            width='auto'
        ),
        dbc.Col(
            html.H1("🍔 McDonald's Reviews Dashboard", className='text-center my-4', style={"fontSize": "36px"}),
            width=True
        ),
    ], align="center", className='mb-4'),

    dbc.Row([dbc.Col(dcc.Graph(figure=pie_fig), width=12)]),

    dbc.Row([dbc.Col(dcc.Graph(figure=bar_sentiment), width=12)]),

    dbc.Row([dbc.Col(dcc.Graph(figure=line_time_rating), width=12)]),

    dbc.Row([dbc.Col(dcc.Graph(figure=bar_top_stores), width=12)]),

    dbc.Row([dbc.Col(dcc.Graph(figure=scatter_map), width=12)]),

    dbc.Row([dbc.Col(dcc.Graph(figure=bar_rating_count), width=12)]),

    dbc.Row([
        dbc.Col(html.Div([
            html.H3("Word Cloud of Reviews", className='text-center mt-4'),
            html.Img(src='data:image/png;base64,{}'.format(encoded_wordcloud),
                     style={'width': '100%', 'border': '1px solid #ccc', 'margin-top': '10px'})
        ]), width=12),
    ]),

    html.Footer("Created  using Plotly Dash", className='text-center mt-5 mb-2 text-muted', style={'fontSize': '18px'})
], style={'backgroundColor': '#ffffff', 'padding': '30px'})

if __name__ == '__main__':
    app.run(debug=True)