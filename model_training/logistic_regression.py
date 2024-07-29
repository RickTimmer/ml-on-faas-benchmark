import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

data = pd.read_csv('../datasets/sentiment.csv')

X = data['Text']
y = data['Emotion']

vectorizer = CountVectorizer(stop_words='english')
X_vectorized = vectorizer.fit_transform(X)

logreg = LogisticRegression(max_iter=1000, random_state=42)
logreg.fit(X_vectorized, y)

joblib.dump(logreg, '../functions/logistic-regression/model.joblib')
joblib.dump(vectorizer, '../functions/logistic-regression/vectorizer.joblib')
