# Dashboard-combined-

# 📊 Sentiment Analysis Dashboards with Plotly Dash

This project delivers a suite of interactive dashboards built using **Plotly Dash** and **Python**, enabling comprehensive **sentiment analysis** of customer reviews, movie ratings, and Twitter data. It includes individual dashboards and a **combined application** that lets users switch between all three from a central interface.

---

## 🚀 Features

- **🔄 Interactive Visualizations**
  - Pie charts, bar charts, histograms, scatter plots, word clouds, line and box plots
- **🧠 Sentiment Integration**
  - Visualizations powered by pre-processed sentiment scores and labels
- **☁️ Word Clouds**
  - Highlights frequent terms in McDonald’s reviews and Tweets
- **📈 Analytical Insights**
  - Tracks trends in customer feedback, movie sentiment, and social activity
- **🧭 Combined Dashboard**
  - `combined_dashboard.py` allows switching across dashboards from one UI
- **📱 Responsive Design**
  - Dashboards adapt across screen sizes for better UX

---

## 📦 Dashboards Included

### 🍟 McDonald's Reviews Dashboard (`mcdonaldsdashbaord.py`)
- Sentiment distribution
- Store-wise sentiment
- Review time vs. rating
- Top stores by review count
- Store locations by rating
- Word cloud from customer reviews  
📥 Input: `McDonald_s_Reviews.xlsx`

---

### 🎬 Movie Ratings Dashboard (`n_movies_dashbord.py`)
- IMDb ratings distribution
- Votes per movie
- Ratings over years
- Average ratings by genre
- Sentiment distribution
- Rating vs. duration
- Sentiment score by genre
- Rating by certificate  
📥 Input: `n_movies_coloured.xlsx`

---

### 🐦 Twitter Sentiment Dashboard (`twitter_dashboard.py`)
- Tweet sentiment distribution
- Tweets over time
- Avg. likes/retweets by sentiment
- Most active users
- Sentiment score spread
- Hourly tweet volume
- Word cloud of tweets  
📥 Input: `twitter_dataset_1.xlsx`

---

### 🧩 Combined Dashboard (`combined_dashboard.py`)
- Single page interface with dropdown to switch between:
  - McDonald’s reviews
  - Movie ratings
  - Twitter sentiment  
📥 Inputs:  
  - `McDonald_s_Reviews.xlsx`  
  - `n_movies_coloured.xlsx`  
  - `twitter_dataset_1.xlsx`

---

## 🧰 Requirements

> 📌 There is **no prebuilt `requirements.txt`

### Required Libraries

```txt
pandas
numpy
plotly
dash
dash-bootstrap-components
wordcloud
matplotlib
openpyxl
Pillow
textblob
```

### Installation Steps

```bash
# Optional: Set up a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data required for TextBlob
python -m textblob.download_corpora
```

---

## 📁 Project Structure

```
/your-project-directory/
│── combined_dashboard.py               # Main dashboard with dropdown interface
│── mcdonaldsdashbaord.py               # McDonald's reviews dashboard
│── n_movies_dashbord.py                # Movie ratings dashboard
│── twitter_dashboard.py                # Twitter sentiment dashboard
│── requirements.txt                    # (Create this file yourself)
│── README.md                           # Project documentation
│
├── /assets/
│   └── 3.png                           # Example image/logo
│
└── /data/
    ├── McDonald_s_Reviews.xlsx
    ├── n_movies_coloured.xlsx
    └── twitter_dataset_1.xlsx
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sentiment-analysis-dashboards.git
cd sentiment-analysis-dashboards
```

### 2. Add Datasets

Create a `/data/` folder and place your Excel files:

- `McDonald_s_Reviews.xlsx`
- `n_movies_coloured.xlsx`
- `twitter_dataset_1.xlsx`

Update file paths in Python scripts if necessary.

### 3. Add Static Assets

Create an `/assets/` directory and add logos/images like `3.png`.

---

## ▶️ How to Run

### 🍟 McDonald's Dashboard

```bash
python mcdonaldsdashbaord.py
```
Visit: [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

### 🎬 Movie Ratings Dashboard

```bash
python n_movies_dashbord.py
```
Visit: [http://127.0.0.1:5002](http://127.0.0.1:5002)

---

### 🐦 Twitter Sentiment Dashboard

```bash
python twitter_dashboard.py
```
Visit: [http://127.0.0.1:5050](http://127.0.0.1:5050)

---

### 🧩 Combined Dashboard

```bash
python combined_dashboard.py
```
Visit: [http://127.0.0.1:5050](http://127.0.0.1:5050)

> ⚠️ Avoid port conflicts if running Twitter and Combined dashboards at the same time.

---


