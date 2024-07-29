import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.mixture import GaussianMixture
import joblib

data = pd.read_csv('../datasets/sentiment.csv')

X = data['Text']

vectorizer = CountVectorizer(stop_words='english', max_features=3000)
X_vectorized = vectorizer.fit_transform(X)

X_dense = X_vectorized.toarray()

n_components = 2
gmm = GaussianMixture(n_components=n_components, random_state=42)
gmm.fit(X_dense)

joblib.dump(gmm, '../functions/gaussian-mixture/model.joblib')
joblib.dump(vectorizer, '../functions/gaussian-mixture/vectorizer.joblib')
