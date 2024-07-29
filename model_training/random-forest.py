import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv('../datasets/sentiment.csv')

X = data['Text']
y = data['Emotion']

vectorizer = CountVectorizer(stop_words='english')
X_vectorized = vectorizer.fit_transform(X)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_vectorized, y)

joblib.dump(rf, '../functions/random-forest/model.joblib')
joblib.dump(vectorizer, '../functions/random-forest/vectorizer.joblib')
