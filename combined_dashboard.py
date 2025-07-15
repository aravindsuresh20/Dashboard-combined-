import pandas as pd

import numpy as np

import base64

from io import BytesIO

from wordcloud import WordCloud

import matplotlib

matplotlib.use('Agg')  # Use non-interactive backend

import matplotlib.pyplot as plt

import plotly.express as px

import plotly.graph_objs as go

from dash import Dash, html, dcc, Output, Input

import dash_bootstrap_components as dbc

# Initialize app

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Combined Dashboard"

# Initialize global variables

df_mcd, df_tw, df_mv = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

figs_mcd, figs_tw, figs_mv = [], [], []

encoded_wc_mcd, encoded_wc_tw = "", ""

# ---------------- McDonald's Data ----------------

print("--- Loading and processing McDonald's data ---")

try:

    df_mcd = pd.read_excel("McDonald_s_Reviews.xlsx")

    df_mcd.columns = df_mcd.columns.str.strip()

    df_mcd['rating'] = df_mcd['rating'].astype(str).str.extract(r'(\d)').astype(float)

    df_mcd['rating_count'] = df_mcd['rating_count'].astype(str).str.replace(',', '').astype(float)

    df_mcd['sentiment'] = df_mcd['rating'].apply(lambda x: 1 if x >= 4 else (-1 if x <= 2 else 0))

    df_mcd['sentiment_label'] = df_mcd['sentiment'].map({1: 'Positive', 0: 'Neutral', -1: 'Negative'})

    def parse_review_time(text):

        text = str(text).lower()

        if 'day' in text: return 0.1

        elif 'week' in text: return 0.5

        elif 'month' in text:

            num = ''.join([s for s in text if s.isdigit()])

            return int(num) if num else 1

        elif 'year' in text:

            num = ''.join([s for s in text if s.isdigit()])

            return int(num)*12 if num else 12

        return np.nan

    df_mcd['months_ago'] = df_mcd['review_time'].apply(parse_review_time)

    critical_cols = ['rating', 'rating_count', 'latitude', 'longitude', 'months_ago', 'store_address', 'review', 'sentiment_label', 'sentiment']

    for col in critical_cols:

        if col not in df_mcd.columns:

            print(f"Missing column: {col}")

            df_mcd = pd.DataFrame()

            break

    if not df_mcd.empty:

        df_mcd.dropna(subset=critical_cols, inplace=True)

        # Graphs

        figs_mcd.append(px.pie(df_mcd, names='sentiment_label', title='Sentiment Distribution'))

        figs_mcd.append(px.bar(df_mcd.groupby('store_address')['sentiment'].mean().reset_index(),

                               x='store_address', y='sentiment', title='Store vs Avg Sentiment'))

        figs_mcd.append(px.line(df_mcd.groupby('months_ago')['rating'].mean().reset_index().sort_values('months_ago'),

                                x='months_ago', y='rating', title='Review Time vs Rating'))

        top_10 = df_mcd['store_address'].value_counts().nlargest(10).reset_index()

        top_10.columns = ['store_address', 'review_count']

        figs_mcd.append(px.bar(top_10, x='store_address', y='review_count', title='Top 10 Stores by Reviews'))

        figs_mcd.append(px.scatter(df_mcd, x='longitude', y='latitude', color='rating', title='Store Locations by Rating',

                                   hover_data=['store_address']))

        figs_mcd.append(px.bar(df_mcd.groupby('store_address')['rating_count'].mean().reset_index().sort_values('rating_count', ascending=False).head(10),

                               x='store_address', y='rating_count', title='Top 10 by Avg Rating Count'))

        # Word Cloud

        text = ' '.join(df_mcd['review'].dropna().astype(str))

        if text.strip():

            wc = WordCloud(width=1600, height=700, background_color='white').generate(text)

            buf = BytesIO()

            plt.figure(figsize=(16, 8))

            plt.imshow(wc, interpolation='bilinear')

            plt.axis('off')

            plt.tight_layout()

            plt.savefig(buf, format='png')

            plt.close()

            encoded_wc_mcd = base64.b64encode(buf.getvalue()).decode()

except Exception as e:

    print(f"Error in McDonald's Data: {e}")

# ---------------- Twitter Data ----------------

print("\n--- Loading and processing Twitter data ---")

try:

    df_tw = pd.read_excel("twitter_dataset_1.xlsx")

    df_tw['Timestamp'] = pd.to_datetime(df_tw['Timestamp'], errors='coerce')

    df_tw.dropna(subset=['Timestamp'], inplace=True)

    df_tw['Hour'] = df_tw['Timestamp'].dt.hour

    df_tw['Sentiment_Label'] = df_tw['sentiment'].map({1: 'Positive', -1: 'Negative', 0: 'Neutral'})

    tw_cols = ['Timestamp', 'sentiment', 'Likes', 'Retweets', 'Username', 'sentiment_score', 'Text', 'Hour', 'Sentiment_Label']

    for col in tw_cols:

        if col not in df_tw.columns:

            print(f"Missing column: {col}")

            df_tw = pd.DataFrame()

            break

    if not df_tw.empty:

        df_tw.dropna(subset=tw_cols, inplace=True)

        figs_tw.append(px.pie(df_tw, names='Sentiment_Label', title='Tweet Sentiment Distribution'))

        figs_tw.append(px.line(df_tw.groupby(df_tw['Timestamp'].dt.date).size().reset_index(name='Tweet Count'),

                               x='Timestamp', y='Tweet Count', title='Tweets Over Time'))

        figs_tw.append(px.bar(df_tw.groupby('Sentiment_Label')['Likes'].mean().reset_index(),

                              x='Sentiment_Label', y='Likes', title='Avg Likes by Sentiment'))

        figs_tw.append(px.bar(df_tw.groupby('Sentiment_Label')['Retweets'].mean().reset_index(),

                              x='Sentiment_Label', y='Retweets', title='Avg Retweets by Sentiment'))

        figs_tw.append(px.bar(x=df_tw['Username'].value_counts().head(10).index,

                              y=df_tw['Username'].value_counts().head(10).values,

                              title='Top 10 Active Users'))

        figs_tw.append(px.histogram(df_tw, x='sentiment_score', nbins=30, title='Sentiment Score Distribution'))

        figs_tw.append(px.bar(df_tw.groupby('Hour').size().reset_index(name='Tweet Count'),

                              x='Hour', y='Tweet Count', title='Hourly Tweet Activity'))

        text = ' '.join(df_tw['Text'].dropna().astype(str))

        if text.strip():

            wc = WordCloud(width=1500, height=1000, background_color='white').generate(text)

            buf = BytesIO()

            plt.figure(figsize=(10, 5))

            plt.imshow(wc, interpolation='bilinear')

            plt.axis("off")

            plt.tight_layout()

            plt.savefig(buf, format='png')

            plt.close()

            encoded_wc_tw = base64.b64encode(buf.getvalue()).decode()

