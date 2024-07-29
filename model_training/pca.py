import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
import joblib

data = pd.read_csv('../datasets/sentiment.csv')

X = data['Text']

vectorizer = CountVectorizer(stop_words='english')
X_vectorized = vectorizer.fit_transform(X)

n_components = 2
pca = PCA(n_components=n_components, random_state=42)
X_pca = pca.fit_transform(X_vectorized.toarray())

joblib.dump(pca, '../functions/pca/model.joblib')
joblib.dump(vectorizer, '../functions/pca/vectorizer.joblib')
