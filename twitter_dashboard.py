import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
import base64
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc
import os # Import os module to check for file existence

# Load dataset
df = pd.read_excel("twitter_dataset_1.xlsx")
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')
df['Hour'] = df['Timestamp'].dt.hour
df['Sentiment_Label'] = df['sentiment'].map({1: 'Positive', -1: 'Negative', 0: 'Neutral'})

# 1. Pie Chart - Sentiment Distribution
sentiment_counts = df['Sentiment_Label'].value_counts()
fig1 = px.pie(values=sentiment_counts.values, names=sentiment_counts.index,
              title='Tweet Sentiment Distribution', height=800)

# 2. Line Chart - Tweets Over Time
tweets_per_day = df.groupby(df['Timestamp'].dt.date).size().reset_index(name='Tweet Count')
fig2 = px.line(tweets_per_day, x='Timestamp', y='Tweet Count', title='Tweets Over Time', height=800)

# 3. Bar Chart - Likes by Sentiment
likes_by_sentiment = df.groupby('Sentiment_Label')['Likes'].mean().reset_index()
fig3 = px.bar(likes_by_sentiment, x='Sentiment_Label', y='Likes',
              title='Average Likes by Sentiment', height=800)

# 4. Bar Chart - Retweets by Sentiment
retweets_by_sentiment = df.groupby('Sentiment_Label')['Retweets'].mean().reset_index()
fig4 = px.bar(retweets_by_sentiment, x='Sentiment_Label', y='Retweets',
              title='Average Retweets by Sentiment', height=800)

# 5. Bar Chart - Top 10 Active Users
top_users = df['Username'].value_counts().head(10)
fig5 = px.bar(x=top_users.index, y=top_users.values,
              title='Top 10 Most Active Users',
              labels={'x': 'Username', 'y': 'Number of Tweets'}, height=800)

# 6. Histogram - Sentiment Score Distribution
fig6 = px.histogram(df, x='sentiment_score', nbins=30,
                    title='Sentiment Score Distribution', height=800)

# 7. Bar Chart - Hourly Tweet Activity
hourly_counts = df.groupby('Hour').size().reset_index(name='Tweet Count')
fig7 = px.bar(hourly_counts, x='Hour', y='Tweet Count', title='Hourly Tweet Activity', height=800)

# 8. Word Cloud
text = " ".join(str(tweet) for tweet in df['Text'].dropna())
wordcloud = WordCloud(width=1500, height=1000, background_color='white').generate(text)
wordcloud_path = "wordcloud.png"
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig(wordcloud_path)
plt.close()

# Encode logo and word cloud
logo_path = "assets/3.png"  # Replace with your actual logo path

# --- Add dummy logo for testing if it doesn't exist ---
if not os.path.exists("assets"):
    os.makedirs("assets")
if not os.path.exists(logo_path):
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (100, 50), color = 'green')
    d = ImageDraw.Draw(img)
    d.text((10,10), "LOGO", fill=(255,255,255))
    img.save(logo_path)
    print(f"Dummy logo created at: {logo_path}")
# --- End of dummy logo creation ---

# Ensure logo_path and wordcloud_path exist before encoding
try:
    encoded_logo = base64.b64encode(open(logo_path, 'rb').read()).decode()
    encoded_wc = base64.b64encode(open(wordcloud_path, 'rb').read()).decode()
except FileNotFoundError as e:
    print(f"Error: Make sure '{e.filename}' exists. Please check your `logo_path` and `wordcloud_path`.")
    # Exit or handle gracefully if files are missing
    exit()


# Dash App Layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Twitter Sentiment Dashboard"

app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.Img(src=f'data:image/png;base64,{encoded_logo}',
                     style={'height': '80px', 'padding': '10px 0 10px 20px'}), # Padding adjusted for left alignment
            width={"size": "auto"}, # Column width based on content
            align="center" # Vertically center the logo
        ),
        dbc.Col(
            html.H1("Twitter Sentiment Dashboard", className="text-center mb-0"), # text-center for horizontal centering, mb-0 to remove bottom margin
            align="center" # Vertically center the heading
        )
    ], justify="start", # Align row content to the start (left) - no effect on text centering in the col
       className="align-items-center mb-4", # Vertically align items in the row, add bottom margin
       style={'width': '100%'} # Ensure the row takes full width
    ),


    dcc.Graph(figure=fig1),  # Tweet Sentiment Distribution
    dcc.Graph(figure=fig2),  # Tweets Over Time
    dcc.Graph(figure=fig3),  # Average Likes by Sentiment
    dcc.Graph(figure=fig4),  # Average Retweets by Sentiment
    dcc.Graph(figure=fig5),  # Top 10 Most Active Users
    dcc.Graph(figure=fig6),  # Sentiment Score Distribution
    dcc.Graph(figure=fig7),  # Hourly Tweet Activity

    html.H2("Word Cloud of Tweets", style={'text-align': 'center'}),
    html.Div([
        html.Img(src=f'data:image/png;base64,{encoded_wc}',
                 style={'display': 'block', 'margin': '0 auto', 'max-width': '100%'})
    ])
])

if __name__ == '__main__':
    app.run(port=5050, debug=True)