except Exception as e:

    print(f"Error in Twitter Data: {e}")

# ---------------- Movies Data ----------------

print("\n--- Loading and processing Movies data ---")

try:

    df_mv = pd.read_excel("n_movies_coloured.xlsx")

    df_mv['year_clean'] = df_mv['year'].astype(str).str.extract(r'(\d{4})').astype(float)

    df_mv['duration_min'] = df_mv['duration'].astype(str).str.extract(r'(\d+)').astype(float)

    df_mv['genre_main'] = df_mv['genre'].astype(str).str.split(',').str[0].replace('', np.nan)

    df_mv['sentiment_label'] = df_mv['sentiment'].map({1: 'Positive', 0: 'Neutral', -1: 'Negative'})

    mv_cols = ['rating', 'votes', 'duration_min', 'year_clean', 'sentiment_score', 'sentiment_label', 'genre_main', 'certificate']

    for col in mv_cols:

        if col not in df_mv.columns:

            print(f"Missing column: {col}")

            df_mv = pd.DataFrame()

            break

    if not df_mv.empty:

        df_mv.dropna(subset=mv_cols, inplace=True)

        figs_mv.append(px.pie(df_mv, names='sentiment_label', title='Sentiment Distribution'))

        figs_mv.append(go.Figure(data=[go.Box(y=df_mv['rating'], name='IMDb Ratings')], layout=dict(title='Box Plot of IMDb Ratings')))

        figs_mv.append(go.Figure(data=[go.Histogram(x=df_mv['votes'])], layout=dict(title='Distribution of Votes')))

        figs_mv.append(go.Figure(data=[go.Scatter(x=df_mv['year_clean'], y=df_mv['rating'], mode='markers',

                                                  marker=dict(color=df_mv['sentiment_score'], colorscale='Viridis', showscale=True))],

                                 layout=dict(title='Ratings Over Years')))

        figs_mv.append(go.Figure(data=[go.Bar(x=df_mv.groupby('genre_main')['rating'].mean().sort_values(ascending=False).index,

                                              y=df_mv.groupby('genre_main')['rating'].mean().sort_values(ascending=False).values)],

                                 layout=dict(title='Avg Rating by Genre')))

except Exception as e:

    print(f"Error in Movie Data: {e}")

# ---------------- Layout ----------------

app.layout = dbc.Container([

    dbc.Row([

        dbc.Col(html.Img(src='/assets/3.png', style={'height': '60px'}), width="auto"),

        dbc.Col(html.H2("📊 Unified Dashboard Viewer", className="text-center text-primary my-3"), width=True),

        dbc.Col(width="auto")

    ], align='center', className='mb-4'),

    dbc.Row([

        dbc.Col(dcc.Dropdown(

            id='dashboard-selector',

            options=[

                {'label': "McDonald's Reviews", 'value': 'mcd'},

                {'label': "Twitter Sentiment", 'value': 'twitter'},

                {'label': "Movies Sentiment", 'value': 'movies'},

            ],

            value='mcd',

            clearable=False

        ), width=6)

    ], justify='center'),

    dbc.Row([

        dbc.Col(id='dashboard-output')

    ])

], fluid=True)

# ---------------- Callback ----------------

@app.callback(

    Output('dashboard-output', 'children'),

    Input('dashboard-selector', 'value')

)

def render_dashboard(selected):

    content = []

    if selected == 'mcd':

        if figs_mcd:

            content.extend([dcc.Graph(figure=fig) for fig in figs_mcd])

        else:

            content.append(html.P("No McDonald's review graphs available."))

        if encoded_wc_mcd:

            content.extend([

                html.H3("Word Cloud of Reviews", className='text-center mt-4'),

                html.Img(src='data:image/png;base64,{}'.format(encoded_wc_mcd), style={'width': '100%'})

            ])

    elif selected == 'twitter':

        if figs_tw:

            content.extend([dcc.Graph(figure=fig) for fig in figs_tw])

        else:

            content.append(html.P("No Twitter graphs available."))

        if encoded_wc_tw:

            content.extend([

                html.H3("Word Cloud of Tweets", className='text-center mt-4'),

                html.Img(src='data:image/png;base64,{}'.format(encoded_wc_tw), style={'width': '100%'})

            ])

    elif selected == 'movies':

        if figs_mv:

            content.extend([dcc.Graph(figure=fig) for fig in figs_mv])

        else:

            content.append(html.P("No movie graphs available."))

    return html.Div(content)  # ✅ FIXED: Wrapped in Div

# ---------------- Run ----------------

if __name__ == '__main__':

    app.run(port=5050, debug=True)
 