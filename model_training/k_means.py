import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import joblib

data = pd.read_csv('../datasets/sentiment.csv')

X = data['Text']

vectorizer = CountVectorizer(stop_words='english')
X_vectorized = vectorizer.fit_transform(X)

n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(X_vectorized)

joblib.dump(kmeans, '../functions/k-means/model.joblib')
joblib.dump(vectorizer, '../functions/k-means/vectorizer.joblib')
